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


@periodic_task(run_every=(crontab(minute='*/10')), name='update_rooms')
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
            print('user found AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa')
            if user.is_send and user.email:
                print('bot access ')
                bot = DjangoTelegramBot.get_bot()
                site_parser(bot, user.chat_id, rooms=rooms)


@periodic_task(run_every=(crontab(minute='*/59')), name='delete_rooms')
def delete_old_rooms():
    for room in Advert.objects.filter(~Q(link=''), link__isnull=False):
        response = requests.get(room.link)
        if response.status_code == 404:
            room.delete()
