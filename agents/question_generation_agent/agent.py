from openai import OpenAI
import json
from typing import List

from .prompt import get_prompt
from secret import OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)


def execute_agent(message: str, message_history: list[str], question: str):
    latest_message = ""

    for msg in get_agent_response(message, message_history, question):
        print(msg)
        if msg != 'EOF':
            latest_message += msg
        if '.' in msg or '!' in msg or '?' in msg or 'EOF' in msg:
            yield latest_message
            latest_message = ""


def get_agent_response(
    message: str,
    message_history: list,
    question: str,
):

    msg_history = [{"role": "system", "content": f"You are a friendly assistant that teaches Hindi like a supportive friend. you need to guide the user on how to solve the question : {question}. Dont give them the answer"}] + message_history + [{"role": "user", "content": message}]
    print(msg_history)
    response = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:pdotdeep:hindi-training-001:BLlHRUFV",
        messages=msg_history,
        stream=True,
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content

    yield "EOF"

