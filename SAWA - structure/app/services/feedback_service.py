"""
Feedback service for analyzing student responses
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List
import json
import re

from app.models.feedback import FeedbackAnalysis
from app.models.conversation import Conversation
from app.models.prompt import Prompt
from app.services.ai_service import AIService

class FeedbackService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()

    def analyze_response(self, conversation_id: int, student_response: str) -> Dict[str, Any]:
        """Analyze student response and generate comprehensive feedback"""
        
        # Get conversation and prompt context
        conversation = self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ValueError("Conversation not found")
        
        prompt = self.db.query(Prompt).filter(
            Prompt.id == conversation.prompt_id
        ).first()
        
        # Use AI service for analysis
        ai_analysis = self.ai_service.analyze_scientific_argument(
            prompt_content=prompt.content,
            student_response=student_response,
            expected_elements=prompt.expected_elements
        )
        
        # Create feedback analysis record
        feedback_record = FeedbackAnalysis(
            conversation_id=conversation_id,
            argument_structure_score=ai_analysis.get("argument_structure_score"),
            evidence_quality_score=ai_analysis.get("evidence_quality_score"),
            scientific_accuracy_score=ai_analysis.get("scientific_accuracy_score"),
            clarity_score=ai_analysis.get("clarity_score"),
            overall_score=ai_analysis.get("overall_score"),
            strengths=json.dumps(ai_analysis.get("strengths", [])),
            areas_for_improvement=json.dumps(ai_analysis.get("areas_for_improvement", [])),
            specific_suggestions=json.dumps(ai_analysis.get("specific_suggestions", [])),
            analysis_method="ai_analysis",
            confidence_score=ai_analysis.get("confidence_score", 0.8)
        )
        self.db.add(feedback_record)
        self.db.commit()
        
        # Generate feedback text
        feedback_text = self._generate_feedback_text(ai_analysis)
        
        return {
            "feedback_text": feedback_text,
            "scores": {
                "argument_structure": ai_analysis.get("argument_structure_score"),
                "evidence_quality": ai_analysis.get("evidence_quality_score"),
                "scientific_accuracy": ai_analysis.get("scientific_accuracy_score"),
                "clarity": ai_analysis.get("clarity_score"),
                "overall": ai_analysis.get("overall_score")
            },
            "strengths": ai_analysis.get("strengths", []),
            "areas_for_improvement": ai_analysis.get("areas_for_improvement", []),
            "specific_suggestions": ai_analysis.get("specific_suggestions", []),
            "confidence_score": ai_analysis.get("confidence_score", 0.8)
        }

    def _generate_feedback_text(self, analysis: Dict[str, Any]) -> str:
        """Generate human-readable feedback text from analysis"""
        overall_score = analysis.get("overall_score", 0)
        strengths = analysis.get("strengths", [])
        improvements = analysis.get("areas_for_improvement", [])
        suggestions = analysis.get("specific_suggestions", [])
        
        feedback_parts = []
        
        # Overall assessment
        if overall_score >= 8:
            feedback_parts.append("Excellent work! Your response demonstrates strong scientific argumentation skills.")
        elif overall_score >= 6:
            feedback_parts.append("Good job! Your response shows solid understanding with room for improvement.")
        elif overall_score >= 4:
            feedback_parts.append("Your response shows some understanding, but there are several areas to work on.")
        else:
            feedback_parts.append("Your response needs significant improvement. Let's work on the fundamentals.")
        
        # Strengths
        if strengths:
            feedback_parts.append(f"\n**Strengths:**\n• " + "\n• ".join(strengths))
        
        # Areas for improvement
        if improvements:
            feedback_parts.append(f"\n**Areas for Improvement:**\n• " + "\n• ".join(improvements))
        
        # Specific suggestions
        if suggestions:
            feedback_parts.append(f"\n**Specific Suggestions:**\n• " + "\n• ".join(suggestions))
        
        return "\n".join(feedback_parts)

    def get_feedback_history(self, user_id: int) -> List[Dict[str, Any]]:
        """Get feedback history for a user"""
        feedback_analyses = self.db.query(FeedbackAnalysis).join(
            Conversation
        ).filter(
            Conversation.user_id == user_id
        ).order_by(FeedbackAnalysis.created_at.desc()).all()
        
        return [
            {
                "id": fa.id,
                "conversation_id": fa.conversation_id,
                "overall_score": fa.overall_score,
                "created_at": fa.created_at,
                "strengths": json.loads(fa.strengths) if fa.strengths else [],
                "areas_for_improvement": json.loads(fa.areas_for_improvement) if fa.areas_for_improvement else []
            }
            for fa in feedback_analyses
        ]
