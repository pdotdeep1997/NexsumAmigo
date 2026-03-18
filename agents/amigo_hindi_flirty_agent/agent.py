from openai import OpenAI
import json
from typing import List

from .prompt import get_prompt
from secret import OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)


def execute_agent(message: str, message_history: list[str], lesson_context: str, is_reminder=False):
    latest_message = ""

    for msg in get_agent_response(message, message_history, lesson_context, is_reminder):
        print(msg)
        if msg != 'EOF':
            latest_message += msg
        if '.' in msg or '!' in msg or '?' in msg or 'EOF' in msg:
            yield latest_message
            latest_message = ""


def get_agent_response(
    message: str,
    message_history: list,
    lesson_context: str,
    is_reminder: bool=False
):
    PROMPT = get_prompt(message, message_history, lesson_context)
    reminder_msg = "The user has not responded in a long time, so send a friendly reminder message." if is_reminder else ""
    msg_history = [{"role": "system", "content": f"You are a flirty and suggestive assistant that teaches Hindi like a playful, charming, slightly naughty friend.{reminder_msg} Current Topic: {lesson_context}"}] + message_history + [{"role": "user", "content": message}]
    print(msg_history)
    response = client.chat.completions.create(
        model="ft:gpt-4.1-mini-2025-04-14:pdotdeep:flirty-hindi:BcSlpEXb",
        messages=msg_history,
        stream=True,
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

    yield "EOF"

