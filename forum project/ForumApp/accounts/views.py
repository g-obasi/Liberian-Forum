from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth import login as auth_login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import SignUpForm, UserInfoUpdateForm
from .models import User

from forum.models import Post, Topic


# USER VIEW CONFIGURATION

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserInfoUpdateForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('my_account')
    
    def get_initial(self):
        dict ={''}
        return dict

    def form_valid(self, form):
        files = self.request.FILES.getlist('files')
        message = form.cleaned_data['message']

        post = Post.objects.create(
                message=message,
                last_updated=datetime.now()
                )

        post.save()

        for file in files:
            Attachment.objects.create(post=post,
                                    image=file)

        post_url = '{url}?page={page}#{id}'.format(
                url=post.get_absolute_url(),
                id=post.pk,
                page=self.topic.get_page_count()
            )
        return redirect(post_url)

@login_required()
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    topics = Topic.objects.filter(created_by=user)
    posts = Post.objects.filter(created_by=user)
    # print(posts)
    
    posts_count = Post.objects.filter(created_by=user).count()
    topics_count = Topic.objects.filter(created_by=user).count()
  

    user = get_object_or_404(User, username=user)
    context = {
                'user': user,
                'topics': topics,
                'posts': posts,
                'topics_count': topics_count,
                'posts_count': posts_count,
    }

    if request.user.username == username:
        return render(request, 'account/my_account.html', context)
    else:
        return render(request, 'account/profile_view.html', context)


@login_required()
def following(request, username):
    user = User.objects.get_object_or_404(username)
    followings = user.followings.all()
    return render(request, 'account/followings.html', {'followings': followings})


@login_required()
def followers(request, username):
    user = User.objects.get_object_or_404(username)
    followers = user.followers.all()
    return render(request, 'account/followers.html', {'followers': followers})


# @login_required()
# def view_posts(request, username):
#     user = User.objects.get_object_or_404(username)
#     my_posts = Post.objects.filter(created_by=user)
#     return render(request, 'account/view_posts.html', {'my_posts': my_posts})


class ViewPosts(ListView, LoginRequiredMixin):
    model = Post
    template_name = 'account/view_posts.html'
    context_object_name = 'my_posts'
    # paginate_by = 20

    def get_queryset(self):
        user = User.objects.get_object_or_404(self.kwargs['username'])
        queryset = Post.objects.filter(created_by=user)
        return queryset


class ViewTopics(ListView, LoginRequiredMixin):
    model = Topic
    template_name = 'account/view_posts.html'
    context_object_name = 'my_topics'
    # paginate_by = 20

    def get_queryset(self):
        user = User.objects.get_object_or_404(self.kwargs['username'])
        queryset = Topic.objects.filter(created_by=user)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get_object_or_404(self.kwargs['username'])
        posts = Post.objects.filter(created_by=user)
        context['posts'] = Post.objects.filter(created_by=user)
        
        context['post_count'] = Post.objects.filter(created_by=user).count()


@login_required()
def view_topics(request, username):
    user = User.objects.get_object_or_404(username)
    my_topics = Topic.objects.filter(created_by=user)
    posts = Post.objects.filter(created_by=user)
    posts_count = Post.objects.filter(created_by=user).count()

    return render(request, 'account/view_topics.html', {'posts': posts, 'posts_count': posts_count, 'my_topics': my_topics})


@login_required()
def my_likes(request, username):
    user = User.objects.get_object_or_404(username)
    my_likes = user.post_likes.all()
    return render(request, 'account/my_likes.html', {'my_likes': my_likes})


@login_required()
def my_shares(request, username):
    user = User.objects.get_object_or_404(username)
    my_shares = user.post_shares.all()
    return render(request, 'account/my_shares.html', {'my_shares': my_shares})
