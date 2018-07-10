from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Message
from .forms import MessageForm, RegisterForm, LoginForm
from .mixins import UserNeededMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"


class DetailMessageView(DetailView):
    model = Message
    template_name = "tweets/message_detail.html"


class CreateMessageView(LoginRequiredMixin, CreateView): 
    model = Message
    form_class = MessageForm
    success_url = "/home"
    template_name_suffix = "_create"

    def form_valid(self, form):
        print("form looks good")
        form.instance.creator = self.request.user
        return super(CreateMessageView, self).form_valid(form)
        # Above method saves form and redirects same as below but with less code
        # self.object = form.save()
        # return redirect("/home")

    def form_invalid(self, form):
        """  Modifying built in function for invalid form entry plus setting message error. """
        print("something went wrong", form.non_field_errors) 
        if "text" in form.errors:
            messages.warning(self.request, 'Message must contain word "django" and be less than 100 characters')
        if form.errors:
            messages.warning(self.request, 'errors')
        return redirect("/create")


# Url returns data in same form as create and populates with tweet info
class UpdateMessageView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = "/home"
    template_name = "tweets/message_update.html"


class ListMessageView(ListView):
    model = Message
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_messages"] = Message.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        """
            Modifying queryset to pull any url parameters and then filter against current user messages only
        """
        qs = Message.objects.all()
        print(self.request.GET)
        query = self.request.GET.get('q', None)
        if query is not None: 
            qs = qs.filter(
                Q(text__icontains = query) |
                Q(creator__username__icontains = query)
            )
        return qs.filter(creator__id = str(self.request.user.id))
    

class DeleteMessageView(LoginRequiredMixin,DeleteView):
    model = Message 
    success_url = reverse_lazy("home")
    template_name_suffix = "_delete"


class RegisterView(View):
    form_class = RegisterForm
    template_name = "tweets/reg.html"

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        """ Overriding base post method to encrpyt user password and validate registration from data"""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            return redirect("/login")
        else:
            if 'username' in form.errors:
                messages.warning(request, 'Username does not meet requirements.  Please try again.')
            return redirect("/")


class LoginView(View):
    form_class = LoginForm
    template_name = "tweets/log.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form":form})
    
    def post(self, request):
        form = LoginForm()
        submitted_form = self.form_class(request.POST)
        if submitted_form.is_valid():
            try: 
                username = submitted_form.cleaned_data["username"]
                password = submitted_form.cleaned_data["password"]
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect("/home")
                else:
                    messages.warning(request, 'Username or password does not match our records')
                    return redirect("/login")
            except: 
                messages.warning(request, 'Username or password does not match our records')
                return render(request, self.template_name, {"form":form})
            

def logout_view(request):
    """ Clear session data. """
    logout(request)
    return redirect("/home")