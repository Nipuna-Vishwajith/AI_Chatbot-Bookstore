import json
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import spacy
import re
import requests

# Telegram Bot Token
TOKEN = '5881058982:AAGJYI0beRW2Ke7xeJ89M_vUd5lHtjzUZUI'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
# Load menu and intents from JSON files
with open('menu.json', 'r') as menu_file:
    menu = json.load(menu_file)

with open('intents.json', 'r') as intents_file:
    intents = json.load(intents_file)["intents"]
# Command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    introduction = "Hello! I'm your Book Chatbot. I can help you with book recommendations, information about authors, and book orders.\n\n"\
                    "If you want to explore our book categories, just type 'book menu' or any related query."
    
    update.message.reply_text(introduction)

# Command handler for /book_menu
def book_menu(update: Update, context: CallbackContext) -> None:
    introduction = "We have books under the following categories only:\n\n"\
                    "1. Combined Maths\n"\
                    "2. Chemistry\n"\
                    "3. Physics\n"\
                    "4. Biology\n\n"\
                    "Please select a category by pressing the buttons from your keyboard."
    
    # Use ReplyKeyboardMarkup to provide category options
    category_buttons = [
        [KeyboardButton("1. Combined Maths"), KeyboardButton("2. Chemistry")],
        [KeyboardButton("3. Physics"), KeyboardButton("4. Biology")]
    ]
    reply_markup = ReplyKeyboardMarkup(category_buttons, one_time_keyboard=True)

    update.message.reply_text(introduction, reply_markup=reply_markup)

# Function to handle unknown queries
def unknown_query(update: Update) -> None:
    response = random.choice([
        "I'm sorry, but I couldn't understand that. Could you please rephrase?",
        "I didn't catch that. Could you please provide more clarity?"
    ])
    update.message.reply_text(response)



