import logging
import re

from django.core.validators import validate_email
from django_telegrambot.apps import DjangoTelegramBot
from telegram.ext import CommandHandler, MessageHandler, Filters

from placex.settings import SEARCH_KEYS
from placex.utils import get_keys_from_message, set_keys_on_user
from rent.models import User
from placex.settings_common import PARSERS, ADMIN_EMAILS


logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, context):
    chat_id = bot.message.chat.id
    user, created = User.objects.get_or_create(chat_id=chat_id)
    if created:
        user.is_new = True
    user.name = bot.message.chat.first_name or 'Неопознанный' + '' + bot.message.chat.last_name or 'клиент'
    user.save()
    if not user.is_send:
        user.is_send = True
        user.save()
    if not user.email:
        context.bot.send_message(chat_id, 'Пожалуйста, введите свой email. \nОн нужен для вашей идентификации в системе и не будет использоваться для спама.')
    else:
        context.bot.send_message(chat_id, 'Добро пожаловать! Для подробной инструкции по ' \
                                                             'по управлению нажмите /help')


def _help(bot, context):
    chat_id = bot.message.chat.id
    message = 'Этот бот позволяет искать объявления об аренде квартир/комнат и слать уведомления о новых ' \
              'объявлениях. \n' \
              'Введите следуюшие свойства квартиры: \n' \
              'max=< Максимальная цена в USD, по умолчанию 500$ > \n ' \
              'min=< Минимальная цена в USD, по умолчанию 0$ > \n'
    context.bot.send_message(chat_id, text=message)


def echo(bot, context):
    # logger.info(str(dir(context.update)))
    chat_id = bot.message.chat.id

    user, created = User.objects.get_or_create(chat_id=chat_id)
    if created:
        user.is_new = True
    if not user.name:
        user.name = bot.message.chat.first_name or 'Неопознанный' + '' + bot.message.chat.last_name or 'клиент'
    user.save()
    is_permissions = True
    search_res = re.search(r'<placex>.+</placex>', bot.message.text)
    if search_res:
        code = search_res.group(0)
        code = code.replace('<placex>', '').replace('</placex>', '')
        user_in_site = User.objects.filter(attachment_code=code).first()
        if user_in_site and user_in_site!=user:
            user_in_site.chat_id = user.chat_id
            user_in_site.price_max = user.price_max
            user_in_site.price_min = user.price_min
            user_in_site.is_send = user.is_send
            user_in_site.is_onliner = user.is_onliner
            user_in_site.is_kufar = user.is_kufar
            user_in_site.save()
            user.delete()
            user = user_in_site

    if not user.is_send:
        is_permissions = False
        context.bot.send_message(chat_id, text='Пожалуйста, введите /start. \n' \
                                                             'Это необходимо для запуска бота')
    elif not user.email:
        try:
            validate_email(bot.message.text)
            user.email = bot.message.text
            user.save()
            # if user.email in ADMIN_EMAILS:
            user.is_onliner = True
            user.is_kufar = True
            user.save()
            context.bot.send_message(chat_id, text='Спасибо 😘 \n' \
                                                                 'Теперь вы можете вводить параметры для поиска. \n' \
                                                                 'Для более подробной информации нажмите /help')
        except:
            is_permissions = False
            context.bot.send_message(chat_id, text='Пожалуйста, введите верный email. \n' \
                                                                 'Он нужен для вашей идентификации в системе и не будет использоваться для спама.')

    elif not any(getattr(user, permission, False) for permission in PARSERS) and is_permissions:
        is_permissions = False
        context.bot.send_message(chat_id, text='Извините, похоже у вас недостаточно прав для ' \
                                                             'использования данного сервиса. \n' \
                                                             'Для расширения прав доступа напишите мне на почту: \n' \
                                                             'domen699@gmail.com \n' \
                                                             'Спасибо 😉')

    elif is_permissions == True:
        if search_res:
            context.bot.send_message(chat_id, text=f'{user.name}, спасибо, что связали бота с профилем placex.\nТеперь Вы можете выполнить настройку бота через /help или из профиля placex')
        else:
            search_values = get_keys_from_message(bot.message.text.lower(), SEARCH_KEYS)
            user = User.objects.get(chat_id=chat_id)
            set_keys_on_user(user, search_values)
            context.bot.send_message(chat_id, text=bot.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def stop(bot, context):
    chat_id = bot.message.chat.id
    user = User.objects.get(chat_id=chat_id)
    user.is_send = False
    user.save()
    message = 'Вы отписались от обновлений, для возобновления нашего общения введите /start'
    context.bot.send_message(chat_id, text=message)


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(CommandHandler("stop", stop))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
