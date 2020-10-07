import logging

from . import configs
from telegram.bot import Bot

logger = logging.getLogger(__name__)

CHAT_ID = 772974581
telegram_bot = Bot(configs.TELEGRAM_TOKEN)


def send_message(chat_id, text):
    return telegram_bot.send_message(chat_id, text)


def send_me(text):
    return telegram_bot.send_message(CHAT_ID, text)
