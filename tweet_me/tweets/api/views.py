from django.db.models import Q

from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from .serializers import MessageSerializer
from .pagination import StandardSetPagination
from ..models import Message


# Create API with built in permission class for commong condition. Additional validation beyond "LoginRequiredMixin"
class MessageCreateAPIView(CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = StandardSetPagination

    # Updating base get_queryset with search functionality
    def get_queryset(self, *args, **kwargs):
        """
            Base message set is the user's messges and those the user follows using django qs combination.
            Query set allows for search filtering based on user info.
        """

        # Variable to get query set of profiles user follows
        profiles_followed = self.request.user.profile.get_following()
        q_set1 = Message.objects.filter(creator__in = profiles_followed)
        q_set2 = Message.objects.filter(creator = self.request.user)
        q_set = (q_set1 | q_set2).distinct().order_by("-created_at")
        query = self.request.GET.get('q', None)
        
        if query is not None: 
            q_set = q_set.filter(
                Q(text__icontains = query) |
                Q(creator__username__icontains = query)
            )
        return q_set

