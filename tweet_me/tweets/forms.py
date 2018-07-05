from django.forms import ModelForm, TextInput, HiddenInput

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