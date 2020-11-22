from django.forms import ModelForm, forms

from rent.models import Advert
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = '__all__'
class RegistrationForm(forms.Form):
    pass