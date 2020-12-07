# Create your tasks here
from __future__ import absolute_import, unicode_literals

import os
import traceback

import requests
from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Q
from django_telegrambot.apps import DjangoTelegramBot

from rent.models import Advert, Settings
from rent.models import User
from placex.utils import site_parser, get_rooms_for_user


@periodic_task(run_every=(crontab(minute='*/20')), name='update_rooms')
def update_rooms():
    setting = Settings.objects.all().first()
    if setting is None:
        setting = Settings.objects.create()
    print('pre_sent')
    if setting.is_sent:
        try:
            rooms = get_rooms_for_user()
        except:
            print(f'error while parsing {traceback.format_exc()}')
            rooms = []
        print('is_sent')
        for user in User.objects.filter(chat_id__isnull=False, is_send=True, email__isnull=False):
            if user.is_send and user.email:
                print('bot access ')
                bot = DjangoTelegramBot.get_bot()
                site_parser(bot, user.chat_id, rooms=rooms)

@periodic_task(run_every=(crontab(minute='*/1')), name='check_new_users')
def update_rooms():
    setting = Settings.objects.all().first()
    if setting is None:
        setting = Settings.objects.create()
    for user in User.objects.filter(chat_id__isnull=False, is_send=True, email__isnull=False, is_new=True):
        if user.is_send and user.email:
            print('bot access ')
            bot = DjangoTelegramBot.get_bot()
            for advert in Advert.objects.all().order_by('-date_advert')[:15]:
                message_ = f'{advert.link} \n {advert.price} \n Адрес: {advert.address or "Не указан"}'
                if user.price_min or 0 <= float(advert.price) <= user.price_max or 500:
                    bot.sendPhoto(user.chat_id, photo=advert.images.all().order_by('is_main').last().file)
                    bot.sendMessage(user.chat_id, text=message_)
            user.is_new = False
            user.save()

@periodic_task(run_every=(crontab(minute='*/59')), name='delete_rooms')
def delete_old_rooms():
    for room in Advert.objects.filter(~Q(link=''), link__isnull=False):
        response = requests.get(room.link)
        if response.status_code == 404:
            room.delete()
