
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),


    # API Routes
    path("like", views.like, name="like"),
    path("editing_post", views.editing_post, name="editing_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("new_post", views.new_post, name="new_post"),
    path("follow", views.follow_button, name="follow_button"),
    path("profile/<int:userid>", views.profile, name="profile"),
    path("follow/<int:user_id>", views.follow, name="follow")
]
