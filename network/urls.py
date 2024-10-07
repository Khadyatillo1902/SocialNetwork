
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newPost', views.newPost, name='newPost'),
    path('following', views.following, name='following'),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('follow/<int:user_id>', views.follow, name='follow'),
    path('unfollow/<int:user_id>', views.unfollow, name='unfollow'),
    path('posts/<int:post_id>/like', views.like_post, name='like_post'),
    path('posts/<int:post_id>/edit', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/comment', views.comment, name='comment'),
]
