import os

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from django.dispatch import receiver


class User(AbstractUser):
    name = models.CharField(verbose_name='ФИО', max_length=50, null=True, blank=True)
    max_price = models.FloatField(verbose_name='Максимальная цена', null=True, blank=True)
    min_price = models.FloatField(verbose_name='Минимальная цена', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Телефон', max_length=13, null=True, blank=True)


class Advert(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Владелец')
    description = models.TextField(verbose_name='Описание')
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    address = models.CharField(verbose_name='Адрес', max_length=200)
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return self.address

    def get_main_image(self):
        return self.images.filter(is_main=True).first()

@receiver(models.signals.post_delete, sender=Advert)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.source_file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)



class Image(models.Model):
    file = models.ImageField(verbose_name='Изображения')
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name="images")
    is_main = models.BooleanField(default=False)
    class Meta:
        ordering = ['-is_main']
    def __str__(self):
        return str(self.advert)
