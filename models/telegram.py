from typing import Union, Optional, Dict, Any
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


class Chat(BaseModel):
    id: int
    type: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Message(BaseModel):
    message_id: int
    from_: User = Field(..., alias="from")
    chat: Chat
    date: int
    text: Optional[str] = None


class CallbackQuery(BaseModel):
    id: str
    from_: User = Field(..., alias="from")
    chat_instance: str
    message: Message
    data: str


class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None



