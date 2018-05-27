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
        location_button = telegram.KeyboardButton(text="Suggest a location")
        all_location_button = telegram.KeyboardButton(text="See all locations")
        custom_keyboard = [[location_button], [all_location_button]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text="Aiyo paiseh got error LOL try again can?", reply_markup=reply_markup)

    def suggest_location():
        locations = pd.read_csv('locations.csv', index_col=0)
        suggestion = random.choice(list(locations['name']))
        bot.send_message(chat_id=update.message.chat_id, text=f"We should go to... {suggestion}!!")
        return suggestion

    def next_step_prompt(suggestion):
        location_restaurant_button = telegram.KeyboardButton(text=f"Suggest a restaurant in {suggestion}")
        location_button = telegram.KeyboardButton(text="Suggest another location")
        all_location_button = telegram.KeyboardButton(text="See all locations")
        custom_keyboard = [[location_restaurant_button], [location_button], [all_location_button]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text="Do you want me to suggest a restaurant in this location? Suggest another location? You can also choose to see all locations!", reply_markup=reply_markup)

    def see_all_locations():
        ccp_button = telegram.KeyboardButton(text="Changi City Point")
        uebiz_button = telegram.KeyboardButton(text="UE BizHub")
        plaza8_button = telegram.KeyboardButton(text="Plaza 8")
        custom_keyboard = [[ccp_button], [uebiz_button], [plaza8_button]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text="Click the below if you want me to suggest a restaurant in the location, or any other locations!", reply_markup=reply_markup)

    # def suggest_ue_restaurants():
    #     uebizhub = pd.read_csv('uebizhub.csv', index_col=0)
    #     suggestion = random.choice(list(uebizhub['0']))
    #     bot.send_message(chat_id=update.message.chat_id, text=f"We should eat at... {suggestion}!!")

    #     another_restaurant_button = telegram.KeyboardButton(text="Suggest another restaurant in UE BizHub")
    #     location_button = telegram.KeyboardButton(text="Suggest a location")
    #     all_location_button = telegram.KeyboardButton(text="See all locations")
    #     custom_keyboard = [[another_restaurant_button], [location_button], [all_location_button]]
    #     reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    #     bot.send_message(chat_id=update.message.chat_id, text="Let me know if you want another restaurant recommendation... or another location recommendation!", reply_markup=reply_markup)

    # def suggest_plaza8_restaurants():
    #     plaza8 = pd.read_csv('plaza8.csv', index_col=0)
    #     suggestion = random.choice(list(plaza8['0']))
    #     bot.send_message(chat_id=update.message.chat_id, text=f"We should eat at... {suggestion}!!")

    #     another_restaurant_button = telegram.KeyboardButton(text="Suggest another restaurant in Plaza 8")
    #     location_button = telegram.KeyboardButton(text="Suggest a location")
    #     all_location_button = telegram.KeyboardButton(text="See all locations")
    #     custom_keyboard = [[another_restaurant_button], [location_button], [all_location_button]]
    #     reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
    #     bot.send_message(chat_id=update.message.chat_id, text="Let me know if you want another restaurant recommendation... or another location recommendation!", reply_markup=reply_markup)

    class Location(object):
        def __init__(self, location_name, location_csv):
            self.location_name = location_name
            self.location_csv = location_csv

        def suggest_restaurants(self):
            restaurant_database = pd.read_csv(self.location_csv, index_col=0)
            suggestion = random.choice(list(restaurant_database['name']))
            bot.send_message(chat_id=update.message.chat_id, text=f"We should eat at... {suggestion}!!")

            another_restaurant_button = telegram.KeyboardButton(text=f"Suggest another restaurant in {self.location_name}")
            location_button = telegram.KeyboardButton(text="Suggest another location")
            all_location_button = telegram.KeyboardButton(text="See all locations")
            custom_keyboard = [[another_restaurant_button], [location_button], [all_location_button]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
            bot.send_message(chat_id=update.message.chat_id, text="Let me know if you want another restaurant recommendation... or another location recommendation!", reply_markup=reply_markup)

    ccp = Location('Changi City Point', 'ccp.csv')
    ue = Location('UE BizHub', 'uebizhub.csv')
    plaza8 = Location('Plaza 8', 'plaza8.csv')

    if update.message.text == 'GO!': 
        suggestion = suggest_location()
        next_step_prompt(suggestion)

    elif 'Changi City Point' in update.message.text: 
        try: 
            ccp.suggest_restaurants()
        except:
            error_msg()

    elif 'UE BizHub' in update.message.text: 
        try:
            ue.suggest_restaurants()
        except:
            error_msg()

    elif 'Plaza 8' in update.message.text: 
        try:
            plaza8.suggest_restaurants()
        except:
            error_msg()

    elif update.message.text in ['Suggest a location', 'Suggest another location']:
        try:
            suggest_location()
            see_all_locations()
        except:
            error_msg()

    elif update.message.text == 'See all locations':
        try:
            see_all_locations()
        except:
            error_msg()

    else:
        error_msg()

def helper_help(bot, update):
    """ If user sends /help command """
    bot.send_message(chat_id=update.message.chat_id, text="Type /start to start LOL")

def helper_unknown(bot, update):
    """ If user sends unknown command """
    bot.send_message(chat_id=update.message.chat_id, text="Sorry leh, I don't know that command. If you don't know got what command, just type / then everything will come out")

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
