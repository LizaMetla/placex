from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    name = models.CharField(verbose_name='ФИО', max_length=50)
    max_price = models.FloatField(verbose_name='Максимальная цена')
    min_price = models.FloatField(verbose_name='Минимальная цена')
    phone_number = models.CharField(verbose_name='Телефон', max_length=13)


class Advert(models.Model):
    description = models.TextField(verbose_name='Описание')
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    address = models.CharField(verbose_name='Адрес', max_length=200)
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return self.address


class Image(models.Model):
    file = models.FileField(verbose_name='Изображения')
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, related_name="images")
