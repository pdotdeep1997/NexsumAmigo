from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pydantic import BaseModel
import json
from service.state_machine.manager import StateMachine
from service.telegram.telegram_manager import TelegramManager 

class Option(BaseModel):
    option: str
    option_id: int

class Question(BaseModel):
    question_id: str
    question: str
    correct_ans: int
    options: list[Option]


class QuestionManager():


    def __init__(self, state_machine: StateMachine, telegram_manager: TelegramManager):
        self.SM = state_machine
        self.TM = telegram_manager
        
    def send_question(self, question_id):
        q_uid, question_text, reply_markup_json = self.get_question_and_markup_for_question(question_id=question_id)
        print("QUESTION AND MARKUP")
        print(question_text, reply_markup_json)
        message_id = self.TM.send_question(question=question_text, reply_markup=reply_markup_json)
        self.SM.ChatQuestion.update_question_id_mapping_with_message_id(q_uid, message_id)


    def update_answered_question(self, q_uid: str):
        question_uid_mapping = self.SM.ChatQuestion.get_question_id_mapping(question_uid=q_uid)
        question_id = question_uid_mapping.get("question_id")
        message_id = question_uid_mapping.get("message_id")
        
        question_dict = self.SM.QuestionsHandler.get_question_by_id(question_id=question_id)
        
        question_model = self._get_question_model(question_dict, is_answered=True)

        keyboard = [[InlineKeyboardButton(o.option, callback_data=f"question:{q_uid}:{o.option_id}:{question_model.correct_ans}")] for o in question_model.options]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup_json = json.dumps(reply_markup.to_dict())
        question_text = question_model.question

        self.TM.update_question(question=question_text, reply_markup=reply_markup_json, message_id=message_id)
    

    def get_question_and_markup_for_question(self, question_id):
        question_id_mapping = self.SM.ChatQuestion.insert_question_id_mapping(question_id=question_id)
        q_uid = question_id_mapping.get("id")

        question_dict = self.SM.QuestionsHandler.get_question_by_id(question_id=question_id)
        print(question_dict)
        print("QUESTION DICT")
        question_model = self._get_question_model(question_dict)

        keyboard = [[InlineKeyboardButton(o.option, callback_data=f"question:{q_uid}:{o.option_id}:{question_model.correct_ans}")] for o in question_model.options]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup_json = json.dumps(reply_markup.to_dict())

        question_text = question_model.question

        return q_uid, question_text, reply_markup_json

    def _get_question_model(self, question_dict: dict, is_answered=False):
        print("THIS IS THE QUESTINOS")
        print(question_dict)
        question_id = question_dict.get("id")
        question = question_dict.get("question")
        c_ans = question.get("correct_answer",None)
        tick = "\u2705"  # ✅
        cross = "\u274C" 
        options = [
            Option(option=f"{(tick if i == c_ans else cross) if is_answered else ''}{o}",option_id=i) for i,o in enumerate(question.get("options",[]))
        ]
        return Question(question_id=question_id,question=question.get("question",""), options=options, correct_ans=question.get("correct_answer",""))


