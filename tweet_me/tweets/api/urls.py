from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from .views import MessageListAPIView, MessageCreateAPIView

urlpatterns = [
    path("all_messages/", MessageListAPIView.as_view(), name="all_messages"),
    path("create/", MessageCreateAPIView.as_view(), name="message_creation"),
]
