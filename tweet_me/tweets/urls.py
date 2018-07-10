from django.urls import path

from . import views
from .views import (
    HomeView, 
    DetailMessageView, 
    CreateMessageView, 
    UpdateMessageView, 
    DeleteMessageView, 
    ListMessageView, 
    RegisterView, 
    LoginView, 
)

urlpatterns = [

    path("", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),

    # Base Message CRUD Views
    path("home/", HomeView.as_view(), name="home"),
    path("create", CreateMessageView.as_view(), name="create"), 
    path("detail/<uuid:pk>", DetailMessageView.as_view(), name="detail"),
    path("update/<uuid:pk>", UpdateMessageView.as_view(), name="update"),
    path("delete/<uuid:pk>", DeleteMessageView.as_view(), name="delete"),
    path("list/", ListMessageView.as_view(), name="list"),
]