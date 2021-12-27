from django.urls import path, include

from .views import signup, UserUpdateView, profile_view, ViewTopics, ViewPosts, my_likes, my_shares, followers, following

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('account/update/', UserUpdateView.as_view, name='update_account'),
    path('myaccount/<username>', profile_view, name='profile_view'),
    path('topics/<username>', ViewTopics, name='view_topics'),
    path('posts/<username>', ViewPosts, name='view_posts'),
    path('<username>', followers, name='followers'),
    path('<username>', following, name='following'),

    # path('viewcomments/<username>', view_comments, name='comments'),
    path('mylikes/<username>', my_likes, name='my_likes'),
    path('myshares/<username>', my_shares, name='my_shares'),

]
