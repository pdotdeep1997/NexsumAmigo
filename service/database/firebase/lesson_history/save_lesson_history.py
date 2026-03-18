from .. import db
from google.cloud import firestore
import datetime

COLLECTION_NAME = "nexsum_lesson_history"

def save_lesson_history_for_chat_id(chat_id: str,language: str, message: str):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    today_doc_ref = db.collection(COLLECTION_NAME).document(date)
    chat_id_progress_doc_ref = today_doc_ref.collection("history").document(str(chat_id))
    doc = chat_id_progress_doc_ref.get()

    if doc.exists:
        chat_id_progress_doc_ref.update({
            language: firestore.ArrayUnion([message])
        })
    else:
        chat_id_progress_doc_ref.set({
            language: [message]
        })