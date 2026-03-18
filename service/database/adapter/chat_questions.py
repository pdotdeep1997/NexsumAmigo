from ..firebase.revision_quiz.add_question_to_revision_quiz_firebase import add_question_to_revision_doc_firebase
from ..firebase.revision_quiz.get_next_revision_question_id_from_firebase import get_next_revision_question_id_from_firebase
from ..firebase.revision_quiz.read_current_revision_question_firebase import read_current_revision_question_firebase

from ..vector.get_related_question import get_relevant_document_ids_for_query

from ..supabase.question_uid_mapping.get_question_id_mapping import get_question_id_mapping_supabase
from ..supabase.question_uid_mapping.update_question_id_mapping_with_message_id import update_question_id_mapping_with_message_id_supabase
from ..supabase.question_uid_mapping.insert_question_id_mapping import insert_question_instance_supabase
from ..supabase.question_uid_mapping.update_question_as_answered import update_question_as_answered_supabase

class ChatQuestionDBHandler:

    def __init__(self, language: str, chat_id: str):
        self.language = language
        self.chat_id = chat_id


    def add_question_to_revision(self, question_id: str):
        add_question_to_revision_doc_firebase(self.chat_id, self.language, question_id)

    def get_next_revision_question_id(self) -> str | None:
        return get_next_revision_question_id_from_firebase(self.chat_id, self.language)
    
    def read_current_revision_question(self):
        return read_current_revision_question_firebase(self.chat_id, self.language)


    def insert_question_id_mapping(self, question_id: str) -> dict:
        question_instance = insert_question_instance_supabase(question_id)
        return question_instance

    def get_question_id_mapping(self, question_uid: str) -> dict:
        question_instance = get_question_id_mapping_supabase(question_uid)
        return question_instance
    
    def update_question_id_mapping_with_message_id(self, q_uid: str, message_id: str):
        question_instance = update_question_id_mapping_with_message_id_supabase(q_uid=q_uid, message_id=message_id)
        return question_instance
    
    def update_question_as_answered(self, q_uid):
        question_instance = update_question_as_answered_supabase(q_uid=q_uid)
        return question_instance
    

    def add_quick_revision_question_for_message(self, message):
        doc_ids = get_relevant_document_ids_for_query(message, self.language, 1)
        question_id = doc_ids[0]
        self.add_question_to_revision(question_id)
