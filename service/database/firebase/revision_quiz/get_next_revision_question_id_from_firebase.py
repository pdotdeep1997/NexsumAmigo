from .. import db
from google.cloud import firestore
import datetime

COLLECTION_NAME = "nexsum_revision_quiz"

def get_next_revision_question_id_from_firebase(chat_id: str, language: str):
    revision_doc = db.collection(COLLECTION_NAME).document(chat_id).get()
    if revision_doc.exists:
        revision = revision_doc.to_dict()
        if language in revision:
            questions = revision[language]["questions"]
            if questions:
                q = questions.pop()
                revision[language]["current"] = q
                db.collection(COLLECTION_NAME).document(chat_id).update(revision)
                return q
            else:
                return None
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
    