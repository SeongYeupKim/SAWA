"""
Prompt model for SAWA application
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Prompt(Base):
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # e.g., "scientific_method", "argumentation", "evidence_evaluation"
    difficulty_level = Column(String, nullable=False)  # "beginner", "intermediate", "advanced"
    subject_area = Column(String, nullable=True)  # e.g., "biology", "chemistry", "physics"
    expected_elements = Column(Text, nullable=True)  # JSON string of expected argument elements
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="created_prompts")
    conversations = relationship("Conversation", back_populates="prompt")
