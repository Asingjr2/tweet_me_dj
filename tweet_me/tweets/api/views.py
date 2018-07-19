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

    # Replacing base get_queryset with search functionality
    # Not working the same as the full list
    def get_queryset(self, *args, **kwargs):
        """
            Modifying queryset to pull any url parameters and then filter against current user messages only.  Queryset allows for order.
        """
        q_set = Message.objects.all().order_by("-created_at")
        print(self.request.GET)
        query = self.request.GET.get('q', None)
        if query is not None: 
            q_set = q_set.filter(
                Q(text__icontains = query) |
                Q(creator__username__icontains = query)
            )
        return q_set.filter(creator__id = str(self.request.user.id))

