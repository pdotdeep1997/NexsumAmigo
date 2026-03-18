from .. import db
from google.cloud import firestore
import datetime

COLLECTION_NAME = "nexsum_revision_quiz"

def add_question_to_revision_doc_firebase(chat_id: str, language: str, question_id: str):
    revision_doc = db.collection(COLLECTION_NAME).document(chat_id).get()
    if revision_doc.exists:
        revision = revision_doc.to_dict()
        print(revision)
        if language in revision:
            revision[language]["questions"].append(question_id)
            revision[language]["questions"] = list(set(revision[language]["questions"]))
        else:
            revision[language] = {
                "questions": [question_id],
                "current": None
            }
        db.collection(COLLECTION_NAME).document(chat_id).update(revision)
        return

    db.collection(COLLECTION_NAME).document(chat_id).set({
        language: {
            "questions": [question_id],
            "current": None
        }
    })
    