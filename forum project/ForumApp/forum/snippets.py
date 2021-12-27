
# SNIPPET FOR PAGINATION IN VIEWS
# # paginator_section = Paginator(section, 20)
# # paginator_post = Paginator(posts, 20)
# # page = self.request.GET.get('page')
# # page_obj = paginator_section.get_page(page)
# # try:
# #     page_list = paginator_section.page(page)
# # except PageNotAnInteger:
# #     page_list = paginator_section.page(1)
# # except EmptyPage:
# #     page_list = paginator_section.page(paginator_section.num_pages)

# SNIPPET TO GET AND SET SESSION DATA IN VIEWS

# # also check- to set use request.session['Liked'] = context['liked']   
# # to get use fav_color = request.session['Liked'] or request.session.get('Liked', False)
# # or to delete 'del request.session['Liked']'= context['liked']

# PAGINATION in Template

                # {% if page_obj.has_previous %}
                # <a href="?page=1">&laquo; first </a><a href="?page={{page_obj.previous_page_number}}"> previous</a>
                # {% endif %}
                # <span class="current">PAGE {{page_obj.number}} of {{page_obj.paginator.num_pages}}.
                # </span>
                # {% if page_obj.has_next %}
                # <a href="?page={{page_obj.next_page_number}}">next </a><a href="?page={{page_obj.paginator.num_pages}}">
                #     last &raquo;</a>
                # {% endif %}



# #TOPIC DETAIL VIEW
# # class TopicDetailView(DetailView):
# #     model = Topic
# #     template_name = 'forum/posts_and_replies.html'
# #     template_name_suffix = None

# # #
# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         board = get_object_or_404(Board, pk=self.object.board.pk)
# #         posts = Post.objects.filter(topic=self.object)
# #         section = Board.objects.filter(pk=self.object.board.pk)
# #         print(section)
# #         paginator_section = Paginator(section, 20)
# #         paginator_post = Paginator(posts, 20)
# #         page = self.request.GET.get('page')
# #         page_obj = paginator_section.get_page(page)
# #         # try:
# #         #     page_list = paginator_section.page(page)
# #         # except PageNotAnInteger:
# #         #     page_list = paginator_section.page(1)
# #         # except EmptyPage:
# #         #     page_list = paginator_section.page(paginator_section.num_pages)
        


# #   # List of similar posts
# #     post_tags_ids = post.tags.values_list('id', flat=True)
# #     similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
# #     similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:6]

# #         for p in posts:
# #             post = get_object_or_404(Post, pk=p.id)

# #         if post.totalikescount == 0:
# #             # like_txt, likes_count = ' '
# #             context['like_txt'], context['likes_count'] = ' '
# #         else:
# #             # like_txt, likes_count = 'Like', post.totallikescount()
# #             context['likes_count'], context['like_txt'] = post.totalikescount(), 'Like' 

# #         if post.totalsharescount == 0:
# #             context['share_txt'], context['shares_count'] = None
# #         else:
# #             # share_txt, shares_count = 'Share', post.totalsharescount()
# #             context['shares_count'], context['share_txt'] = post.totalsharescount(), 'Share'

# #     # FOR POST LIKE
# #         if post.liked_by.filter(id=self.request.user.id).exists():
# #             context['liked'] = 'Unlike'
# #         else:
# #             context['liked'] = 'Like'
        

# #     # FOR POST SHARE   
# #         if post.shared_by.filter(id=self.request.user.id).exists():
# #             context['liked'] = 'Un-Share'
# #         else:
# #             context['liked'] = 'Share'




# # template Pagination
# # {# page_obj.paginator.page_range, page_obj.paginator.get_elided_page_range   #}


# BREADCRUMBS
# # <!-- <h2> {{topic.title|title}} - {{topic.board.name}} - Liberian Forum  </h2>
# # <p class="bold"><a href="{% url 'home' %}"> Liberian Forum </a> {% if topic.board.parent %}/ <a href="{% url 'section' 'topic.board.parent' %}"> {{topic.board.parent}}</a>{% endif %} / <a href="{% url 'section'  'topic.board.name '%}"> {{topic.board.name}}</a> / <a href="/{{topic.board}}"> -->

# TEMPLATE THREAD TOPIC SNIPPET


# # <!--  Topic Header--

# #         <tr>
# #             <td class="bold l pu" id="top">
# #                 <a href="#top"> {{topic.title}} </a> by <a href=" {% url 'profile_view' 'topic.created_by' %}"
# #                     class="user bold">
# #                     {{topic.created_by|lower}} </a>: <span class="s"> <b> {{topic.date_created|date:"h:i a"}} </b> On
# #                     <b>
# #                         {{topic.date_created|date:"jS b"}} </b></span>
# #             </td>
# #         </tr>



# #         <tr>
# #             <!--Topic Body or Content--
# #             <td class="l w pd">
# #                 <div class="narrow">
# #                     <p> {{topic.post.message.first}} </p>
# #                 </div>

# #                 <p class="s"> (<a href="{% url 'quote_post' topic.post.id %}">Quote</a>)

# #                     (<a href=" {% url 'report_post' topic.post.id %}">Report</a>)

# #                     <span class='s' id='likescount' style='font-weight:bold;'>{{post.totalikescount}}
# #                         Like{{post.totalikescount|pluralize:'s'}}</span> <span class='s' id='liketext'
# #                         style='font-weight:bold;'>Like{{post.totalikescount|pluralize:'s'}}
# #                     </span> (<a id='postlike' href="{% url 'post_like' post.id  %}">{{like_state}} </a>)

# #                     <span class='s' id='sharescount' style='font-weight:bold;'>{{post.totalsharescount}}
# #                     </span><span class='s' id='sharetext'
# #                         style='font-weight:bold;'>Share{{post.totalsharescount|pluralize:'s'}}
# #                     </span> (<a id='postshare' href="{% url 'post_share' post.id  %}">{{share_state}} </a>)

# #                 </p>
# #                 {% if post.attachment %}
# #                 {% for image in post.attachment %}
# #                 <p> <img style="max-width:700px;" class="attachmentimage img" src="{{image.url}}" /> an Image </p>
# #                 {% endfor  %}

# #                 {% endif %}

# #             </td>
# #         </tr> -->
