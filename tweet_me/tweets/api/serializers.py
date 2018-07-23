from django.utils.timesince import timesince

from rest_framework import serializers

from tweets.models import Message
from accounts.api.serializers import UserDisplaySerializer


# Creating serializer that references User serializer so all related dated is pulled at once
class MessageSerializer(serializers.ModelSerializer):
    creator = UserDisplaySerializer(read_only=True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id", "text", "created_at", "updated_at", "creator", "timesince", "date_display"
        ]
    
    def get_date_display(self, obj):
        return obj.created_at.strftime("%b %d %I: %M %p")

    # Built in function
    def get_timesince(self, obj):
        return timesince(obj.created_at) + " ago "

