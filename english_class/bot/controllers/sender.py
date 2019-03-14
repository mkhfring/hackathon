# In the name of God

# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging

from telegram import Document
from telegram import ReplyKeyboardMarkup, Bot, LabeledPrice
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, RegexHandler

from english_class.constants.messages import LogMessage
from english_class.constants.states import BotState
from english_class.database.quires import add_user, get_all_not_sent_information, update_is_sent_status, \
    get_user_related_quiz

update_id = None
token = '1254471079:966a4cd79b0c28fca23e9d37fb1473243a3b9468'
bot = Bot(token=token,
          base_url="https://tapi.bale.ai/",
          base_file_url="https://tapi.bale.ai/file/")
updater = Updater(bot=bot)
dispatcher = updater.dispatcher

# Enable logging
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def start(bot: Bot, update):
    reply_keyboard = [['register', 'Other']]
    update.message.reply_text(text="سلام به کلاس زبان خوش‌آمدید."
                              ,
                              reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
    return BotState.reg


def register(bot, update):
    user = update.message.from_user
    logger.info(LogMessage.register.format(user))

    bot.send_invoice(chat_id=update.message.chat_id, title="title", description="description", payload="payload",
                     provider_token="6221061212318796", start_parameter="", currency="IRR",
                     prices=[LabeledPrice('label1', 1000)])
    return BotState.pay


def handle_payment(bot, update):
    logger.info(LogMessage.payment.format(1000))
    user = update.message.from_user
    add_user(user.id)
    reply_keyboard = [['Enter to class 😋']]
    bot.send_message(user.id, text="You have registered successfully.",
                     reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return BotState.menu


def main_menu(bot, update):
    reply_keyboard = [['show lesson', 'send writing essay', 'take a quiz']]
    user = update.message.from_user
    bot.send_message(user.id, text="choose one option:", reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return BotState.selected_menu_option


def show_information(bot: Bot, update):
    user = update.message.from_user
    file = get_all_not_sent_information()
    if file:
        file_id = file.file_id
        doc = Document(file_id=file_id)
        try:
            bot.send_document(user.id, document=doc)
            update_is_sent_status(file_id)

            reply_keyboard = [['next information', 'main menu']]
            bot.send_message(user.id, text='choose one option',
                             reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

            return BotState.next_information

        except BadRequest:
            logger.info(LogMessage.bot_send_message_error)

    else:
        bot.send_message(chat_id=user.id, text="You have finished the course please send your location, so that we can"
                                               "send your certification.(we have to call this api to get more scores:))")
        return BotState.get_location


def get_location(bot, update):
    user = update.message.from_user
    bot.send_message(chat_id=user.id, text="Dear *user* \nWe have to call this api to get more *scores*:)\n"
                                           "Sorry your location will not save in our database.\nBye")


def get_writing(bot, update):
    user = update.message.from_user
    bot.send_message(chat_id=user.id, text='Please send your writing essay')
    return BotState.save_writing


def take_quiz(bot, update):
    user = update.message.from_user
    quiz = get_user_related_quiz(user.id)

    reply_keyboard = [[quiz.option_1, quiz.option_2, quiz.option_3, quiz.option_4]]
    question = quiz.question
    correct_answer = quiz.answer

    dispatcher.user_data['correct_answer'] = correct_answer

    bot.send_message(text=question, eply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return BotState.check_quiz


def check_quiz(bot, update):
    user_answer = update.message.text

    correct_answer = dispatcher.user_data['correct_answer']

    if user_answer == correct_answer:
        return BotState.correct_ans
    else:
        return BotState.wrong_ans


def save_writing_file(bot, update):
    user = update.message.from_user
    save_writing_file(update.message.document, user)

    bot.send_message(user.id, text="your essay has been saved, wait for review.")


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        BotState.reg: [MessageHandler(filters=Filters.text, callback=register)],
        BotState.pay: [MessageHandler(filters=Filters.text, callback=handle_payment)],
        BotState.menu: [RegexHandler(pattern='^Enter to class 😋$', callback=main_menu)],
        BotState.selected_menu_option: [
            RegexHandler(pattern='^show lesson$', callback=show_information),
            RegexHandler(pattern='^send writing essay$', callback=get_writing),
            RegexHandler(pattern='^take quiz$', callback=take_quiz),
        ],
        BotState.next_information: [
            RegexHandler(pattern='^main menu$', callback=main_menu),
            RegexHandler(pattern='^next information', callback=show_information)
        ],
        BotState.get_location: [MessageHandler(filters=Filters.location, callback=get_location)],
        BotState.save_writing: [MessageHandler(filters=Filters.document, callback=save_writing_file)],
        BotState.check_quiz: [MessageHandler(filters=Filters.text, callback=check_quiz)]

    },

    fallbacks=[]
)

updater.dispatcher.add_handler(conversation_handler)

updater.start_polling(poll_interval=0.5)
updater.idle()
