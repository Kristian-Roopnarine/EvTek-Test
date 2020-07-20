from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from .models import Address

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email','phone_number','account_type')

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('street','apt','state','zipcode','user')