from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404

from accounts.api.serializers import UserDisplaySerializer


# Create your views here.
class UserDetailView(DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    # queryset = User.objects.all()

    # Built in function to match against url kwargs
    def get_object(self):
        return get_object_or_404(User, id__iexact=self.kwargs.get("id"))
