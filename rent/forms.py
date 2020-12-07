from django.forms import ModelForm, forms

from rent.models import Advert
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
class CustomUserAuthForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=100)

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'image', 'name', 'phone_number')
        field_classes = {'email': forms.EmailField}


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'email': forms.EmailField}



class AdvertForm(ModelForm):
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    class Meta:
        model = Advert
        exclude = ['owner','is_active_admin' ]
class RegistrationForm(forms.Form):
    pass

class SearchForm(forms.Form):
    cost_min = forms.IntegerField(required=False)
    cost_max = forms.IntegerField(required=False)
    is_owner = forms.BooleanField(required=False)