"""
Feedback analysis model for SAWA application
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class FeedbackAnalysis(Base):
    __tablename__ = "feedback_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    # Scoring metrics
    argument_structure_score = Column(Float, nullable=True)  # 0-10
    evidence_quality_score = Column(Float, nullable=True)  # 0-10
    scientific_accuracy_score = Column(Float, nullable=True)  # 0-10
    clarity_score = Column(Float, nullable=True)  # 0-10
    overall_score = Column(Float, nullable=True)  # 0-10
    
    # Detailed feedback
    strengths = Column(Text, nullable=True)  # JSON string
    areas_for_improvement = Column(Text, nullable=True)  # JSON string
    specific_suggestions = Column(Text, nullable=True)  # JSON string
    
    # Analysis metadata
    analysis_method = Column(String, nullable=True)  # "ai_analysis", "rule_based", "hybrid"
    confidence_score = Column(Float, nullable=True)  # 0-1
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    message = relationship("Message")
    conversation = relationship("Conversation")
