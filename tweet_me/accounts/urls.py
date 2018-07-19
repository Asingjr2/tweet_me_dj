from django.contrib import admin
from django.urls import path, include

from accounts.api.serializers import UserDisplaySerializer
from .views import UserDetailView, UserFollowView

app_name= "accounts"
urlpatterns = [
        path("profiles/<str:username>", UserDetailView.as_view(), name="user_detail"),
        path("follow/<str:username>", UserFollowView.as_view(), name="follow"),
]

