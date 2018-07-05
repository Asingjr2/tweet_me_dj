from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .models import Message
from .forms import MessageForm

# Create your views here.


class HomeView(TemplateView):
    template_name = "tweets/home.html"


class DetailMessageView(DetailView):
    model = Message
    template_name = "tweet/message_detail.html"


class CreateMessageView(CreateView): 
    model = Message
    form_class = MessageForm
    success_url = "/home"
    template_name_suffix = "_create"

    def form_valid(self, form):
        print("form looks good")
        form.instance.creator = self.request.user
        self.object = form.save()
        return redirect("/home")

    def form_invalid(self, form):
        # Specific logic for invalid form entry plus setting message error
        print("something went wrong", form.errors) 
        if "text" in form.errors:
            messages.warning(self.request, 'Message must contain word "django" and be less than 100 characters')
        return redirect("/create")


class UpdateMessageView(UpdateView):
    model = Message
    template_name_suffix = "_update"


class ListMessageView(ListView):
    model = Message
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_messages"] = Message.objects.all()
        return context


class DeleteMessageView(DeleteView):
    model = Message 
    success_url = reverse_lazy("home")


def logout(request):
    """ Clear session data. """
    logout(request)
    return redirect("/home")