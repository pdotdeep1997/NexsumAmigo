from openai import OpenAI
import json
from typing import List

from .prompt import get_prompt
from secret import OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)


def fetch_lesson_plan():
    return {
        "intentions": {
            "greeting": "Saying hello, goodbye, and asking how someone is",
            "introducing_yourself": "Telling your name and asking someone’s name",
            "asking_directions": "Asking where a place is",
            "requesting_something": "Asking for water, food, help, etc.",
            "asking_price": "Asking how much something costs",
            "expressing_gratitude": "Saying thank you and sorry",
            "polite_expressions": "Common polite phrases"
        },
        "vocab": {
            "A": {
                "Aap": "You (formal)",
                "Aap kaise hain?": "How are you? (to a male)",
                "Aap kaisi hain?": "How are you? (to a female)",
                "Aaj": "Today",
                "Achha": "Good/Okay"
            },
            "B": {
                "Bhai": "Brother",
                "Bahan": "Sister",
                "Bahut": "Very",
                "Bhaav kya hai?": "What is the price?"
            },
            "C": {
                "Chai": "Tea",
                "Chhota": "Small",
                "Chhutti": "Holiday"
            },
            "D": {
                "Dhanyavad": "Thank you",
                "Dost": "Friend"
            },
            "G": {
                "Ghar": "Home",
                "Garmi": "Hot (weather)",
                "Ghar kahaan hai?": "Where is home?"
            },
            "H": {
                "Haan": "Yes",
                "Hawaai adda": "Airport",
                "Hum": "We"
            },
            "J": {
                "Ji haan": "Yes (polite)",
                "Ji nahin": "No (polite)"
            },
            "K": {
                "Kaun?": "Who?",
                "Kaha?": "Where?",
                "Kitna?": "How much?",
                "Kripya": "Please"
            },
            "M": {
                "Mujhe madad chahiye": "I need help",
                "Mausam": "Weather",
                "Mehenga": "Expensive"
            },
            "N": {
                "Namaste": "Hello (formal)",
                "Naya": "New"
            },
            "P": {
                "Paise": "Money",
                "Paani": "Water",
                "Police": "Police"
            },
            "S": {
                "Shukriya": "Thank you (casual)",
                "Sasta": "Cheap",
                "Samajh nahi aaya": "I don’t understand"
            },
            "T": {
                "Taxi": "Taxi",
                "Tandurust": "Healthy"
            },
            "Y": {
                "Yahan": "Here",
                "Yeh kya hai?": "What is this?"
            }
        },
        "useful_sentences": {
            "greetings": {
                "hello": "Namaste",
                "my_name_is": "Mera naam ___ hai.",
                "how_are_you": "Aap kaise hain? (male) / Aap kaisi hain? (female)",
                "i_am_fine": "Main theek hoon."
            },
            "asking_directions": {
                "where_is_this_place": "Yeh jagah kahaan hai?",
                "i_need_to_go_to_hotel": "Mujhe hotel jaana hai.",
                "is_there_a_metro_nearby": "Kya yahan paas mein metro hai?"
            },
            "requesting_something": {
                "i_need_water": "Mujhe paani chahiye.",
                "can_you_help_me": "Kya aap madad kar sakte hain?",
                "please_show_me_this": "Kripya yeh dikhaiye."
            },
            "asking_price": {
                "how_much_is_this": "Yeh kitne ka hai?",
                "is_this_cheap": "Kya yeh sasta hai?"
            },
            "expressing_gratitude": {
                "thank_you": "Dhanyavad",
                "thanks": "Shukriya",
                "sorry_excuse_me": "Maaf kijiye"
            }
        }
    }


def execute_agent(message: str, message_history: list[str], lesson_progress: dict):
    latest_message = ""
    for msg in get_agent_response(message, message_history, lesson_progress):
        latest_message += msg
        if '.' in msg or '!' in msg:
            yield latest_message
            latest_message = ""


def get_agent_response(
    message: str,
    message_history: list,
    lesson_progress: dict,
):
    PROMPT = get_prompt(message, message_history, lesson_plan=fetch_lesson_plan(), lesson_progress=lesson_progress)

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": PROMPT},
        ],
        stream=True,
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

    yield "EOF"

