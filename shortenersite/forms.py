from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from shortenersite import models


class CustomerCreationForm(UserCreationForm):
    """
        The customer registration form
    """
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    user_category = forms.ChoiceField(choices=models.UserProfile.USER_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'user_category')