
from django import forms

from accounts.models import Account

class SignupForm(forms.Form):
    class Meta:
        model = Account

    def signup(self, request, user):
        pass
