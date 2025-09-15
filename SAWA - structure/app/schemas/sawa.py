"""
SAWA schemas implementing the CER + Toulmin framework
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.sawa_conversation import SAWAStage

class SAWAStartRequest(BaseModel):
    topic: str

class StudentResponse(BaseModel):
    conversation_id: int
    content: str

class SAWAResponse(BaseModel):
    message: str
    conversation_id: int
    current_stage: str
    stage_iteration: int
    should_continue: bool
    prep_sheet_ready: bool
    prep_sheet: Optional['PrepSheet'] = None

class PrepSheet(BaseModel):
    claim: str
    evidence_plan: str
    reasoning: str
    backing: str
    qualifier: str
    rebuttal_plan: str

class SAWAConversationResponse(BaseModel):
    id: int
    user_id: int
    topic: str
    current_stage: str
    stage_iteration: int
    claim_response: Optional[str] = None
    evidence_response: Optional[str] = None
    reasoning_response: Optional[str] = None
    backing_response: Optional[str] = None
    qualifier_response: Optional[str] = None
    rebuttal_response: Optional[str] = None
    claim_score: Optional[int] = None
    evidence_score: Optional[int] = None
    reasoning_score: Optional[int] = None
    backing_score: Optional[int] = None
    qualifier_score: Optional[int] = None
    rebuttal_score: Optional[int] = None
    prep_sheet_generated: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SAWAMessageResponse(BaseModel):
    id: int
    conversation_id: int
    message_type: str
    content: str
    stage: Optional[str] = None
    iteration: Optional[int] = None
    rubric_score: Optional[int] = None
    feedback_triggered: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SAWAHistoryResponse(BaseModel):
    conversation: SAWAConversationResponse
    messages: List[SAWAMessageResponse]

class RubricLevel(BaseModel):
    level: int
    level_name: str
    description: str
    example_responses: Optional[List[str]] = None
    socratic_prompts: Optional[List[str]] = None
    feedback_templates: Optional[List[str]] = None

class SAWARubricResponse(BaseModel):
    facet: str
    levels: List[RubricLevel]

class ReasoningScheme(BaseModel):
    scheme_type: str  # causal, correlation, expert_opinion, analogy, consequence
    description: str
    importance: List[str]
    socratic_prompts: List[str]
    examples: List[str]

class QualifierPattern(BaseModel):
    pattern_type: str
    description: str
    sentence_stems: List[str]
    examples: List[str]

class RebuttalStrategy(BaseModel):
    strategy_type: str
    description: str
    examples: List[str]
    response_templates: List[str]

# Update forward references
SAWAResponse.model_rebuild()
