# -*- coding: utf-8 -*-
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# app specific imports
import pandas as pd
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
telegram_token = str(os.environ.get('TELEGRAM_TOKEN'))

# defining Handlers
def start(bot, update):
    """ When /start is pressed - prompts user with brief introduction and ask to press GO! button """
    go_button = telegram.KeyboardButton(text="GO!")
    custom_keyboard = [[go_button]]
    chat_reply = "Hello hello! Want me to suggest food places for you? Press GO!"
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=chat_reply, reply_markup=reply_markup)

def respond(bot, update):
    """ When user sends any text response """
    def error_msg(): 
        go_recommend = telegram.KeyboardButton(text="GO!")
        custom_keyboard = [[go_recommend]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text="Aiyo paiseh got error LOL try again ok, just press GO!", reply_markup=reply_markup)
    

    if update.message.text == 'GO!': 
        try:
            locations = pd.read_csv('locations.csv', index_col=0)
            suggestion = random.choice(list(locations['0']))
            bot.send_message(chat_id=update.message.chat_id, text=suggestion)

            # prompt restaurante search
            ccp_button = telegram.KeyboardButton(text="Changi City Point")
            custom_keyboard = [[ccp_button]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
            bot.send_message(chat_id=update.message.chat_id, text="Click the below if you want me to suggest a restaurant in the location, or any other location!", reply_markup=reply_markup)
    
        except:
            error_msg()

    elif update.message.text == 'Changi City Point': 
        try:
            ccp_clean = pd.read_csv('ccp_clean.csv', index_col=0)
            suggestion = random.choice(list(ccp_clean['0']))
            bot.send_message(chat_id=update.message.chat_id, text=suggestion)
            bot.send_message(chat_id=update.message.chat_id, text="If you want another location recommendation, just press again - GO!")

            # prompt another GO!
            go_recommend = telegram.KeyboardButton(text="GO!")
            custom_keyboard = [[go_recommend]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
            chat_reply="If you want another recommendation, just press again - GO!"
            bot.send_message(chat_id=update.message.chat_id, text=chat_reply, reply_markup=reply_markup)
        except:
            error_msg()
    else:
        error_msg()

def helper_help(bot, update):
    """ If user sends /help command """
    bot.send_message(chat_id=update.message.chat_id, text="Type /start to start LOL")

def helper_unknown(bot, update):
    """ If user sends unknown command """
    bot.send_message(chat_id=update.message.chat_id, text="Sorry leh, I don't know that command. If you dunno got what command, just type / then everything will come out")

def helper_error(bot, update, error, logger):
    """ Log Errors """
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# define main function
def main():
    """ This is where the bot starts from! """

    updater = Updater(token=telegram_token)

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # define which handler to use on different commands to answer in Telegram
    start_handler = CommandHandler('start', start)
    dispatch.add_handler(start_handler)

    respond_handler = MessageHandler(Filters.text, respond)
    dispatch.add_handler(respond_handler)

    help_handler = CommandHandler('help', helper_help)
    dispatch.add_handler(help_handler)

    unknown_handler = MessageHandler(Filters.command, helper_unknown)
    dispatch.add_handler(unknown_handler)

    # log all errors
    dispatch.add_error_handler(helper_error)

    #PROD
    port_number = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen="0.0.0.0",
                          port=port_number,
                          url_path=telegram_token)
    updater.bot.setWebhook("https://foodsuggestsg.herokuapp.com/" + telegram_token)
    updater.idle()

if __name__ == '__main__':
    main()
