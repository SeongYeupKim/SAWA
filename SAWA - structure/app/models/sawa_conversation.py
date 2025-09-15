"""
SAWA Conversation model implementing the CER + Toulmin framework
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class SAWAStage(enum.Enum):
    CLAIM = "claim"
    EVIDENCE = "evidence"
    REASONING = "reasoning"
    BACKING = "backing"
    QUALIFIER = "qualifier"
    REBUTTAL = "rebuttal"
    COMPLETED = "completed"

class SAWAConversation(Base):
    __tablename__ = "sawa_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String, nullable=False)  # The scientific topic being discussed
    
    # Current state
    current_stage = Column(Enum(SAWAStage), default=SAWAStage.CLAIM)
    stage_iteration = Column(Integer, default=0)  # How many times we've looped in current stage
    
    # Student responses for each stage
    claim_response = Column(Text, nullable=True)
    evidence_response = Column(Text, nullable=True)
    reasoning_response = Column(Text, nullable=True)
    backing_response = Column(Text, nullable=True)
    qualifier_response = Column(Text, nullable=True)
    rebuttal_response = Column(Text, nullable=True)
    
    # Rubric scores for each stage (1-4)
    claim_score = Column(Integer, nullable=True)
    evidence_score = Column(Integer, nullable=True)
    reasoning_score = Column(Integer, nullable=True)
    backing_score = Column(Integer, nullable=True)
    qualifier_score = Column(Integer, nullable=True)
    rebuttal_score = Column(Integer, nullable=True)
    
    # Prep sheet generation
    prep_sheet_generated = Column(Boolean, default=False)
    prep_sheet_content = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sawa_conversations")
    messages = relationship("SAWAMessage", back_populates="conversation", cascade="all, delete-orphan")
