""" 
Creating custom mixing for use with create.
Need to complete.
"""

from django import forms
from django.forms.utils import ErrorList

class UserNeededMixin(object):
    def form_valid(self, form):
        # Below checks to make sure user exists 
        if self.request.user.is_authenticated:
            print("there is a user")
            form.instance.creator = self.request.user
            return super(UserNeededMixin, self).form_valid(form)
        else:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([ "User must be logged in to continue."])
            return self.form_invalid(form)