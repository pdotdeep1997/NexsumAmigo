from service.database.adapter.all_users import AllUsersDBAdapter
from service.state_machine.manager import StateMachine
from service.telegram.telegram_manager import TelegramManager
from service.question_manager.question_manager import QuestionManager
from service.agent.manager import AgentManger

def process_reminders():

    forgotton_users = AllUsersDBAdapter().get_all_forgotten_users()
    print(forgotton_users)
    for f in forgotton_users:
        try:
            chat_id = f.get("chat_id")
            language = f.get("language")

            SM = StateMachine(chat_id=chat_id, language=language)
            TM = TelegramManager(chat_id=chat_id, language=language)
            AM = AgentManger(language=language)

            message_history = SM.ContextHistory.read_context()
            lesson_plan = SM.LessonPlan.read_lesson_plan()

            current_goal = lesson_plan["plan"][lesson_plan['current']]
            lesson_context = f"{current_goal['topic']}:{current_goal['goal']}"


            latest_response = ""
            for resp in AM.execute_agent(message="", message_history=message_history, lesson_context=lesson_context, is_reminder=True):
                if resp:
                    latest_response += f"{resp}\n"
                    TM.send_message(resp)

            message_history.append({"role": "assistant", "content": latest_response})
            SM.ContextHistory.save_context(message_history=message_history)
        except Exception as e:
            print(chat_id)
            print("ERROR WHILE SENDING REMINDER")



        

