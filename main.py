#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from secret import TELE_BOT_TOKEN
from agents.simple_hindi_agent.agent import execute_agent
from agents.amigo_hindi_agent.agent import execute_agent as execute_amigo_agent

from cache.cache import get_message_history, set_message_history, get_learning_progress, set_learning_progress
from database.supabase.get_lesson_subscripton import get_subscribed_lesson
from database.supabase.get_user_lesson_progress import get_user_lesson_progress

from lesson_utils.lesson_utils import extract_message_context
from message_utils.question import trigger_question

bot = telebot.TeleBot(TELE_BOT_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
        Hi there, I am EchoBot.
        I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
        """)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    print(message.chat.first_name)
    username = "Pradeep"
    chat_id = message.chat.id
    message_history: list = get_message_history(message.chat.id)
    # # lesson_progress: dict = get_learning_progress(message.chat.id)

    # # lesson = get_subscribed_lesson(telegram_id=message.chat.id)
    # # lesson_plan_id = lesson.get("lesson_id")
    # # lesson_plan = []
    # # if lesson:
    # #     lesson_plan = lesson.get("amigo_lesson_plan",{}).get("lesson_plan", [])

    # # user_progress = get_user_lesson_progress(telegram_id=message.chat.id, lesson_id=lesson_plan_id)

    # if not lesson_plan:
    #     bot.send_message(chat_id, "I think you havent subscribed to any lessons? Subscribe to a lesson or reach out to support for help")
    #     return 
    
    # context = []
    # if user_progress:
    #     lesson_progress = user_progress.get("lesson_progress", [])
    #     context = extract_message_context(lesson_progress)
    # else:
    #     context = lesson_plan[0:3]


    # print(lesson)
    # print(user_progress)
    
    print(f"Message received from {message.chat.id}: {message.text}")

    chat_id = message.chat.id  
    message_history.append({"role": "user", "content": message.text})
    # print("CONTEXT!!")
    # print(context)


    # OPTIONAL: Send response with interactive buttons
    # if "?" in message.text or message.text.lower().startswith("help"):
    #     trigger_question(bot, chat_id=chat_id,question_id="_")
    #     send_lesson_menu(chat_id=chat_id)


    for response in execute_amigo_agent(message.text, message_history, lesson_context=""):
        if response:
            message_history.append({"role": "assistant", "content": response})
            bot.send_message(chat_id, response) 
            set_message_history(message.chat.id, message_history[-10:])


lesson_plan = [
    {"title": "Greetings", "id": "lesson_1"},
    {"title": "Numbers", "id": "lesson_2"},
    {"title": "Food", "id": "lesson_3"},
]


def send_lesson_menu(chat_id, completed_lessons=[]):
    keyboard = []
    for lesson in lesson_plan:
        title = lesson["title"]
        lesson_id = lesson["id"]
        completed = "✅" if lesson_id in completed_lessons else "🔓"
        button = InlineKeyboardButton(f"{completed} {title}", callback_data=f"lesson:{lesson_id}")
        keyboard.append([button])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id, "📚 Choose a lesson to continue:", reply_markup=reply_markup)




@bot.callback_query_handler(func=lambda call: call.data.startswith("question:"))
def callback_query(call: CallbackQuery):
    print("Got answer from question")
    _,question_id,option_id = call.data.split(":")
    if option_id == "12323":
        bot.answer_callback_query(call.id, "Awesome! Here's how I can help.")
        bot.send_message(call.message.chat.id, "Try asking me: 'How do I say good morning in Hindi?' 😊")
    else:
        bot.answer_callback_query(call.id, "Got it! Let me know if you need anything.")
        bot.send_message(call.message.chat.id, "Okay! Feel free to message me anytime.")



@bot.callback_query_handler(func=lambda call: call.data.startswith("lesson:"))
def handle_lesson_click(call):
    lesson_id = call.data.split(":")[1]
    
    # Load the lesson details based on the ID
    lesson_title = next((l["title"] for l in lesson_plan if l["id"] == lesson_id), "Unknown Lesson")
    
    # Send the lesson intro or first flashcard
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, f"📝 Starting lesson: *{lesson_title}*", parse_mode="Markdown")
    
    # Here you can start sending actual flashcard content
    bot.send_message(call.message.chat.id, f"Flashcard 1: How do you say 'Hello' in Hindi?\nAnswer: *Namaste*", parse_mode="Markdown")
    
    # Mark as completed (in real case, save to DB)
    completed_lessons = get_learning_progress(call.message.chat.id)
    completed_lessons.append(lesson_id)
    #set_learning_progress(call.message.chat.id, completed_lessons)

    # Optionally show menu again
    send_lesson_menu(call.message.chat.id, lesson_plan, completed_lessons)



print("STARTING TELE SERVER")
bot.infinity_polling()