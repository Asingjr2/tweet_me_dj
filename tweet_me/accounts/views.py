from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404, redirect

from accounts.api.serializers import UserDisplaySerializer

from .models import UserProfile, UserProfileManager


# Create your views here.
class UserDetailView(DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    queryset = User.objects.all()

    # Built in function to match against url kwargs
    def get_object(self):
        return get_object_or_404(User, username__iexact=self.kwargs.get("username"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['following'] = UserProfile.objects.is_following(self.request.user, self.get_object())
        return context


# Refactor later to use generic views
class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated:
           is_following = UserProfile.objects.toggle_follow( request.user, toggle_user)
        return redirect("accounts:user_detail", username = username )

        # toggle_user = get_object_or_404(User, username__iexact=username)
        # if request.user.is_authenticated is not None:
        #     print("user is real")
        #     user_profile, created = UserProfile.objects.get_or_create(owner = request.user)
        #     if toggle_user in user_profile.following.all():
        #         user_profile.following.remove(toggle_user)
        #     else:
        #         user_profile.following.add(toggle_user)
        # return redirect("accounts:user_detail", username = username )

