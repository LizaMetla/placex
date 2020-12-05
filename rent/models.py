import os

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.dispatch import receiver


class User(AbstractUser):
    name = models.CharField(verbose_name='ФИО', max_length=50, null=True, blank=True)
    price_max = models.IntegerField(verbose_name='Максимальная цена', default=500, blank=True)
    price_min = models.IntegerField(verbose_name='Минимальная цена', default=0, blank=True)
    phone_number = models.CharField(verbose_name='Телефон', max_length=20, null=True, blank=True)
    is_agent = models.BooleanField(default=False)
    favorites = models.ManyToManyField('Advert', blank=True)
    image = models.ImageField(null=True, blank=True)
    is_send = models.BooleanField(default=True, blank=True)
    is_kufar = models.BooleanField(default=False, blank=True)
    is_onliner = models.BooleanField(default=True, blank=True)
    is_hata = models.BooleanField(default=False, blank=True)
    chat_id = models.CharField(max_length=50, blank=True, null=True)
class AdvertManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active_admin=True)

class Advert(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Владелец', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    address = models.CharField(verbose_name='Адрес', max_length=200, blank=True, null=True)
    city = models.CharField(verbose_name='Город', max_length=200, null=True, blank=True)
    price = models.FloatField(verbose_name='Цена')
    is_active_admin = models.BooleanField(default=False, verbose_name='Скрыть объявление у всех в выдаче?')
    is_active = models.BooleanField(default=True, verbose_name='Сделать видимым для всех пользователей?', blank=True)
    see_counter = models.IntegerField(default=0, blank=True)
    count_room = models.IntegerField(default=1)
    link = models.TextField(null=True, blank=True)
    is_agent = models.BooleanField(default=False)
    def __str__(self):
        return self.address
    class Meta:
        ordering = ['-date_created']
    def get_main_image(self):
        image = self.images.filter(is_main=True).first()
        if not image:
            image = self.images.all().first()
        return image


class Settings(models.Model):
    is_sent = models.BooleanField(default=True)


class Image(models.Model):
    file = models.ImageField(verbose_name='Изображения', null=True)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name="images", null=True)
    is_main = models.BooleanField(default=False)
    class Meta:
        ordering = ['-is_main']
    def __str__(self):
        return str(self.advert)
@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)