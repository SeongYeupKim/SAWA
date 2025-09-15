"""
SAWA Message model for tracking Socratic dialogue
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class MessageType(enum.Enum):
    SOCRATIC_QUESTION = "socratic_question"
    STUDENT_RESPONSE = "student_response"
    FEEDBACK_NUDGE = "feedback_nudge"
    PREP_SHEET = "prep_sheet"

class SAWAMessage(Base):
    __tablename__ = "sawa_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("sawa_conversations.id"), nullable=False)
    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    
    # Stage context
    stage = Column(String, nullable=True)  # Which SAWA stage this message belongs to
    iteration = Column(Integer, nullable=True)  # Which iteration within the stage
    
    # Evaluation context
    rubric_score = Column(Integer, nullable=True)  # 1-4 score if this was evaluated
    feedback_triggered = Column(Boolean, default=False)  # Whether this triggered feedback
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("SAWAConversation", back_populates="messages")
