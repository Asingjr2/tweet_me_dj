from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

from rest_framework import serializers

user = get_user_model()


class UserDisplaySerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = user # same as equating to User
        fields = [
            "username", "id", "follower_count",
        ]

    # Custom method for api.  Similar to avg views for an item or rating, etc.  Requires 'get' in front of method name
    def get_follower_count(self, obj):
        return 15
