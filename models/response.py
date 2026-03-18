from pydantic import BaseModel, Field
from typing import Optional


class FromUser(BaseModel):
    id: int
    is_bot: bool
    first_name: str | None = None
    username: str | None = None


class Chat(BaseModel):
    id: int
    first_name: str | None = None
    username: str | None = None
    type: str


class MessageResult(BaseModel):
    message_id: int
    from_: FromUser = Field(..., alias="from")  # ✅ aliasing "from"
    chat: Chat
    date: int
    text: str


class TelegramSendMessageResponse(BaseModel):
    ok: bool
    result: MessageResult
