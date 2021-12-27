from django.urls import path
from .views import index, BoardView,  PostListView, TopicCreateView, NewsList, FeaturedTopic, SectionTopic, TopicDeleteView, PostUpdateView, PostCreateView, PostDeleteView, search, like_dislike_post,  share_unshare_post, reply_topic, follow_unfollow_topic, delete_file, follow_unfollow_board, quote_post, followed_boards, followed_topics, new_posts, reply_post, RecentPostList, trending, following_people_post, ReportInnapropiatePost, likes_and_shares, mentions, feed

urlpatterns = [
    path('index', index, name='index'),
    path('', FeaturedTopic.as_view(), name='home'),
    path('news/', NewsList.as_view(), name='news'),
    path('board/', BoardView.as_view(), name='board_list'),
    path('feed/', feed, name='feed'),
    path('create-topic/<board>', TopicCreateView.as_view(), name='create_topic'),
    path('delete-topic/<int:pk>', TopicDeleteView.as_view(), name='delete_topic'),
    path('topics/<board_name>', SectionTopic.as_view(), name='section'),
    path('<int:topic_pk>/', PostListView.as_view(), name='thread_post_list'),
    path('likes-shares/', likes_and_shares, name='likes_and_shares'),

    path('create-post/<int:topic_pk>', PostCreateView.as_view(), name='new_post'),
    path('delete-post/<int:pk>', PostDeleteView.as_view(), name='delete_post'),
    path('update-post/<int:pk>', PostUpdateView.as_view(), name='update_post'),

    path('post/reply/<int:post_pk>', reply_post, name='reply_post'),
    path('reply-topic/<int:topic_pk>', reply_topic, name='reply_topic'),
    path('quote-post/<int:post_pk>', quote_post, name='quote_post'),

    path('report/<int:pk>', ReportInnapropiatePost, name='report_post'),

    path('news-feed/', following_people_post, name='shared_with_me'),
    path('delete-file/<int:pk>', delete_file, name='delete_file'),
    path('follow-topic/<int:topic_pk>', follow_unfollow_topic,
         name='follow_unfollow_topic'),
    path('follow-boards/<int:board_pk>', follow_unfollow_board,
         name='follow_unfollow_board'),

    path('followed-topics/', followed_topics, name='followed_topics'),
    path('followed-boards/', followed_boards, name='followed_boards'),
    path('recent-post', RecentPostList.as_view(), name='recent'),
    path('trending-topics', trending, name='trending'),
    path('new-topic', new_posts, name='new'),
    path('mention/', mentions, name='mentions'),


    path('like-post/<int:id>', like_dislike_post, name='post_like'),
    path('share-post<int:id>', share_unshare_post, name='post_share'),

    path('search/', search, name='search'),


]
