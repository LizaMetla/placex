import logging

from django.core.validators import validate_email
from django_telegrambot.apps import DjangoTelegramBot
from telegram.ext import CommandHandler, MessageHandler, Filters

from rent.models import User
from placex.settings_common import PARSERS, ADMIN_EMAILS
from placex.utils import site_parser

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, context):
    chat_id = bot.message.chat.id
    user, _ = User.objects.get_or_create(chat_id=chat_id)
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
              'max=< Максимальная цена в USD, по умолчанию 300$ > \n ' \
              'min=< Минимальная цена в USD, по умолчанию 100$ > \n'
    context.bot.send_message(chat_id, text=message)


def echo(bot, context):
    # logger.info(str(dir(context.update)))
    chat_id = bot.message.chat.id

    user, _ = User.objects.get_or_create(chat_id=chat_id)
    user.name = bot.message.chat.first_name or 'Неопознанный' + '' + bot.message.chat.last_name or 'клиент'
    user.save()
    is_permissions = True

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
        context.bot.send_message(bot, chat_id, bot.message.text)


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
