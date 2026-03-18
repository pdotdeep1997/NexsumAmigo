
import requests
from secret import TELE_HINDI_BOT_TOKEN, TELE_ITALIAN_BOT_TOKEN, TELE_SPANISH_BOT_TOKEN, TELE_ITALIAN_BADDIE_BOT_TOKEN, TELE_HINDI_FLIRTY_BOT_TOKEN

from models.response import TelegramSendMessageResponse

def get_telebot_token(language: str):
    if language == 'italian':
        return TELE_ITALIAN_BOT_TOKEN
    elif language == 'hindi':
        return TELE_HINDI_BOT_TOKEN
    elif language == 'spanish':
        return TELE_SPANISH_BOT_TOKEN
    elif language == 'flirtyitalian':
        return TELE_ITALIAN_BADDIE_BOT_TOKEN
    elif language == 'flirtyhindi':
        return TELE_HINDI_FLIRTY_BOT_TOKEN

class TelegramManager:

    def __init__(self, chat_id, language):
        self.chat_id = chat_id
        self.language = language

    def send_message(self, message: str) -> None:
        TELE_BOT_TOKEN = get_telebot_token(language=self.language)
        telegram_api_url = f"https://api.telegram.org/bot{TELE_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message
        }
        resp = requests.post(telegram_api_url, data=data)
        print(resp.json())
        
        parsed_response = TelegramSendMessageResponse(**resp.json())
        print(parsed_response)
    
    def send_question(self, question: str, reply_markup: str) -> str:
        TELE_BOT_TOKEN = get_telebot_token(language=self.language)
        telegram_api_url = f"https://api.telegram.org/bot{TELE_BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": self.chat_id,
            "text": question,
            "reply_markup": reply_markup
        }
        resp = requests.post(telegram_api_url, data=data)
        print(resp.json())
        parsed_response = TelegramSendMessageResponse(**resp.json())
        message_id = parsed_response.result.message_id
        return message_id
    
    def update_message(self, message: str, message_id: str) -> None:
        TELE_BOT_TOKEN = get_telebot_token(language=self.language)
        telegram_api_url = f"https://api.telegram.org/bot{TELE_BOT_TOKEN}/editMessageText"

        payload = {
            "chat_id": self.chat_id,
            "message_id": message_id,
            "text": message,
        }
        resp = requests.post(telegram_api_url, data=payload)
        print("THIS IS THE MESSAGE SENT")
        print(resp.json())

        parsed_response = TelegramSendMessageResponse(**resp.json())
        print(parsed_response)
    


    def update_question(self, question: str, reply_markup: dict, message_id: str) -> None:
        TELE_BOT_TOKEN = get_telebot_token(language=self.language)
        telegram_api_url = f"https://api.telegram.org/bot{TELE_BOT_TOKEN}/editMessageText"

        payload = {
            "chat_id": self.chat_id,
            "message_id": message_id,
            "text": question,
            "reply_markup": reply_markup
        }
        resp = requests.post(telegram_api_url, data=payload)
        print("THIS IS THE MESSAGE SENT")
        print(resp.json)

        parsed_response = TelegramSendMessageResponse(**resp.json())
        print(parsed_response)
    