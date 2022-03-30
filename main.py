import logging
import os

import telebot

from config import BUTTON_CMDS
from extensions import ExchangeException
from utils import exchange_inputs, get_available_currencies, get_help, validate_input_data

bot = telebot.TeleBot(os.environ.get("TOKEN"))


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=["start", "help"])
def send_help(message: telebot.types.Message):
    logger.info(f"{message.from_user.username}: {message.text}")
    buttons = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_help = telebot.types.KeyboardButton(BUTTON_CMDS["help"])
    btn_currencies = telebot.types.KeyboardButton(BUTTON_CMDS["currencies"])
    buttons.row(btn_help, btn_currencies)

    hello_msg = get_help()
    bot.reply_to(message, hello_msg, reply_markup=buttons, parse_mode="markdown")


@bot.message_handler(commands=["currencies"])
def send_currency(message: telebot.types.Message):
    logger.info(f"{message.from_user.username}: {message.text}")
    available_currencies = get_available_currencies()
    bot.reply_to(message, available_currencies, parse_mode="markdown")


@bot.message_handler(content_types=["text"])
def main(message: telebot.types.Message):
    logger.info(f"{message.from_user.username}: {message.text}")
    if message.text == BUTTON_CMDS["help"]:
        reply_msg = get_help()
    elif message.text == BUTTON_CMDS["currencies"]:
        reply_msg = get_available_currencies()
    else:
        try:
            parsed_inputs = validate_input_data(message.text)
        except ExchangeException as exc:
            reply_msg = f"😢 ошибка\n{str(exc)}"
        except Exception as exc:
            reply_msg = f"😢 неизвестная ошибка\n{str(exc)}"
        else:
            reply_msg = exchange_inputs(*parsed_inputs)

    bot.reply_to(message, reply_msg, parse_mode="markdown")


bot.polling()
