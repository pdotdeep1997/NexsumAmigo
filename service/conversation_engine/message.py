from models.telegram import Update

from service.state_machine.manager import StateMachine
from service.telegram.telegram_manager import TelegramManager
from service.question_manager.question_manager import QuestionManager
from service.agent.manager import AgentManger

from cache.count_since_question_cache import get_count, update_count

from utils.config.config import STATE_MESSAGE, STATE_QUIZ

def process_message(update: Update, language:str):
    message = update.message
    chat_id = str(message.chat.id)

    SM = StateMachine(chat_id=chat_id, language=language)
    TM = TelegramManager(chat_id=chat_id, language=language)
    QM = QuestionManager(state_machine=SM, telegram_manager=TM)
    AM = AgentManger(language=language)
    
    state = SM.get_current_state()

    SM.ChatState.update_last_active()

    if SM.process_command(message.text):
        # State was changed
        state = SM.get_current_state()
        if state == STATE_MESSAGE:
            TM.send_message("I am back! how was the quiz?")
        elif state == STATE_QUIZ:
            q_id = SM.ChatQuestion.get_next_revision_question_id()
            if q_id:
                TM.send_message("Time for a quiz!!")
                QM.send_question(question_id=q_id)
            else:
                TM.send_message("You need to do more learning before i can judge what to test you on!")
                SM.change_to_message_mode()
        #Do nothing besides changing states
    else:
        state = SM.get_current_state()
        if state == STATE_QUIZ:
            # Messaging in quiz modes means they are asking for help/hints for quiz
            q_id = SM.ChatQuestion.read_current_revision_question()
            if q_id:
                print(f"Retrieveing Question: {q_id}")
                message_history = SM.ContextHistory.read_context()
                question_dict = SM.QuestionsHandler.get_question_by_id(question_id=q_id)

                question_text = question_dict.get("question").get("question")
                latest_response = ""
                for resp in AM.execute_question_agent(message=message.text, message_history=message_history, question=question_text):
                    if resp:
                        latest_response += f"{resp}\n"
                        TM.send_message(resp)
                
                message_history.append({"role": "assistant", "content": latest_response})
                SM.ContextHistory.save_context(message_history=message_history)

                # TODO SAVE COMPLETE LESSON HISTORY

            else:
                TM.send_message("Seems like you dont have a valid question to be asked.")
                SM.change_to_message_mode()

        elif state == STATE_MESSAGE:
            # Normal chatting/learning
            message_history = SM.ContextHistory.read_context()
            lesson_plan = SM.LessonPlan.read_lesson_plan()

            current_goal = lesson_plan["plan"][lesson_plan['current']]
            lesson_context = f"{current_goal['topic']}:{current_goal['goal']}"


            latest_response = ""
            for resp in AM.execute_agent(message=message.text, message_history=message_history, lesson_context=lesson_context):
                if resp:
                    latest_response += f"{resp}\n"
                    TM.send_message(resp)

            message_history.append({"role": "user", "content": message.text})
            message_history.append({"role": "assistant", "content": latest_response})
            SM.ContextHistory.save_context(message_history=message_history)

            update_count(chat_id=chat_id)

            SM.ChatQuestion.add_quick_revision_question_for_message(latest_response)

            # TODO SAVE MESSAGE TO COMPLETE HISTORY

            lesson_plan["plan"][lesson_plan['current']]["count"] += 1
            if lesson_plan["plan"][lesson_plan['current']]["count"] > 20:
                #Conduct Quiz
                TM.send_message(f"Do you want to try a quick quiz on what you learnt so far?")
                TM.send_message(f"Type /quiz to get started!")
                lesson_plan["current"] += 1

            SM.LessonPlan.update_lesson_plan(lesson_plan)
            