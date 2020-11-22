from django.contrib import admin

# Register your models here.
from rent.models import Advert, User, Image
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
admin.site.register(Advert)
admin.site.register(Image)



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username',]

admin.site.register(User, CustomUserAdmin)