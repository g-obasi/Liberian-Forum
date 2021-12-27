from datetime import datetime, timedelta
# from django.core.paginator import Paginator
import os
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import HttpResponse
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect, reverse
from itertools import chain
from django.core.mail import send_mail, mail_admins
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, Count

from .models import Post, Board, Topic, Attachment
from .forms import PostForm, QuoteForm, TopicForm, PostUpdateForm, BoardChoiceForm, FileForm
from LibForum import settings
from accounts.models import User


def index(request):
    return HttpResponse('<h1> This is the Homepage<h1>')


class NewsList(ListView):
    # model = Topic
    template_name = 'forum/news.html'
    context_object_name = 'featured_news'
    queryset = Topic.objects.filter(featured=True).order_by('-date_created')
    paginate_by = 80


class FeaturedTopic(ListView):
    # model = Topic
    template_name = 'forum/home.html'
    paginate_by = 60
    context_object_name = 'featured_topics'
    queryset = Topic.objects.filter(featured=True).order_by('-date_created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_count'] = User.objects.count()
        return context


class SectionTopic(ListView):
    # model = Topic
    template_name = 'forum/section.html'
    context_object_name = 'topics'
    paginate_by = 60

    def get_queryset(self):
        board = get_object_or_404(Board, name=self.kwargs['board_name'])
        queryset = Topic.objects.filter(board=board)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        board = get_object_or_404(Board, name=self.kwargs['board_name'])
        # print(board.id)
        context['child_boards'] = Board.objects.filter(parent=board)
        context['board'] = board

        # FOR TOPIC FOLLOW
        if self.request.user.is_authenticated:
            if board.followers.filter(board_followers=self.request.user).exists():
                context['follow_text'] = 'Unfollow'
            else:
                context['follow_text'] = 'Follow'
        return context



class BoardView(ListView):
    model = Board
    template_name = 'forum/board_topic_view.html'
    template_name_suffix = None
    context_object_name = 'board'
    # paginate_by = 20

    def get_queryset(self):
        board = get_object_or_404(Board, pk=self.kwargs.get('name'))
        queryset = board.topics.order_by('-last_updated')
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    template_name = 'forum/create_topic.html'
    template_name_suffix = None
    # success_url = reverse('topic/section_posts/')
    form_class = TopicForm
    # files = request.FILES.getlist('images')

# create a kwarg to accept board_pk
    def form_valid(self, form):
        subject = form.cleaned_data['title']  # Topic
        message = form.cleaned_data['message']  # Post
        board_pk = self.kwargs['board_pk']
        board = get_object_or_404(Board, pk=board_pk)
        print(board)
        files = self.request.FILES.getlist('image')
        user = self.request.user

        topic = Topic(
            created_by=user,
            title=subject,
            slug=slugify(subject),
            board=board,
            views=F('views') + 1,
            post_count=F('post_count') + 1,
            )
        topic.followers.add(user)

        post = Post.objects.create(
                message=message,
                topic=topic,
                created_by=user,
                )
        post.save()
        topic.save()

        for file in files:
            Attachment.objects.create(
                post=post, image=file
            )

        return redirect('/')


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = 'forum/delete_topic.html'
    template_name_suffix = None


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'forum/create_post.html'
    template_name_suffix = None
    form_class = PostForm
    redirect_field_name = 'posts/<int:pk>/'

    def form_valid(self, form):
        files = self.request.FILES.getlist('image')
        message = form.cleaned_data['message']
        topic = self.request.get['topic_pk']

        post = Post.objects.create(
                message=message,
                topic=topic,
                created_by=self.request.user,
                last_updated=datetime.now()
                )
        topic.post_count = F('post_count') + 1
        post.save()
        topic.save()

        for file in files:
            Attachment.objects.create(post=post,
                                    image=file)

        post_url = '{url}?page={page}#{id}'.format(
                url=post.get_absolute_url(),
                id=post.id,
                page=topic.post.get_page_count()
            )
        return redirect(post_url)


def ReportInnapropiatePost(request,  post_id, report_reason):
    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(User, pk=request.user.id)
    message = " Please check this post with the POST ID - <b>{post_id}</b> <br>POST REPORTER ID - {reporter_id} <br>CONTENT = <b>{post_content}</b> if it is Appropriate or Not".format(
                post_id=post.id,
                reporter_id=user.id,
                post_content=post.message
    )
    
    # send_mail(" REPORT POST", message="", from_email="", )
    mail_admins("REPORT POST",  html_message=message)



def likes_and_shares(request):
    pass


def trending(request): pass


@login_required()
def mentions(request): pass


#  Latest post by people you're followin
@login_required()
def following_people_post(request):
    user = request.user.id
    posts = Post.objects.filter(created_by__followings__followes=user)
    return render(request, 'forum/following_people_feed.html', {'posts': posts})



# def recent_posts(request):
#     time_48hours = datetime.now() - timedelta(hours=48)
#     recent_48 = Post.objects.filter(date_created__gte=time_48hours)
#     return render(request, 'forum/recent.html', {'recent': recent_48})


class RecentPostList(ListView):
    # model = Post
    template_name = 'forum/recent.html'
    context_object_name = 'recent_post'
    paginate_by = 80

    def get_queryset(self):
        time_48hours = datetime.now() - timedelta(hours=48)
        queryset = Post.objects.filter(date_created__gte=time_48hours)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])
        context['topic'] = topic

        # FOR TOPIC FOLLOW
        if topic.followers.filter(id=self.request.user.id).exists():
            context['follow_text'] = 'Unfollow'
        else:
            context['follow_text'] = 'Follow'

        
        for post in self.get_queryset():
            if post.totalikescount() >= 1:
                context['likes_count'], context['like_txt'] = post.totalikescount(), 'Like'

            if post.totalsharescount() >= 1:
                context['shares_count'], context['share_txt'] = post.totalsharescount(), 'Share'

        # FOR POST LIKE
            if post.liked_by.filter(id=self.request.user.id).exists():
                context['like_state'] = 'Unlike'
            else:
                context['like_state'] = 'Like'

        # FOR POST SHARE
            if post.shared_by.filter(id=self.request.user.id).exists():
                context['share_state'] = 'Un-Share'
            else:
                context['share_state'] = 'Share'
        return context



def new_posts(request):
    time_5hours = datetime.now() - timedelta(hours=5)
    new_5 = Post.objects.filter(date_created__gte=time_5hours)
    return render(request, 'forum/new.html', {'new_posts': new_5})


@login_required()
def followed_topics(request, username):
    user = get_object_or_404(User, username=username)
    followed_topics = user.thread_followers.all()
    return render(request, 'forum/followed_threads.html', {'followed_topics': followed_topics})


# follow - unfollow boards
# class FollowedBoards(ListView):
#     template_name = 'forum/followed_boards.html'
#     paginate_by = 60

#     def get_queryset(self):
#         queryset = Board.objects.filter(followed_by=self.request.user)
#         # topics
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
    

@login_required()
def followed_boards(request, username, keyword=None):
    user = User.get_object_or_404(username)
    
    if request.method == 'POST':
        form = BoardChoiceForm(request.Post)

    if form.is_valid:
        board = form.cleaned_data.get('board_select')
        board = get_object_or_404(Board, name=board)

    if user.board.filter(pk=board).exists():
        pass
    else:
        user.board.add(board)
    followed_boards = Board.objects.filter(followers=user)
    board_topics = Topic.objects.filter(board__in=followed_boards).all()

    return render(request, 'forum/followed_boards.html', {'followed_boards': followed_boards, 'board_topics': board_topics})


@login_required()
def quote_post(request, post_id, topic_id):
    post = get_object_or_404(Post, pk=post_id)
    replies_desc = post.replies.all().reverse()
    topic = topic_id

    init_data = {
        'comment_text': post.message
    }
    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES)
        message = form.cleaned_data['message']
        files = request.FILES.getlist('files')

        if form.is_valid():

            post = Post.objects.create(
                message=message,
                last_updated=datetime.now()
                )
            post.save()
            
            for file in files:
                Attachment.objects.create(post=post, image=file)
 
        post_url = '{url}?page={page}#{id}'.format(
                url=post.get_absolute_url(),
                id=post.pk,
                page=topic.post.get_page_count()
            )  # reverse('post_detail', topic.pk, post_html_id)

        return redirect(post_url)
    else:
        form = QuoteForm(initial=init_data)

    return render(request, 'forum/quote_post.html', {'form': form, 'replies': replies_desc})

#  SH / FT / FB / L&S / MT / FG / FS 

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'forum/update_post.html'
    template_name_suffix = None
    form_class = PostUpdateForm


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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'forum/delete_post.html'
    template_name_suffix = None
    # success_url = reverse('topic/section_posts/')


class PostListView(ListView):
    # model = Post
    template_name = 'forum/posts_and_replies.html'
    context_object_name = 'post'
    paginate_by = 3

    def get_queryset(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])
        queryset = Post.objects.filter(topic=topic).order_by('-date_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_pk'])
        context['topic'] = topic

        # FOR TOPIC FOLLOW
        if topic.followers.filter(id=self.request.user.id).exists():
            context['follow_text'] = 'Unfollow'
        else:
            context['follow_text'] = 'Follow'

        #List of similar posts
        topic_tags_ids = topic.tags.values_list('id', flat=True)
        similar_posts = Topic.objects.filter(tags__in=topic_tags_ids).exclude(id=topic.id)
        context['similar_topics'] = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_created')[:6]

        for post in self.get_queryset():
            if post.totalikescount() == 0:
                # like_txt, likes_count = ' '
                context['like_txt'], context['likes_count'] = '', ''
            else:
                # like_txt, likes_count = 'Like', post.totallikescount()
                context['likes_count'], context['like_txt'] = post.totalikescount(), 'Like'

            if post.totalsharescount() == 0:
                context['share_txt'], context['shares_count'] = '', ''
            else:
                context['shares_count'], context['share_txt'] = post.totalsharescount(), 'Share'

        # FOR POST LIKE
            if post.liked_by.filter(id=self.request.user.id).exists():
                context['like_state'] = 'Unlike'
            else:
                context['like_state'] = 'Like'

        # FOR POST SHARE
            if post.shared_by.filter(id=self.request.user.id).exists():
                context['share_state'] = 'Un-Share'
            else:
                context['share_state'] = 'Share'
        return context


@login_required()
def like_dislike_post(request, id):
    userid = request.user.id
    user = request.user

    post = get_object_or_404(Post, pk=id)
    if post.liked_by.filter(id=userid).exists():
        post.liked_by.remove(user)
        liked = 'false'
    else:
        post.liked_by.add(user)
        liked = 'true'
    
    return JsonResponse({'liked': liked})


@login_required()
def share_unshare_post(request, id):
    userid = request.user.id
    user = request.user

    post = get_object_or_404(Post, pk=id)
    if post.shared_by.filter(id=userid).exists():
        post.shared_by.remove(user)
        shared = 'false'
    else:
        post.shared_by.add(user)
        shared = 'true'
    
    return JsonResponse({'shared': shared})


@login_required()
def follow_unfollow_board(request, board_id):
    userid = request.user.id
    user = request.user
    board = get_object_or_404(Board, pk=board_id)
    if board.followers.filter(id=userid).exists():
        board.followers.remove(user)
        followed_board = 'false'
    else:
        board.followers.add(user)
        followed_board = 'true'
    return JsonResponse({'followed_board': followed_board})


@login_required()
def delete_file(request, file_id):
    file = get_object_or_404(Attachment, pk=file_id)
    os.remove(os.path.join(settings.MEDIA_ROOT, file.name))
    file.delete()
    delete_result = 'Deleted'

    return JsonResponse({'deleted': delete_result})


@login_required()
def follow_unfollow_topic(request, topic_id):
    # user_id = request.user.id
    user = request.user
    topic = get_object_or_404(Topic, pk=topic_id)
    if topic.followers.filter(user=user).exists():
        topic.followers.remove(user)
        followed_topic = 'true'
    else:
        topic.followers.add(user)
        followed_topic = 'false'
    return JsonResponse({'followed_topic': followed_topic})


def feed(request):
    pass

def search(request, q):
    query = request.GET.get('q') 

    if q:
        topic_vector = SearchVector('title')
        post_vector = SearchVector('message')

        query = SearchQuery(q)
        post_search_headline = SearchHeadline('message', 'query', start_sel='<span class="highlight">', stop_sel='</span>')
        topic_search_headline = SearchHeadline(
            'title', 'query', start_sel='<span class="highlight">', stop_sel='</span>')

        topic_results = Topic.objects.annotate(rank=SearchRank(topic_vector, query)).annotate(headline=topic_search_headline).filter(rank__gte=0.1).order_by('-rank')
        post_results = Post.objects.annotate(rank=SearchRank(post_vector, query)).annotate(headline=post_search_headline).filter(rank__gte=0.2).order_by('-rank')
        results = list(chain(topic_results, post_results))
        # results = topic_results.union(post_results, all=True)
        for result in results:
            print(results)

    # result = Post.objects.filter(
    #     Q(topic__title__icontains=query) | Q(message__icontains=query)
    # )
    return render(request, 'forum/search.html',
                  context={'search_result': results})

@login_required()
def reply_post(request, pk):
    pass


@login_required()
def reply_topic(request, topic_pk):
    topic = get_object_or_404(Topic, topic_pk=topic_pk)
    replies_desc = topic.post_replies.all().reverse()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        message = form.cleaned_data['message']
        files = request.FILES.getlist('files')

        if form.is_valid():
            post = Post.objects.create(
                created_by=request.user,
                message=message,
                last_updated=datetime.now(),
                topic=topic)
            post.save()
            
            topic.last_updated = datetime.now()
            topic.post_count = F('post_count')+1
            topic.save()
            
            for file in files:
                Attachment.objects.create(post=post, image=file)
 
        post_url = '{url}?page={page}#{id}'.format(
                url=post.get_absolute_url(),
                id=post.pk,
                page=request.Get.get('page')
            )  

        return redirect(post_url)

    else:
        form = PostForm()
    # reply_context =
    return render(request, 'forum/reply_topic.html', {'form': form, 'topic': topic, 'replies': replies_desc})








