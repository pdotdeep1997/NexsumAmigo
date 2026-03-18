from .. import db
from google.cloud import firestore
import datetime

COLLECTION_NAME = "nexsum_revision_quiz"

def read_current_revision_question_firebase(chat_id: str, language: str):
    revision_doc = db.collection(COLLECTION_NAME).document(chat_id).get()
    if revision_doc.exists:
        revision = revision_doc.to_dict()
        if language in revision:
            q = revision[language].get("current")
            return q
        else:
            revision[language] = {
                "questions": [],
                "current": None
            }
            db.collection(COLLECTION_NAME).document(chat_id).update(revision)
        return None

    db.collection(COLLECTION_NAME).document(chat_id).set({
        language: {
            "questions": [],
            "current": None
        }
    })
    return None
    