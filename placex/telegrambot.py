import logging
import re

from django.core.validators import validate_email
from django_telegrambot.apps import DjangoTelegramBot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from placex.settings import SEARCH_KEYS
from placex.utils import get_keys_from_message, set_keys_on_user
from rent.models import User
from placex.settings_common import PARSERS, ADMIN_EMAILS

HELP_BUTTON_CALLBACK_DATA = 'help'
help_button = InlineKeyboardButton(
    text='Help me',  # text that show to user
    callback_data=HELP_BUTTON_CALLBACK_DATA  # text that send to bot when user tap button
)

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
        context.bot.send_message(chat_id,
                                 'Пожалуйста, введите свой email. \nОн нужен для вашей идентификации в системе и не будет использоваться для спама.')
    else:
        context.bot.send_message(chat_id, 'Добро пожаловать! Для подробной инструкции по ' \
                                          'по управлению нажмите /help',
                                 reply_markup=InlineKeyboardMarkup([[help_button]]))
        context.bot.send_message(chat_id, 'Вы можете задать параметры поиска квартир ниже:',
                                 reply_markup=main_menu_keyboard())


def _help(bot, context):
    chat_id = bot.callback_query.message.chat.id
    message = 'Этот бот позволяет искать объявления об аренде квартир/комнат и слать уведомления о новых ' \
              'объявлениях. \n' \
              'Для установки диапазона цен войдите в меню и нажмите "Указать цену!"'
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
        if user_in_site and user_in_site != user:
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
                                                   'Для более подробной информации нажмите кнопку ниже \n' \
                                                    'Для завершения работы нажмите /stop', reply_markup=InlineKeyboardMarkup([[help_button]]))
            context.bot.send_message(chat_id, 'Вы можете задать параметры поиска квартир ниже:',
                                     reply_markup=main_menu_keyboard())
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
            context.bot.send_message(chat_id,
                                     text=f'{user.name}, спасибо, что связали бота с профилем placex.\nТеперь Вы можете выполнить настройку бота через /help или из профиля placex')
        else:
            if bot.message.text == 'Указать цену!':
                context.bot.send_message(chat_id, text='Установка цены для арендной квартиры:',
                                         reply_markup=cost_menu_keyboard())
            elif bot.message.text =='Остановить поиск :(':
                stop(bot, context)
            else:
                context.bot.send_message(chat_id, text=bot.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def stop(bot, context):
    chat_id = bot.message.chat.id
    user = User.objects.get(chat_id=chat_id)
    user.is_send = False
    user.is_new = True
    user.save()
    message = 'Вы отписались от обновлений, для возобновления нашего общения введите /start'
    context.bot.send_message(chat_id, text=message)


def set_max_price(bot, context, price):
    chat_id = bot.callback_query.message.chat.id
    user = User.objects.get(chat_id=chat_id)
    user.price_max = price
    user.save()
    context.bot.send_message(chat_id, text=f'Установлена максимальная цена в {price}$')


def set_min_price(bot, context, price):
    chat_id = bot.callback_query.message.chat.id
    user = User.objects.get(chat_id=chat_id)
    user.price_min = price
    user.save()
    context.bot.send_message(chat_id, text=f'Установлена минимальная цена в {price}$')


def callback_query_handler(bot, update):
    cqd = bot.callback_query.data
    # message_id = update.callback_query.message.message_id
    # update_id = update.update_id
    if cqd == HELP_BUTTON_CALLBACK_DATA:
        _help(bot, update)
    elif cqd == 'm1':
        set_max_price(bot, update, 300)
    elif cqd == 'm2':
        set_max_price(bot, update, 400)
    elif cqd == 'm3':
        set_max_price(bot, update, 510)
    elif cqd == 'm4':
        set_max_price(bot, update, 1000)
    elif cqd == 'm5':
        set_min_price(bot, update, 0)
    elif cqd == 'm6':
        set_min_price(bot, update, 100)
    elif cqd == 'm7':
        set_min_price(bot, update, 300)
    elif cqd == 'm8':
        set_min_price(bot, update, 450)


def main_menu_message():
    return 'Пожалуйста, укажите цену в USD!'


def cost_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('От 0$', callback_data='m5'), InlineKeyboardButton('До 300$', callback_data='m1')],
        [InlineKeyboardButton('От 100$', callback_data='m6'), InlineKeyboardButton('До 400$', callback_data='m2')],
        [InlineKeyboardButton('От 300$', callback_data='m7'), InlineKeyboardButton('До 510$', callback_data='m3')],
        [InlineKeyboardButton('От 450$', callback_data='m8'), InlineKeyboardButton('До 1000$', callback_data='m4')],
        ]
    return InlineKeyboardMarkup(keyboard)


def main_menu_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton('Указать цену!', callback_data='cost_menu'), KeyboardButton('Остановить поиск :(')]], resize_keyboard=True,
                               one_time_keyboard=False)


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CallbackQueryHandler(callback_query_handler))
    # log all errors
    dp.add_error_handler(error)
