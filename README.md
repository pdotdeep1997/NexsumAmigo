# NexsumAmigo

NexsumAmigo is an AI language-learning Telegram bot designed to feel less like a course and more like a conversation with a friend. Instead of pushing learners through rigid lessons, the bot chats naturally, asks follow-up questions, gives practice prompts, and helps users build confidence in a target language inside Telegram, where they already spend time.

The project currently supports multiple language-specific bot flows, including Hindi, Italian, and Spanish, with different agent personalities for more conversational learning experiences.

## What the App Does

- Lets users practice a language through natural Telegram conversations
- Uses AI agents to respond like a supportive learning companion
- Sends questions and interactive prompts to reinforce learning
- Tracks context, lesson progress, and revision history
- Supports multiple language and persona variants through separate bot flows

## Why This Is Useful

Language learning products often lose users because they feel repetitive, formal, or disconnected from daily life. A Telegram-based AI bot solves that by meeting learners in a familiar chat interface and turning practice into an ongoing relationship rather than a one-time lesson.

From a business perspective, this model is useful because:

- It reduces friction to entry since users do not need to install a separate learning app
- It increases retention by creating a friend-like conversational habit instead of a textbook workflow
- It supports lightweight, frequent engagement, which is critical for language progress
- It can be adapted into multiple languages, tones, and learner segments without rebuilding the whole product
- It creates room for subscription or premium offerings such as advanced tutoring, custom lesson plans, streak systems, or specialized personas

In short, the product is valuable because it combines accessibility, habit formation, and personalization in a format that is easy for users to return to every day.

## Technical Structure

This project is structured as a FastAPI backend that receives Telegram webhook events, routes them into the conversation engine, and sends responses back through the Telegram Bot API.

Key parts of the codebase:

- `app.py` bootstraps the FastAPI application and registers the Telegram router
- `routers/telegram.py` exposes webhook endpoints for each supported language/persona flow and a reminder endpoint
- `service/conversation_engine/` handles incoming messages and question responses
- `service/agent/` selects the right AI agent implementation for the chosen language flow
- `agents/` contains the actual prompt and agent logic for each language or personality variant
- `service/telegram/` wraps Telegram Bot API calls for sending and updating messages
- `service/database/` contains adapters and integrations for persistence, including Firebase, Supabase, vector retrieval, and in-memory lesson plan sources
- `service/modules/` includes supporting workflows such as reminders and feedback
- `models/` defines request and response models for Telegram and internal messaging

At a high level, the request flow is:

1. Telegram sends an update to a language-specific webhook.
2. The router dispatches the event in the background.
3. The conversation engine decides whether the user sent a free-form message or answered a question.
4. The selected AI agent generates the next response.
5. State, context, and lesson progress can be read from or written to the storage layer.
6. The Telegram manager sends the reply back to the user.

## Running the Project

The repository is a Python service with FastAPI entrypoints and Telegram integrations. To run it locally, install the Python dependencies from `requirements.txt`, configure the required secrets for Telegram and backing services, and start the API server that serves `app.py`.
