from ..firebase.context_history.read_context_history import read_context_history_for_chat_id_from_firebase
from ..firebase.context_history.save_context_history import save_context_history_for_chat_id

class ContextHistoryDBHandler:

    def __init__(self, language: str, chat_id: str):
        self.language = language
        self.chat_id = chat_id

    def read_context(self):
        return read_context_history_for_chat_id_from_firebase(chat_id=self.chat_id, language=self.language)
    
    def save_context(self, message_history: list):
        save_context_history_for_chat_id(chat_id=self.chat_id, language=self.language, messages=message_history)
