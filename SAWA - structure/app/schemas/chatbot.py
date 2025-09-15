"""
Chatbot schemas for SAWA application
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.conversation import ConversationStatus
from app.models.message import MessageType

class ConversationCreate(BaseModel):
    prompt_id: int

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    prompt_id: int
    status: ConversationStatus
    current_step: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    conversation_id: int
    content: str
    message_type: MessageType

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    message_type: MessageType
    content: str
    metadata: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChatbotResponse(BaseModel):
    message: str
    message_type: MessageType
    conversation_id: int
    next_step: str
    feedback: Optional[Dict[str, Any]] = None
    should_continue: bool = True

class StudentResponse(BaseModel):
    conversation_id: int
    content: str

class FeedbackAnalysis(BaseModel):
    argument_structure_score: Optional[float] = None
    evidence_quality_score: Optional[float] = None
    scientific_accuracy_score: Optional[float] = None
    clarity_score: Optional[float] = None
    overall_score: Optional[float] = None
    strengths: Optional[List[str]] = None
    areas_for_improvement: Optional[List[str]] = None
    specific_suggestions: Optional[List[str]] = None
    confidence_score: Optional[float] = None

class ConversationHistory(BaseModel):
    conversation: ConversationResponse
    messages: List[MessageResponse]
    feedback_analyses: List[FeedbackAnalysis]
