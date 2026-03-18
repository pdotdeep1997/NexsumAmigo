from models.telegram import Update

from service.state_machine.manager import StateMachine
from service.agent.manager import AgentManger
from utils.config.config import STATE_MESSAGE, STATE_QUIZ
from service.telegram.telegram_manager import TelegramManager
from service.question_manager.question_manager import QuestionManager
from utils.config.config import STATE_MESSAGE, STATE_QUIZ


def process_question_response(update: Update, language:str):
    chat_id=str(update.callback_query.message.chat.id)

    SM = StateMachine(chat_id=chat_id, language=language)
    TM = TelegramManager(chat_id=chat_id, language=language)
    QM = QuestionManager(state_machine=SM, telegram_manager=TM)

    AM = AgentManger(language=language)

    state = SM.get_current_state()

    cb_data = update.callback_query.data
    m_type,q_uuid,user_response,correct_ans = cb_data.split(":")

    question_id_mapping_dict = SM.ChatQuestion.get_question_id_mapping(q_uuid)

    if question_id_mapping_dict:
        #update question
        message_id = question_id_mapping_dict.get("message_id",None)
        is_answered = question_id_mapping_dict.get("question_answered_state",False)
        print("question_id_mapping_dict")
        print(question_id_mapping_dict)
        if not is_answered:
            QM.update_answered_question(q_uuid)
            if user_response == correct_ans:
                TM.send_message("Great Work Answering that question correctly!")
            else:
                TM.send_message("Oh man! you got that wrong")

            SM.ChatQuestion.update_question_as_answered(q_uuid)

    else:
        pass
    
    if state == STATE_QUIZ:
        q_id = SM.ChatQuestion.get_next_revision_question_id()
        if q_id:
            TM.send_message("Next question...")
            QM.send_question(q_id)
        else:
            TM.send_message("That's the end of the quick quiz!")
            TM.send_message("Now back to learning!")
            SM.change_to_message_mode()

            message_history = SM.ContextHistory.read_context()

            lesson_plan = SM.LessonPlan.read_lesson_plan()
            current_goal = lesson_plan["plan"][lesson_plan['current']]
            lesson_context = f"{current_goal['topic']}:{current_goal['goal']}"

            latest_response = ""
            for resp in AM.execute_question_agent(message="What's next?", message_history=message_history, lesson_context=lesson_context):
                if resp:
                    latest_response += f"{resp}\n"
                    TM.send_message(resp)

        pass
    elif state == STATE_MESSAGE:
        pass
