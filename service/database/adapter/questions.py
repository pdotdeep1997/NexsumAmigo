from ..supabase.questions.get_questions_by_ids import get_question_by_id_supabase, list_question_by_ids_supabase
from ..supabase.questions.insert_question import insert_question_supabase

class QuestionDBHandler:

    def __init__(self, language: str):
        self.language = language

    # --- Supabase Calls ---

    def get_question_by_id(self, question_id: str) -> dict:
        question = get_question_by_id_supabase(question_id, self.language)
        return question

    def get_questions_by_ids(self, question_ids: list[str]) -> list[dict]:
        questions_list = list_question_by_ids_supabase(question_ids, self.language)
        return questions_list

    def insert_question(self, question: dict) -> dict:
        question = insert_question_supabase(question, self.language)
        return question
