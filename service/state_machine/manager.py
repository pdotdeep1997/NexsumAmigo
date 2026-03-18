from service.database.adapter.lesson_state import ChatStateDBHandler
from service.database.adapter.lesson_plan import LessonPlan
from service.database.adapter.context_history import ContextHistoryDBHandler
from service.database.adapter.questions import QuestionDBHandler
from service.database.adapter.chat_questions import ChatQuestionDBHandler

from utils.config.config import STATE_QUIZ,STATE_MESSAGE


States = [STATE_MESSAGE,STATE_QUIZ]




class StateMachine():

    def __init__(self, chat_id, language):
        self.chat_id = chat_id
        self.language = language

        self.ChatState = ChatStateDBHandler(language=language, chat_id=chat_id)
        self.ContextHistory = ContextHistoryDBHandler(language=language, chat_id=chat_id)
        self.ChatQuestion = ChatQuestionDBHandler(language=language, chat_id=chat_id)
        self.QuestionsHandler = QuestionDBHandler(language=language)
        self.LessonPlan = LessonPlan(chat_id=chat_id, language=language)


    def change_to_quiz_mode(self):
        self.ChatState.update_state_for_chat(STATE_QUIZ)

    def change_to_message_mode(self):
        self.ChatState.update_state_for_chat(STATE_MESSAGE)

    def get_current_state(self):
        state_dict =  self.ChatState.get_state_for_chat()
        return state_dict.get("state")
    
    def process_command(self, message: str) -> bool:
        if message.startswith('/quiz'):
            self.change_to_quiz_mode()
            return True
        elif message.startswith('/end_quiz'):
            self.change_to_message_mode()
            return True
        return False
