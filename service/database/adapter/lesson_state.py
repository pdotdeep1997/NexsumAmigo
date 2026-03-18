from ..supabase.state.get_state import get_state_for_chat_id_supabase
from ..supabase.state.update_state import update_state_for_chat_id_to_messaging_state,update_state_for_chat_id_to_quiz_state
from ..supabase.state.update_state import update_last_active_state
from utils.config.config import STATE_QUIZ,STATE_MESSAGE

class ChatStateDBHandler:

    def __init__(self, language: str, chat_id: str):
        self.language = language
        self.chat_id = chat_id


    def get_state_for_chat(self):
        return get_state_for_chat_id_supabase(self.chat_id, self.language)
    
    def update_state_for_chat(self, new_state):
        if new_state == STATE_MESSAGE:
            update_state_for_chat_id_to_messaging_state(self.chat_id, self.language)
        elif new_state == STATE_QUIZ:
            update_state_for_chat_id_to_quiz_state(self.chat_id, self.language)

    def update_last_active(self):
        update_last_active_state(self.chat_id, self.language)