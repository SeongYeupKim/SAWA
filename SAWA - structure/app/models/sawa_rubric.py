"""
SAWA Rubric model for storing evaluation criteria and examples
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class SAWARubric(Base):
    __tablename__ = "sawa_rubric"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Rubric facet
    facet = Column(String, nullable=False)  # claim, evidence, reasoning, backing, qualifier, rebuttal
    
    # Level information
    level = Column(Integer, nullable=False)  # 1-4
    level_name = Column(String, nullable=False)  # weak, developing, proficient, advanced
    
    # Description and examples
    description = Column(Text, nullable=False)
    example_responses = Column(Text, nullable=True)  # JSON string of example responses
    
    # Socratic prompts for this level
    socratic_prompts = Column(Text, nullable=True)  # JSON string of prompts
    
    # Feedback templates for this level
    feedback_templates = Column(Text, nullable=True)  # JSON string of feedback templates
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
