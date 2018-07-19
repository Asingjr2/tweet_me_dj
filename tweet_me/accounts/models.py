from django.db import models
from django.db.models.signals import post_save 
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# Can refactor later.  Good to update queryset to filter out/ exclude user
class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            # Built in filter functionality
            if self.instance:
                qs = qs.exclude(user = self.instance)
        except: 
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(owner=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else: 
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(owner=user)
        if created: 
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False
        

class UserProfile(models.Model):
    # Related name will bring you into user object
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "profile")
    # Following will bring you into user profile...and then you would move into "user" to get user attributes
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name = "followed_by" )

    objects = UserProfileManager()

    def __str__(self):
        return " Profile belongs to {}".format(self.owner.username)

    def get_following(self):
        users = self.following.all()
        return users.exclude(username= self.owner.username)



def save_user_receiver(sender, instance, created, *args, **kwargs):
    """
    Creates profile automatically using django signals and created object "instance"
    """
    print("profile created", instance)
    if created:
        new_profile = UserProfile.objects.get_or_create(owner=instance)

# Post save is a built in signal that sends messages once a "sender" is saved/created
post_save.connect(save_user_receiver, sender=User)

