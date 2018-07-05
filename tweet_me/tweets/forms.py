from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, HiddenInput, PasswordInput

from .models import Message


class MessageForm(ModelForm):
    # Creating form that leaves out creator.  Creator set in view logic 
    class Meta:
        model = Message
        fields = ["text",]
        widgets = {
            "text": TextInput(attrs = {
                "class": "form-control"
            }), 
        }


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta: 
        model = User
        fields = ["username", "password"]
        help_texts = {
        'username': None,
        'password': None,
    }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, 
     widget = forms.TextInput)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
 