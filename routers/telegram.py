from fastapi import APIRouter, BackgroundTasks
from models.telegram import Update
from service.conversation_engine.message import process_message
from service.conversation_engine.question import process_question_response
from service.modules.reminder import process_reminders

router = APIRouter(prefix="/telegram")


def process_telegram_message(update: Update, language: str, background_tasks: BackgroundTasks):
    if update.message:
        print(f"Received message from {update.message.from_.username}: {update.message.text}")
        background_tasks.add_task(process_message, update, language)
        
        
    elif update.callback_query:
        print(f"Callback clicked by {update.callback_query.from_.username}: {update.callback_query.data}")
        background_tasks.add_task(process_question_response, update, language)

    return {"status": "ok"}


@router.post("/hindi/webhook")
async def telegram_hindi_webhook(update: Update, background_tasks: BackgroundTasks):
    LANGUAGE = 'hindi'
    return process_telegram_message(update, LANGUAGE, background_tasks)
    
    
@router.post("/flirtyhindi/webhook")
async def telegram_flirtyhindi_webhook(update: Update, background_tasks: BackgroundTasks):
    LANGUAGE = 'flirtyhindi'
    return process_telegram_message(update, LANGUAGE, background_tasks)
    




@router.post("/italian/webhook")
async def telegram_italian_webhook(update: Update, background_tasks: BackgroundTasks):
    LANGUAGE = 'italian'
    return process_telegram_message(update, LANGUAGE, background_tasks)
    


@router.post("/spanish/webhook")
async def telegram_spanish_webhook(update: Update, background_tasks: BackgroundTasks):
    LANGUAGE = 'spanish'
    return process_telegram_message(update, LANGUAGE, background_tasks)
    

@router.post("/flirtyitalian/webhook")
async def telegram_flirtyitalian_webhook(update: Update, background_tasks: BackgroundTasks):
    LANGUAGE = 'flirtyitalian'
    return process_telegram_message(update, LANGUAGE, background_tasks)
    


@router.get("/send_reminders")
async def telegram_reminders(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_reminders)
    return {"status": "Success INITIATING REMINDERS"}
    
