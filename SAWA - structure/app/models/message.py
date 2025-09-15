"""
Message model for SAWA application
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class MessageType(enum.Enum):
    AI_PROMPT = "ai_prompt"
    STUDENT_RESPONSE = "student_response"
    AI_FEEDBACK = "ai_feedback"
    AI_CONTINUE_QUESTION = "ai_continue_question"
    STUDENT_CONTINUE_RESPONSE = "student_continue_response"

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(Text, nullable=True)  # JSON string for additional data (e.g., feedback scores, analysis)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
