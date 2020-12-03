import re
import traceback
from io import BytesIO
from uuid import uuid4

import requests

from rent.models import User, Advert, Settings, Image
from placex.settings_common import PARSERS
from placex.settings import SEARCH_KEYS


def get_keys_from_message(message: str, search_keys: dict) -> dict:
    response_keys = {}
    for model_key, re_rey in search_keys.items():
        search_result = re.search(re_rey, message)
        if search_result:
            search_result = search_result.group(0)
        if search_result:
            response_keys.update({model_key: search_result.split('=')[1]})
    return response_keys


def set_keys_on_user(user, search_values):
    for key, value in search_values.items():
        if hasattr(user, key):
            setattr(user, key, value)
    user.save()


def get_rooms_for_user(user):
    rooms = []
    for key, parser_func in PARSERS.items():
        if hasattr(user, key) and getattr(user, key):
            rooms.extend(parser_func(user))
    return rooms


def get_or_create_send_setting():
    setting = Settings.objects.all().first()
    if setting is None:
        setting = Settings.objects.create()
    return setting


def is_sent_notify_gen():
    while True:
        setting = get_or_create_send_setting()
        yield setting.is_sent

import re

def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return 'file.png'
    return fname[0]
def site_parser(bot, chat_id, message=''):
    if not User.objects.filter(chat_id=chat_id):
        print('bot not found')
        bot.sendMessage(chat_id=chat_id, text=message)
    else:
        search_values = get_keys_from_message(message, SEARCH_KEYS)
        user = User.objects.get(chat_id=chat_id)
        set_keys_on_user(user, search_values)
        try:
            rooms = get_rooms_for_user(user)
        except:
            print(f'error while parsing {traceback.format_exc()}')
            rooms = []
        for room in rooms:
            room_link = room.get('link')

            if not Advert.objects.filter(owner=user, link=room_link):
                image = room.pop('image')
                image_obj = None
                if image:
                    response = requests.get(url=image)
                    if response.status_code == 200:
                        file = response.content
                        filename = uuid4().hex + '.jpeg'
                        image_obj = Image.objects.create()
                        image_obj.file.save(filename, BytesIO(file))
                        image_obj.save()
                room = Advert.objects.create(**room)
                room.link = room_link
                room.save()
                if image_obj:
                    image_obj.advert = room
                    image_obj.save()
                room.user = user
                room.save()
                message_ = f'{room.link} \n {room.price} \n Адрес: {room.address or "Не указан"}'
                bot.sendPhoto(chat_id, photo=room.images.all().first().file)
                bot.sendMessage(chat_id, text=message_)
