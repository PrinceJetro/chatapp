from .views import *
from django.urls import path

urlpatterns = [
    path('', register, name='register'),
    path("register", register, name="register"),
    path("avatar/<str:pk>", Avatar, name="avatar"),
    path("login", login, name="login"),
    path("home", home, name="home"),
    path("room/<str:pk>", chatroom, name="chatroom"),
    path("profile/<str:pk>", userProfile, name="userprofile"),
    path("create-room", createRoom, name="create-room"),
    path("delete-room/<str:pk>", deleteRoom, name="delete-room"),
    path("delete-message/<str:pk>", deleteMessage, name="delete-message"),
    #path("chat/<str:username>/", chatroom, name="chatroom"),
    #path("chat/<str:username>/getmessage", getMessage, name="getmessage"),
    path("logout", logout_request, name="logout"),
]
