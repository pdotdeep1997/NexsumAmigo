
from agents.amigo_hindi_agent.agent import execute_agent as execute_amigo_agent
from agents.amigo_question_hindi_agent.agent import execute_agent as execute_amigo_question_hint_agent

from agents.amigo_italian_agent.agent import execute_agent as execute_amigo_italian_agent
from agents.amigo_question_italian_agent.agent import execute_agent as execute_amigo_question_hint_italian_agent

from agents.amigo_spanish_agent.agent import execute_agent as execute_amigo_spanish_agent
from agents.amigo_question_spanish_agent.agent import execute_agent as execute_amigo_question_hint_spanish_agent

from agents.amigo_italian_baddie_agent.agent import execute_agent as execute_italian_baddie_agent
from agents.amigo_question_italian_baddie_agent.agent import execute_agent as execute_italian_question_hint_baddie_agent

from agents.amigo_hindi_flirty_agent.agent import execute_agent as execute_hindi_flirty_agent
from agents.amigo_question_hindi_flirty_agent.agent import execute_agent as execute_hindi_question_hint_flirty_agent


class AgentManger:

    def __init__(self, language):

        if language == 'hindi':
            self.message_agent_fn = execute_amigo_agent
            self.question_agent_fn  = execute_amigo_question_hint_agent 
            
        elif language == 'italian':
            self.message_agent_fn = execute_amigo_italian_agent
            self.question_agent_fn = execute_amigo_question_hint_italian_agent 

        elif language == 'spanish':
            self.message_agent_fn = execute_amigo_spanish_agent
            self.question_agent_fn = execute_amigo_question_hint_spanish_agent 

        elif language == 'flirtyitalian':
            self.message_agent_fn = execute_italian_baddie_agent
            self.question_agent_fn = execute_italian_question_hint_baddie_agent 

        elif language == 'flirtyhindi':
            self.message_agent_fn = execute_hindi_flirty_agent
            self.question_agent_fn = execute_hindi_question_hint_flirty_agent 

        self.language = language

    
    def execute_agent(self, **kwargs):
        return self.message_agent_fn(**kwargs)
    
    def execute_question_agent(self, **kwargs):
        return self.message_agent_fn(**kwargs)
        