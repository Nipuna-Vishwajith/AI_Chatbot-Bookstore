import json
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load menu and intents from JSON files
with open('menu.json', 'r') as menu_file:
    menu = json.load(menu_file)

with open('intents.json', 'r') as intents_file:
    intents = json.load(intents_file)["intents"]

# Telegram Bot Token
TOKEN = '5881058982:AAGJYI0beRW2Ke7xeJ89M_vUd5lHtjzUZUI'

# Create updater and dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Function to handle regular messages
def handle_messages(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.lower()

    # Iterate through intents
    for intent in intents:
        if 'patterns' in intent and 'responses' in intent:
            for pattern in intent['patterns']:
                if pattern.lower() in user_message:
                    response = random.choice(intent['responses'])
                    update.message.reply_text(response)

                    # If the intent is related to book categories or menu, provide the introduction
                    if intent['tag'] in ["greeting", "book_menu"]:
                        start(update, context)
                        
                    return

    # If no intent matches, handle as an unknown query
    unknown_query(update)

# Command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    introduction = "Hello! I'm your Book Chatbot. We have books under the following categories:\n\n"\
                    "1. Combined Maths\n"\
                    "2. Chemistry\n"\
                    "3. Physics\n"\
                    "4. Biology\n\n"\
                    "Please select a category by typing the corresponding number."
    
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

# Add command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

# Start the bot
updater.start_polling()
updater.idle()



#     5881058982:AAGJYI0beRW2Ke7xeJ89M_vUd5lHtjzUZUI