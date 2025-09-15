"""
Analytics API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.conversation import Conversation
from app.models.feedback import FeedbackAnalysis
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/user/progress")
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's learning progress and statistics"""
    
    # Get user's conversations
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).all()
    
    # Get feedback analyses
    feedback_analyses = db.query(FeedbackAnalysis).join(
        Conversation
    ).filter(
        Conversation.user_id == current_user.id
    ).all()
    
    # Calculate statistics
    total_conversations = len(conversations)
    completed_conversations = len([c for c in conversations if c.status.value == "completed"])
    
    if feedback_analyses:
        avg_overall_score = sum(fa.overall_score for fa in feedback_analyses if fa.overall_score) / len([fa for fa in feedback_analyses if fa.overall_score])
        avg_structure_score = sum(fa.argument_structure_score for fa in feedback_analyses if fa.argument_structure_score) / len([fa for fa in feedback_analyses if fa.argument_structure_score])
        avg_evidence_score = sum(fa.evidence_quality_score for fa in feedback_analyses if fa.evidence_quality_score) / len([fa for fa in feedback_analyses if fa.evidence_quality_score])
        avg_clarity_score = sum(fa.clarity_score for fa in feedback_analyses if fa.clarity_score) / len([fa for fa in feedback_analyses if fa.clarity_score])
    else:
        avg_overall_score = 0
        avg_structure_score = 0
        avg_evidence_score = 0
        avg_clarity_score = 0
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_conversations = len([c for c in conversations if c.created_at >= thirty_days_ago])
    
    return {
        "total_conversations": total_conversations,
        "completed_conversations": completed_conversations,
        "completion_rate": completed_conversations / total_conversations if total_conversations > 0 else 0,
        "average_scores": {
            "overall": round(avg_overall_score, 2),
            "argument_structure": round(avg_structure_score, 2),
            "evidence_quality": round(avg_evidence_score, 2),
            "clarity": round(avg_clarity_score, 2)
        },
        "recent_activity": {
            "conversations_last_30_days": recent_conversations
        }
    }

@router.get("/user/feedback-history")
async def get_user_feedback_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's feedback history"""
    from app.services.feedback_service import FeedbackService
    
    feedback_service = FeedbackService(db)
    return feedback_service.get_feedback_history(current_user.id)

@router.get("/admin/overview")
async def get_admin_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system overview for admin users"""
    if not current_user.is_teacher:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Get system statistics
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_conversations = db.query(Conversation).count()
    completed_conversations = db.query(Conversation).filter(
        Conversation.status == "completed"
    ).count()
    
    # Recent activity
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_conversations = db.query(Conversation).filter(
        Conversation.created_at >= thirty_days_ago
    ).count()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users
        },
        "conversations": {
            "total": total_conversations,
            "completed": completed_conversations,
            "completion_rate": completed_conversations / total_conversations if total_conversations > 0 else 0,
            "recent_30_days": recent_conversations
        }
    }
