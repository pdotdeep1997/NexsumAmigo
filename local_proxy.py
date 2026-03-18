#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import requests

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from secret import TELE_HINDI_BOT_TOKEN, TELE_ITALIAN_BOT_TOKEN

bot = telebot.TeleBot(TELE_ITALIAN_BOT_TOKEN)

LOCAL_API_URL = "http://127.0.0.1:8000"

tele_url = "http://127.0.0.1:8000/telegram/italian/webhook"

print("setting up local proxy")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print(message)
    try:
        resp = requests.post(
            tele_url,
            json= {
                "update_id": 12345,
                "message": {
                    "message_id": message.message_id,
                    "from": {
                        "id": message.from_user.id,
                        "is_bot": message.from_user.is_bot,
                        "first_name": message.from_user.first_name,
                        "username": message.from_user.username,
                        "language_code": message.from_user.language_code
                    },
                    "chat": {
                        "id": message.chat.id,
                        "first_name": message.chat.first_name,
                        "username": message.chat.username,
                        "type": message.chat.type
                    },
                    "date": message.date,
                    "text": message.text
                }
            }

        )
        print(resp.text)
    except Exception as e:
        print(f"Error sending message to webhook: {e}")




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    # Create the format expected by your FastAPI webhook
    forward_payload = {
        "update_id": 123456789,  # Can use any unique update_id or fetch it dynamically
        "callback_query": {
            "id": call.id,
            "from": {
                "id": call.from_user.id,
                "is_bot": call.from_user.is_bot,
                "first_name": call.from_user.first_name,
                "last_name": call.from_user.last_name,
                "username": call.from_user.username,
                "language_code": call.from_user.language_code
            },
            "chat_instance": call.chat_instance,
            "message": {
                "message_id": call.message.message_id,
                "from": {
                    "id": call.message.from_user.id,
                    "is_bot": call.message.from_user.is_bot,
                    "first_name": call.message.from_user.first_name,
                    "last_name": call.message.from_user.last_name,
                    "username": call.message.from_user.username,
                    "language_code": call.message.from_user.language_code
                },
                "chat": {
                    "id": call.message.chat.id,
                    "type": call.message.chat.type
                },
                "date": call.message.date,
                "text": call.message.text
            },
            "data": call.data
        }
    }

    # Forward to the webhook
    requests.post(tele_url, json=forward_payload)
    print(f"Forwarding callback query: {call.data}")



bot.infinity_polling()