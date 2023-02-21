
from django.urls import path

from . import views

urlpatterns = [
    path("<int:page>", views.index, name="index"),
    path("", views.index, name = "index_without_parameter"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path('profile/<str:username>/<int:page>', views.profile, name="profile"),
    path('profile/<str:username>', views.profile, name="profile_without_parameter"),
    path('follow/<str:username>', views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("following/<int:page>", views.following, name="following"),
    path('following', views.following, name="following_without_parameter"),

    # API urls
    path('post/<int:post_id>', views.post, name="post"),
    path('likes', views.like, name="like")
]
