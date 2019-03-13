# In the name of God

# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging

from telegram import ReplyKeyboardMarkup, Bot, LabeledPrice

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

from constants.messages import LogMessage

update_id = None
token = '1254471079:966a4cd79b0c28fca23e9d37fb1473243a3b9468'

# Enable logging
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

REG, PAYMENT = range(2)


def start(bot: Bot, update):
    reply_keyboard = [['register', 'Other']]
    update.message.reply_text(text="سلام به کلاس زبان خوش‌آمدید."
                              ,
                              reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
    return REG


def register(bot, update):
    user = update.message.from_user
    logger.info(LogMessage.register.format(user))

    bot.send_invoice(chat_id=update.message.chat_id, title="title", description="description", payload="payload",
                     provider_token="6221061212318796", start_parameter="", currency="IRR",
                     prices=[LabeledPrice('label1', 1000)])
    return PAYMENT


def handle_payment(bot, update):
    logger.info(LogMessage.payment.format(1000))
    user = update.message.from_user
    return 0


bot = Bot(token=token,
          base_url="https://tapi.bale.ai/",
          base_file_url="https://tapi.bale.ai/file/")
updater = Updater(bot=bot)

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        REG: [MessageHandler(filters=Filters.text, callback=register)],
        PAYMENT: [MessageHandler(filters=Filters.successful_payment, callback=handle_payment)],
    },

    fallbacks=[]
)

updater.dispatcher.add_handler(conversation_handler)

updater.start_polling(poll_interval=2)
updater.idle()
