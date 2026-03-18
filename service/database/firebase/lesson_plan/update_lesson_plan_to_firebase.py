from .. import db
from google.cloud import firestore
import datetime

COLLECTION_NAME = "nexsum_lesson_plan"

def update_lesson_plan_to_firebase(chat_id: str,language: str, lesson_plan: dict):
    db.collection(COLLECTION_NAME).document(str(chat_id)).update({
        language: lesson_plan
    })
    