from service.database.adapter.all_users import AllUsersDBAdapter
from service.state_machine.manager import StateMachine
from service.telegram.telegram_manager import TelegramManager
from service.question_manager.question_manager import QuestionManager
from service.agent.manager import AgentManger

def process_reminders():

    forgotton_users = AllUsersDBAdapter().get_all_forgotten_users()