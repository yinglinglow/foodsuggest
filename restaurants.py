# app specific imports
import pandas as pd
import random
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class Location(object):
    def __init__(self, location_name, location_csv):
        self.location_name = None
        self.location_csv = None

    def suggest_restaurants(self):
        restaurant_database = pd.read_csv(self.location_csv, index_col=0)
        suggestion = random.choice(list(restaurant_database['name']))
        bot.send_message(chat_id=update.message.chat_id, text=f"We should eat at... {suggestion}!!")

        another_restaurant_button = telegram.KeyboardButton(text=f"Suggest another restaurant in {self.location_name}")
        location_button = telegram.KeyboardButton(text="Suggest a location")
        all_location_button = telegram.KeyboardButton(text="See all locations")
        custom_keyboard = [[another_restaurant_button], [location_button], [all_location_button]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text="Let me know if you want another restaurant recommendation... or another location recommendation!", reply_markup=reply_markup)

