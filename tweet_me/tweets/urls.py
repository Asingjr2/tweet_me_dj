from django.urls import path

from . import views
from .views import (
    HomeView, 
    DetailMessageView, 
    CreateMessageView, 
    UpdateMessageView, 
    DeleteMessageView, 
    ListMessageView
)


urlpatterns = [
    # Base Message Views
    path("home", HomeView.as_view(), name="home"),
    path("create", CreateMessageView.as_view(), name="create"), 
    path("detail/<uuid:pk>", DetailMessageView.as_view(), name="detail"),
    path("update", UpdateMessageView.as_view(), name="update"),
    path("delete/<uuid:id>", DeleteMessageView.as_view(), name="delete"),
    path("list", ListMessageView.as_view(), name="list")
]