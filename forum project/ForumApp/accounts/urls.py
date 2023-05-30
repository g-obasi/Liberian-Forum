from django.urls import path, include

from .views import signup, UserUpdateView, profile_view, ViewTopics, ViewPosts, likes_and_shares,followers_and_followings

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update_account'),
    path('my_account/<username>', profile_view, name='profile_view'),
    path('topics/<username>', ViewTopics.as_view(), name='view_topics'),
    path('posts/<username>', ViewPosts.as_view(), name='view_posts'),
    path('<username>', followers_and_followings, name='followers'),
    path('likes-shares/', likes_and_shares, name='likes_and_shares'),

    # path('viewcomments/<username>', view_comments, name='comments'),
    # path('mylikes/<username>', my_likes, name='my_likes'),
    # path('myshares/<username>', my_shares, name='my_shares'),

]
