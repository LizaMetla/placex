# Create your tasks here
from __future__ import absolute_import, unicode_literals

import os
import traceback

import requests
from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Q
from django_telegrambot.apps import DjangoTelegramBot

from rent.models import Advert, Settings
from rent.models import User
from placex.utils import site_parser, get_rooms

#туть ставим 2 минутки
@periodic_task(run_every=(crontab(minute='*/10')), name='update_rooms')
def update_rooms():
    setting = Settings.objects.all().first()
    if setting is None:
        setting = Settings.objects.create()
    print('pre_sent')
    if setting.is_sent:
        try:
            rooms = get_rooms()
        except:
            print(f'error while parsing {traceback.format_exc()}')
            rooms = []
        print('is_sent')
        new_rooms = site_parser(rooms=rooms)
        bot = DjangoTelegramBot.get_bot()
        for user in User.objects.filter(chat_id__isnull=False, is_send=True, email__isnull=False):
            print('bot access ')
            for advert in new_rooms:
                message_ = f'{advert.link} \n {advert.price} \n Адрес: {advert.address or "Не указан"}'
                user = User.objects.get(pk=user.pk)
                if (user.price_min or 0) <= float(advert.price) <= (user.price_max or 500):
                    bot.sendPhoto(user.chat_id, photo=advert.images.all().first().file)
                    bot.sendMessage(user.chat_id, text=message_)


@shared_task(name="tasks.send_site_room")
def send_site_room(room_id):
    setting = Settings.objects.all().first()
    if setting is None:
        setting = Settings.objects.create()
    print('pre_sent')
    if setting.is_sent:
        advert = Advert.objects.filter(pk=room_id).first()
        if not advert:
            return None
        bot = DjangoTelegramBot.get_bot()
        for user in User.objects.filter(chat_id__isnull=False, is_send=True, email__isnull=False):
            message_ = f'{advert.link}\n{advert.price} \nАдрес: {advert.address or "Не указан"}'
            user = User.objects.get(pk=user.pk)
            if (user.price_min or 0) <= float(advert.price) <= (user.price_max or 500):
                bot.sendPhoto(user.chat_id, photo=advert.images.all().first().file)
                bot.sendMessage(user.chat_id, text=message_)


@periodic_task(run_every=(crontab(minute='*/2')), name='check_new_users')
def check_new_users():
    setting = Settings.objects.all().first()
    if setting is None:
        setting = Settings.objects.create()
    for user in User.objects.filter(chat_id__isnull=False, is_send=True, email__isnull=False, is_new=True):
        if user.is_send and user.email:
            print('bot access ')
            bot = DjangoTelegramBot.get_bot()
            for advert in Advert.objects.filter(price__gte=(user.price_min or 0), price__lte=(user.price_max or 500)).order_by('-date_advert')[:15]:
                message_ = f'{advert.link} \n {advert.price} \n Адрес: {advert.address or "Не указан"}'
                bot.sendPhoto(user.chat_id, photo=advert.images.all().order_by('is_main').last().file)
                bot.sendMessage(user.chat_id, text=message_)
            user.is_new = False
            user.save()


@periodic_task(run_every=(crontab(minute='*/59')), name='delete_rooms')
def delete_old_rooms():
    with requests.Session() as s:
        for room in Advert.objects.filter(~Q(link=''), link__isnull=False):
            if 'localhost' in room.link:
                continue
            response = s.get(room.link)
            if response.status_code == 404:
                room.delete()
