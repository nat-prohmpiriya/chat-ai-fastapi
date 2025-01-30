from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from ..models.chat_model import Chat, Message, ChatSettings
from ..models.user_model import User

class ChatHistoryService:
    def __init__(self):
        pass
    
    async def create_conversation(self, user: User, settings: ChatSettings) -> Chat:
        """สร้าง conversation ใหม่"""
        conversation = Chat(
            user=user,
            conversation_id=str(uuid4()),
            settings=settings
        )
        await conversation.insert()
        return conversation
    
    async def add_message(self, conversation_id: str, message: Message) -> Chat:
        """เพิ่มข้อความใหม่ลงใน conversation"""
        conversation = await Chat.find_one({"conversation_id": conversation_id})
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
            
        conversation.messages.append(message)
        conversation.updated_at = datetime.utcnow()
        await conversation.save()
        return conversation
    
    async def get_conversation(self, conversation_id: str) -> Optional[Chat]:
        """ดึงข้อมูล conversation"""
        return await Chat.find_one({"conversation_id": conversation_id})
    
    async def get_user_conversations(self, user: User) -> List[Chat]:
        """ดึงประวัติการสนทนาทั้งหมดของผู้ใช้"""
        return await Chat.find({"user": user}).to_list()
    
    async def delete_conversation(self, conversation_id: str):
        """ลบ conversation"""
        conversation = await Chat.find_one({"conversation_id": conversation_id})
        if conversation:
            await conversation.delete()
