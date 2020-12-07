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
    search_fields = ('address', 'link')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'chat_id', 'name', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Fields', {'fields': ('chat_id', 'name', 'price_max', 'price_min', 'phone_number', 'is_agent', 'favorites', 'image', 'is_send',
                               'is_kufar', 'is_onliner', 'is_hata')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    autocomplete_fields = ('favorites', )

admin.site.register(User, CustomUserAdmin)