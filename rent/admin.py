from django.contrib import admin

# Register your models here.
from rent.models import Advert, User, Image

admin.site.register(Advert)
admin.site.register(User)
admin.site.register(Image)