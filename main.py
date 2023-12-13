import json
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import spacy
import re
import requests
import functions

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Load menu and intents from JSON files
with open('menu.json', 'r') as menu_file:
    menu = json.load(menu_file)

with open('intents.json', 'r') as intents_file:
    intents = json.load(intents_file)["intents"]

# Telegram Bot Token
TOKEN = 'x'

# Create updater and dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Maintain a dictionary to store user orders
user_orders = {}

# Maintain a dictionary to store user orders
user_orders = []

# At the beginning of your main.py, create an empty list to store order details
order_details_list = []


def handle_messages(update: Update, context: CallbackContext) -> None:
    global order_details_list
    global user_orders

    user_message = update.message.text.lower()
     # Extract author names using spaCy NER
    doc = nlp(user_message)
    ner_authors = [ent.text.lower() for ent in doc.ents if ent.label_ == "PERSON"]

    # Check if the user mentioned an author name, book title, or category
    menu_authors = [author['author'].lower() for author in menu if author['author'].lower() in user_message]

    # Combine NER and menu_authors to get a comprehensive list of mentioned authors
    mentioned_authors = list(set(ner_authors + menu_authors))
        
    # Check if the user mentioned an author name, book title, or category
    #mentioned_authors = [author['author'].lower() for author in menu if author['author'].lower() in user_message]
    mentioned_titles = [book['title'].lower() for book in menu if book['title'].lower() in user_message]
    mentioned_categories = [category for category in [book['category'].lower() for book in menu] if category in user_message]
    
    price_query_result = extract_price_query(user_message)
    if price_query_result:
        response = handle_price_query(update, price_query_result)
        if response:
            update.message.reply_text(response)
        return 
    # if re.search(r'(\w+) books under (\d+)lkr', user_message):
    # # Handle book category and price range queries
    #     category_price_range_pattern = re.compile(r'(\w+) books under (\d+)lkr')
    #     match = category_price_range_pattern.search(user_message)

    #     if match:
    #         target_category = match.group(1).lower()
    #         upper_limit = int(match.group(2))

    #         books_in_category_and_range = [book for book in menu if book['category'].lower() == target_category and int(book['price_lkr']) <= upper_limit]

    #         if books_in_category_and_range:
    #             response = f"We found the following {target_category.capitalize()} books under {upper_limit}LKR:\n\n"
    #             for book in books_in_category_and_range:
    #                 response += f"Book ID: {book['book_id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nCategory: {book['category']}\nPrice: {book['price_lkr']} LKR\n\n"
    #             update.message.reply_text(response)
    #         else:
    #             update.message.reply_text(f"Sorry, we don't have any {target_category.capitalize()} books in the specified price range.")
    #         return
    elif mentioned_authors or mentioned_titles or mentioned_categories:
        if mentioned_authors:
            books_info = [book for book in menu if book['author'].lower() in mentioned_authors]
            mention_type = 'author'
        elif mentioned_titles:
            books_info = [book for book in menu if book['title'].lower() in mentioned_titles]
            mention_type = 'title'
        else:
            books_info = [book for book in menu if book['category'].lower() in mentioned_categories]
            mention_type = 'category'

        if books_info:
            suggestions = f"We found the following books by {', '.join(mentioned_authors)}:\n\n" if mention_type == 'author' else f"We found the following books with titles {', '.join(mentioned_titles)}:\n\n" if mention_type == 'title' else f"We found the following books with category :\n\n"
            for book in books_info:
                suggestions += f"Book ID: {book['book_id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nCategory: {book['category']}\nPrice: {book['price_lkr']} LKR\n\n"

            update.message.reply_text(suggestions)
            # Ask if the user wants to order any of these books
            update.message.reply_text("Do you want to order any of these books? Reply with '#Order' followed by the Book ID if yes.")
        else:
            if mention_type == 'author':
                update.message.reply_text(f"I'm sorry, but we don't have any books by {', '.join(mentioned_authors)} at the moment.")
            elif mention_type == 'category':
                update.message.reply_text(f"I'm sorry, but we don't have any books in {', '.join(mentioned_categories)} at the moment.")
            else:
                update.message.reply_text(f"I'm sorry, but we don't have any books with titles {', '.join(mentioned_titles)} at the moment.")
        return
    elif user_message.startswith("#order"):
        # Process the order command
        try:
            book_id = int(user_message.split(" ")[1])
            ordered_book = next((book for book in menu if book['book_id'] == str(book_id)), None)
            if ordered_book:
                # Check if user_orders is defined
                if 'user_orders' not in globals():
                    user_orders = []  # Initialize user_orders if not defined

                # Store the ordered books in user_orders
                user_orders.append(ordered_book)

                update.message.reply_text(f"Book ID {book_id} added to your order. To confirm, type '#Confirm Order'.")
            else:
                update.message.reply_text(f"I'm sorry, but there is no book with ID {book_id}. Please provide a valid Book ID.")
        except ValueError:
            update.message.reply_text("Invalid order command. Please use the format '#Order [Book ID]'.")
    elif user_message == "#confirm order":
        # Confirm the order and process it (replace this with your actual order processing logic)
        if user_orders:
            # Display the ordered books to the user
            confirmation_message = "You've selected the following books:\n"
            for book in user_orders:
                confirmation_message += f"Title: {book['title']}\nAuthor: {book['author']}\nPrice: {book['price_lkr']} LKR\n\n"
            confirmation_message += "If you want to order more books type '#order' following book ID. When you are ready to confirm all the books and provide your telephone number, type '#Confirm All'."
            update.message.reply_text(confirmation_message)
        else:
            update.message.reply_text("You don't have any books in your order. Add books using the '/Order [Book ID]' command.")
    elif user_message == "#confirm all":
        # Confirm all the ordered books and ask for telephone number
        if user_orders:
            # Notify about the successful order
            confirmation_message = "Great! You've successfully ordered the following books:\n"
            order_details = []

            for book in user_orders:
                confirmation_message += f"Title: {book['title']}\nAuthor: {book['author']}\nPrice: {book['price_lkr']} LKR\n\n"
                order_details.append({
                    "book_id": book['book_id'],
                    "telephone_number": user_message.split(" ")[-1]
                })

            confirmation_message += "Please provide your telephone number to complete the order."
            update.message.reply_text(confirmation_message)

            # Store order details in the global list
            order_details_list.extend(order_details)

            # Clear the user's order list after completing the order
            user_orders = []
        else:
            update.message.reply_text("You don't have any books in your order. Add books using the '#Order [Book ID]' command.")
    elif user_message.isdigit() and re.match(r'^07\d{8}$', user_message):
        # Process the telephone number
        telephone_number = user_message
    # Print ordered book IDs along with the telephone number in the VSCode terminal
        if order_details_list:
            ordered_book_ids = [order['book_id'] for order in order_details_list]
            print(f"Ordered Book IDs: {', '.join(ordered_book_ids)} | Telephone Number: {telephone_number}")

         # Add ordered book IDs and telephone number to the order_details_list
            order_details_list.clear()
            order_details_list.append({
                "book_id": ordered_book_ids,
                "telephone_number": telephone_number
        })

        # Call the function to send order details to the web application
            send_order_details_to_web()

        # Add your logic to handle the telephone number and ordered books (replace this comment with your actual logic)
            update.message.reply_text(f"Thank you! Your order is confirmed. We will contact you at {telephone_number} for further details.")

        # Clear the global order details list after sending the details
            order_details_list = [] 
            
        else:
            update.message.reply_text("You don't have any books in your order. Add books using the '#Order [Book ID]' command.")
    
    elif re.search(r'(\d+)lkr to (\d+)lkr', user_message):
        # Handle price range queries
        price_range_pattern = re.compile(r'(\d+)lkr to (\d+)lkr')
        match = price_range_pattern.search(user_message)

        if match:
            lower_limit = int(match.group(1))
            upper_limit = int(match.group(2))

            books_in_range = [book for book in menu if lower_limit <= int(book['price_lkr']) <= upper_limit]

            if books_in_range:
                response = f"We found the following books in the price range of {lower_limit}LKR to {upper_limit}LKR:\n\n"
                for book in books_in_range:
                    response += f"Book ID: {book['book_id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nCategory: {book['category']}\nPrice: {book['price_lkr']} LKR\n\n"
                update.message.reply_text(response)
            else:
                update.message.reply_text(f"Sorry, we don't have any books in the specified price range.")
            return
   
    
    

    else:
        # Iterate through intents
        for intent in intents:
            if 'patterns' in intent and 'responses' in intent:
                for pattern in intent['patterns']:
                    # Check for similarity using spaCy
                    doc_user = nlp(user_message)
                    doc_pattern = nlp(pattern.lower())

                    similarity = doc_user.similarity(doc_pattern)
                    if similarity >= 0.7:  # Adjust the similarity threshold as needed
                        response = random.choice(intent['responses'])
                        update.message.reply_text(response)

                        # If the intent is related to book categories or menu, provide the introduction
                        if intent['tag'] == "book_menu":
                            functions.book_menu(update, context)
                        return
        else:
            # If no intent matches and no mentioned categories, handle as an unknown query
            functions.unknown_query(update)

# Function to send order details to the web application
def send_order_details_to_web():
    global order_details_list
    print(order_details_list)
    if order_details_list:
        try:
            # Assuming your web application is running locally on port 3002
            web_api_url = "http://localhost:3002/orders"
            
            # Modify the JSON payload to include 'telephone_number'
            response = requests.post(web_api_url, json={"orders": [{"book_id": order['book_id'], "telephone_number": order['telephone_number']} for order in order_details_list]})
            
            if response.status_code == 200:
                print("Order details sent to the web application successfully.")
                # Clear the list after sending the details
                order_details_list = []
        except Exception as e:
            print("Error sending order details to the web application:", str(e))

def handle_price_query(update: Update, query_result: tuple) -> str:
    target_category, operator, *limits = query_result

    if operator in ['under', 'below', 'less than', 'maximum']:
        books_in_price_range = [book for book in menu if book['category'].lower() == target_category and int(book['price_lkr']) <= int(limits[0])]

        if books_in_price_range:
            response = f"We found the following {target_category.capitalize()} books {operator} {limits[0]}LKR:\n\n"
            for book in books_in_price_range:
                response += f"Book ID: {book['book_id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nCategory: {book['category']}\nPrice: {book['price_lkr']} LKR\n\n"
            return response
        else:
            return f"Sorry, we don't have any {target_category.capitalize()} books in the specified price range."
    elif operator in ['over', 'above']:
        books_over_price = [book for book in menu if book['category'].lower() == target_category and int(book['price_lkr']) >= int(limits[0])]

        if books_over_price:
            response = f"We found the following {target_category.capitalize()} books {operator} {limits[0]}LKR:\n\n"
            for book in books_over_price:
                response += f"Book ID: {book['book_id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nCategory: {book['category']}\nPrice: {book['price_lkr']} LKR\n\n"
            update.message.reply_text(response)
        else:
            update.message.reply_text(f"Sorry, we don't have any {target_category.capitalize()} books {operator} the specified price.")
    elif operator == 'range':
        lower_limit, upper_limit = limits
        books_in_price_range = [book for book in menu if book['category'].lower() == target_category and lower_limit <= int(book['price_lkr']) <= upper_limit]

        if books_in_price_range:
            response = f"We found the following {target_category.capitalize()} books in the range of {lower_limit}LKR to {upper_limit}LKR:\n\n"
            for book in books_in_price_range:
                response += f"Book ID: {book['book_id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nCategory: {book['category']}\nPrice: {book['price_lkr']} LKR\n\n"
            update.message.reply_text(response)
        else:
     
           update.message.reply_text(f"Sorry, we don't have any {target_category.capitalize()} books in the specified price range.")
    elif operator == 'between':
        lower_limit, upper_limit = map(int, limits)
        books_in_price_range = [book for book in menu if book['category'].lower() == target_category and lower_limit <= int(book['price_lkr']) <= upper_limit]

        if books_in_price_range:
            response = f"We found the following {target_category.capitalize()} books between {lower_limit}LKR and {upper_limit}LKR:\n\n"
            for book in books_in_price_range:
                response += f"Book ID: {book['book_id']}\nTitle: {book['title']}\nAuthor: {book['author']}\nCategory: {book['category']}\nPrice: {book['price_lkr']} LKR\n\n"
            return response
        else:
            return f"Sorry, we don't have any {target_category.capitalize()} books in the specified price range."

def extract_price_query(user_message):
    # Define patterns for different price-related queries
    under_pattern = re.compile(r'(\w+) books (under|below|less than|maximum) (\d+)lkr')
    over_pattern = re.compile(r'(\w+) books (over|above) (\d+)lkr')
    range_pattern = re.compile(r'(\w+) books with the range of (\d+)lkr to (\d+)lkr')

    # Check for "under" type query
    match_under = under_pattern.search(user_message)
    if match_under:
        return match_under.groups()

    # Check for "over" type query
    match_over = over_pattern.search(user_message)
    if match_over:
        return match_over.groups()

    # Check for "range" type query
    match_range = range_pattern.search(user_message)
    if match_range:
        return match_range.groups()

    # If no match, return None
    return None

# Add command handlers
dispatcher.add_handler(CommandHandler("start", functions.start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))


# Start the bot
updater.start_polling()
updater.idle()


