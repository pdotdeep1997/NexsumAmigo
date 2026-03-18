from .. import db


COLLECTION_NAME = "nexsum_context_history"

def read_context_history_for_chat_id_from_firebase(chat_id: str, language: str):
    doc_ref = db.collection(COLLECTION_NAME).document(str(chat_id))
    
    doc = doc_ref.get()
    if doc.exists:
        all_language_history = doc.to_dict()
        if language in all_language_history:
            
            return all_language_history[language]
        return []
    else:
        print("No such document!")
        data = {
            language: []
        }
        db.collection(COLLECTION_NAME).document(str(chat_id)).set(data)
        return []