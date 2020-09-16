from django.db import models


# Create your models here.
class Advert(models.Model):
    description = models.TextField(verbose_name='Описание')
    date_created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    address = models.CharField(verbose_name='Адрес', max_length=200)

    def __str__(self):
        return self.address
