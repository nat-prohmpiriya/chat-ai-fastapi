from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..services.chat_service import ChatService
from ..services.chat_history_service import ChatHistoryService
from ..models.chat_model import ChatSettings, Message, Chat
from ..models.user_model import User
from ..middlewares.auth_middleware import get_current_user

router = APIRouter(prefix="/api/chat", tags=["chat"])
chat_service = ChatService()
chat_history_service = ChatHistoryService()

class ChatRequest(BaseModel):
    provider: str
    message: str
    conversation_id: Optional[str] = None
    config: Dict[str, Any] = {
        "temperature": 0.7,
        "max_tokens": 1000,
        "system_message": "You are a helpful assistant."
    }

class ChatResponse(BaseModel):
    message: str
    conversation_id: str

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    try:
        # สร้างหรือดึง conversation
        if not request.conversation_id:
            conversation = await chat_history_service.create_conversation(
                current_user,
                ChatSettings(**request.config)
            )
            conversation_id = conversation.conversation_id
        else:
            conversation_id = request.conversation_id
            
        # บันทึกข้อความของ user
        await chat_history_service.add_message(
            conversation_id,
            Message(role="user", content=request.message)
        )
        
        # ส่งข้อความไปยัง AI
        response = await chat_service.chat(
            provider=request.provider,
            message=request.message,
            config=request.config
        )
        
        # บันทึกข้อความของ AI
        await chat_history_service.add_message(
            conversation_id,
            Message(role="assistant", content=response)
        )
        
        return ChatResponse(message=response, conversation_id=conversation_id)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/conversations", response_model=List[Chat])
async def get_conversations(current_user: User = Depends(get_current_user)):
    """ดึงประวัติการสนทนาทั้งหมดของผู้ใช้"""
    return await chat_history_service.get_user_conversations(current_user)

@router.get("/conversations/{conversation_id}", response_model=Chat)
async def get_conversation(conversation_id: str, current_user: User = Depends(get_current_user)):
    """ดึงข้อมูลการสนทนาเฉพาะ conversation"""
    conversation = await chat_history_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this conversation")
    return conversation

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, current_user: User = Depends(get_current_user)):
    """ลบประวัติการสนทนา"""
    conversation = await chat_history_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conversation.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this conversation")
    await chat_history_service.delete_conversation(conversation_id)
    return {"message": "Conversation deleted"}
