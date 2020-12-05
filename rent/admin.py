from django.contrib import admin

# Register your models here.
from rent.models import Advert, User, Image
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ('address', 'price', 'link')

admin.site.register(Image)



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'chat_id', 'name', 'is_active']

admin.site.register(User, CustomUserAdmin)