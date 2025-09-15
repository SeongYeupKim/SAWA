"""
Chatbot API endpoints implementing the SAWA conversation flow
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.chatbot import (
    ConversationCreate, 
    ConversationResponse, 
    StudentResponse, 
    ChatbotResponse,
    ConversationHistory
)
from app.services.chatbot_service import ChatbotService
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/start", response_model=ChatbotResponse)
async def start_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new conversation with a prompt"""
    try:
        chatbot_service = ChatbotService(db)
        response = chatbot_service.start_conversation(
            user_id=current_user.id,
            prompt_id=conversation_data.prompt_id
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/respond", response_model=ChatbotResponse)
async def process_student_response(
    response: StudentResponse,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process student's response to the initial prompt"""
    try:
        chatbot_service = ChatbotService(db)
        chatbot_response = chatbot_service.process_student_response(response)
        return chatbot_response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/continue/{conversation_id}", response_model=ChatbotResponse)
async def process_continue_response(
    conversation_id: int,
    response: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process student's response to continue question"""
    try:
        chatbot_service = ChatbotService(db)
        chatbot_response = chatbot_service.process_continue_response(
            conversation_id=conversation_id,
            response=response
        )
        return chatbot_response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/history/{conversation_id}", response_model=ConversationHistory)
async def get_conversation_history(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complete conversation history"""
    try:
        chatbot_service = ChatbotService(db)
        history = chatbot_service.get_conversation_history(conversation_id)
        return history
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_user_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user"""
    from app.models.conversation import Conversation
    
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).order_by(Conversation.created_at.desc()).all()
    
    return conversations
