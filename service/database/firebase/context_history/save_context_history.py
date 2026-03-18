from .. import db


COLLECTION_NAME = "nexsum_context_history"

def save_context_history_for_chat_id(chat_id: str, language: str, messages: list):
    data = {
        language: messages[-20:]
    }
    db.collection(COLLECTION_NAME).document(str(chat_id)).update(data)