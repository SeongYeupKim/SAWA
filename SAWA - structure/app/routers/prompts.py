"""
Prompts API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.prompt import Prompt, PromptCreate, PromptUpdate, PromptWithStats
from app.models.prompt import Prompt as PromptModel
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Prompt])
async def get_prompts(
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty_level: Optional[str] = Query(None, description="Filter by difficulty level"),
    subject_area: Optional[str] = Query(None, description="Filter by subject area"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all available prompts with optional filtering"""
    query = db.query(PromptModel).filter(PromptModel.is_active == True)
    
    if category:
        query = query.filter(PromptModel.category == category)
    if difficulty_level:
        query = query.filter(PromptModel.difficulty_level == difficulty_level)
    if subject_area:
        query = query.filter(PromptModel.subject_area == subject_area)
    
    prompts = query.offset(skip).limit(limit).all()
    return prompts

@router.get("/{prompt_id}", response_model=Prompt)
async def get_prompt(
    prompt_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific prompt by ID"""
    prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.post("/", response_model=Prompt)
async def create_prompt(
    prompt_data: PromptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new prompt (teachers only)"""
    if not current_user.is_teacher:
        raise HTTPException(status_code=403, detail="Only teachers can create prompts")
    
    db_prompt = PromptModel(
        **prompt_data.dict(),
        created_by=current_user.id
    )
    
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    
    return db_prompt

@router.put("/{prompt_id}", response_model=Prompt)
async def update_prompt(
    prompt_id: int,
    prompt_data: PromptUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a prompt (teachers only)"""
    if not current_user.is_teacher:
        raise HTTPException(status_code=403, detail="Only teachers can update prompts")
    
    prompt = db.query(PromptModel).filter(PromptModel.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Update only provided fields
    update_data = prompt_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prompt, field, value)
    
    db.commit()
    db.refresh(prompt)
    
    return prompt

@router.get("/categories/list")
async def get_categories(db: Session = Depends(get_db)):
    """Get all available prompt categories"""
    categories = db.query(PromptModel.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

@router.get("/difficulty-levels/list")
async def get_difficulty_levels(db: Session = Depends(get_db)):
    """Get all available difficulty levels"""
    levels = db.query(PromptModel.difficulty_level).distinct().all()
    return [level[0] for level in levels if level[0]]

@router.get("/subject-areas/list")
async def get_subject_areas(db: Session = Depends(get_db)):
    """Get all available subject areas"""
    areas = db.query(PromptModel.subject_area).distinct().all()
    return [area[0] for area in areas if area[0]]
