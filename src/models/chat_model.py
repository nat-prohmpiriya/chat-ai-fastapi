from datetime import datetime
from typing import List, Dict, Optional
from beanie import Document, Link
from pydantic import BaseModel
from .user_model import User

class Message(BaseModel):
    role: str  # "user" หรือ "assistant"
    content: str
    provider: Optional[str] = None  # สำหรับ response จาก AI
    timestamp: datetime = datetime.utcnow()

class ChatSettings(BaseModel):
    temperature: float = 0.7
    max_tokens: int = 1000
    system_message: str = "You are a helpful assistant."

class Chat(Document):
    user: Link[User]
    conversation_id: str
    messages: List[Message] = []
    settings: ChatSettings
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Settings:
        name = "chats"
        
    class Config:
        arbitrary_types_allowed = True
