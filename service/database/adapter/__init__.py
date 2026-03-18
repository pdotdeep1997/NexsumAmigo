

class DBAdapter():

    chat_id: str
    language: str

    def __init__(self, chat_id: str, language: str):
        self.chat_id = chat_id
        self.language = language
