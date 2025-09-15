"""
Prompt schemas for SAWA application
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class PromptBase(BaseModel):
    title: str
    content: str
    category: str
    difficulty_level: str
    subject_area: Optional[str] = None
    expected_elements: Optional[str] = None

class PromptCreate(PromptBase):
    pass

class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    subject_area: Optional[str] = None
    expected_elements: Optional[str] = None
    is_active: Optional[bool] = None

class PromptInDB(PromptBase):
    id: int
    created_by: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Prompt(PromptInDB):
    pass

class PromptWithStats(Prompt):
    usage_count: int
    average_score: Optional[float] = None
    completion_rate: Optional[float] = None
