from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

import uuid

from .validators.validation_errors import clean_text

# Create your models here.

# Updating manager for message object to allow reference to self in retweet
class MessageManager(models.Manager):
    def retweet(self, creator, parent_obj):
        if primary_key.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

        obj = self.model(
            parent = og_parent, 
            creator = user, 
            text = parent_obj.text
        )
        obj.save()
        return obj

class Message(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True, on_delete = models.CASCADE)

    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    text = models.CharField(max_length=100, validators=[clean_text])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete = models.CASCADE, default=1)

    objects = MessageManager()

    class Meta:
        ordering = ["-created_at",]

    def __str__(self):
        return "Text content is {}".format(self.text)

    def get_absolute_url(self):
        return reverse("detail", args=(self.id,))

    
