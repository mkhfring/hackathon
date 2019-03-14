# In the name of God

# !/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import Document
from telegram import ReplyKeyboardMarkup, Bot, LabeledPrice
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, RegexHandler

from english_class.config.config import BotConfig, InvoiceConfig
from english_class.constants.messages import LogMessage, ReplyMessage, start_btns, InvoiceData, enter_btns, \
    main_menu_btns
from english_class.constants.states import BotState
from english_class.database.models import UserQuiz, Quiz, User
from english_class.database.quires import add_user, get_all_not_sent_information, update_is_sent_status, \
    get_user_related_quiz, save_writing
from english_class.utils import get_logger

bot = Bot(token=BotConfig.token,
          base_url=BotConfig.base_url,
          base_file_url=BotConfig.base_file_url)
updater = Updater(bot=bot)
dispatcher = updater.dispatcher

logger = get_logger()


def start(bot, update):
    user = update.message.from_user
    reply_keyboard = [[btn for btn in start_btns]]
    if User.is_exist(user.id):
        reply_keyboard = [[btn for btn in main_menu_btns]]
        user = update.message.from_user
        bot.send_message(user.id, text=ReplyMessage.main_menu,
                         reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
        return BotState.selected_menu_option
    else:
        update.message.reply_text(text=ReplyMessage.start_message,
                                  reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
        return BotState.reg


def register(bot, update):
    user = update.message.from_user
    logger.info(LogMessage.register.format(user))

    bot.send_invoice(chat_id=update.message.chat_id, title=InvoiceData.title, description=InvoiceData.description,
                     payload="payload",
                     provider_token=InvoiceConfig.provider_token, start_parameter="", currency=InvoiceData.currency,
                     prices=[LabeledPrice('label1', InvoiceConfig.amount)])
    return BotState.pay


def handle_payment(bot, update):
    logger.info(LogMessage.payment.format(1000))
    user = update.message.from_user
    add_user(user.id)
    reply_keyboard = [[btn for btn in enter_btns]]
    bot.send_message(user.id, text=ReplyMessage.successful_reg,
                     reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return BotState.menu


def main_menu(bot, update):
    reply_keyboard = [[btn for btn in main_menu_btns]]
    user = update.message.from_user
    bot.send_message(user.id, text=ReplyMessage.main_menu, reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

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
                                               " send your certification.")
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
    from english_class.database.connect import session
    user = update.message.from_user
    user_quiz = session.query(UserQuiz).filter(UserQuiz.user_id == user.id).one_or_none()
    quiz_id = int()
    if not user_quiz:
        quiz_id = 1
    the_quiz = session.query(Quiz).filter(Quiz.id == quiz_id).one_or_none()
    quiz_id += 1
    user_quiz = UserQuiz(quiz_id=quiz_id, user_id=user.id)
    session.merge(user_quiz)
    # the_quiz = get_user_related_quiz(user.id)
    reply_keyboard = [[the_quiz.option_1, the_quiz.option_2, the_quiz.option_3, the_quiz.option_4]]
    question = the_quiz.question
    correct_answer = the_quiz.answer

    dispatcher.user_data['correct_answer'] = correct_answer

    bot.send_message(chat_id=user.id, text=question, reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))

    return BotState.check_quiz


def check_quiz(bot, update):
    user = update.message.from_user

    user_answer = update.message.text

    correct_answer = dispatcher.user_data['correct_answer']
    # reply_keybord = ['next question', 'main menu']

    if user_answer == correct_answer:
        message = ReplyMessage.correct_answer
    else:
        message = ReplyMessage.wrong_answer

    bot.send_message(chat_id=user.id, text=message)


def save_writing_file(bot, update):
    user = update.message.from_user
    save_writing(update.message.document, user.id)

    bot.send_message(chat_id=user.id, text="your essay has been saved, wait for review.")


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        BotState.reg: [MessageHandler(filters=Filters.text, callback=register)],
        BotState.pay: [MessageHandler(filters=Filters.text, callback=handle_payment)],
        BotState.menu: [RegexHandler(pattern='^' + enter_btns[0] + '$', callback=main_menu)],
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
