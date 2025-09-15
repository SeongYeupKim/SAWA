"""
Chatbot service implementing the SAWA conversation flow
Following the preferred logic: AI presents prompt → Student responds → AI provides feedback → Option to continue
"""

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime
import json

from app.models.conversation import Conversation, ConversationStatus
from app.models.message import Message, MessageType
from app.models.prompt import Prompt
from app.models.feedback import FeedbackAnalysis
from app.schemas.chatbot import StudentResponse, ChatbotResponse, FeedbackAnalysis as FeedbackAnalysisSchema
from app.services.feedback_service import FeedbackService
from app.services.ai_service import AIService

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.feedback_service = FeedbackService(db)
        self.ai_service = AIService()

    def start_conversation(self, user_id: int, prompt_id: int) -> ChatbotResponse:
        """Start a new conversation with a prompt"""
        # Get the prompt
        prompt = self.db.query(Prompt).filter(Prompt.id == prompt_id).first()
        if not prompt:
            raise ValueError("Prompt not found")
        
        # Create conversation
        conversation = Conversation(
            user_id=user_id,
            prompt_id=prompt_id,
            status=ConversationStatus.ACTIVE,
            current_step="initial_prompt"
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        # Create initial AI prompt message
        ai_message = Message(
            conversation_id=conversation.id,
            message_type=MessageType.AI_PROMPT,
            content=prompt.content
        )
        self.db.add(ai_message)
        self.db.commit()
        
        return ChatbotResponse(
            message=prompt.content,
            message_type=MessageType.AI_PROMPT,
            conversation_id=conversation.id,
            next_step="student_response",
            should_continue=True
        )

    def process_student_response(self, response: StudentResponse) -> ChatbotResponse:
        """Process student's initial response and provide feedback"""
        # Get conversation
        conversation = self.db.query(Conversation).filter(
            Conversation.id == response.conversation_id
        ).first()
        if not conversation:
            raise ValueError("Conversation not found")
        
        if conversation.current_step != "initial_prompt":
            raise ValueError("Invalid conversation step")
        
        # Save student response
        student_message = Message(
            conversation_id=conversation.id,
            message_type=MessageType.STUDENT_RESPONSE,
            content=response.content
        )
        self.db.add(student_message)
        self.db.commit()
        self.db.refresh(student_message)
        
        # Generate feedback
        feedback_analysis = self.feedback_service.analyze_response(
            conversation_id=conversation.id,
            student_response=response.content
        )
        
        # Create AI feedback message
        feedback_message = Message(
            conversation_id=conversation.id,
            message_type=MessageType.AI_FEEDBACK,
            content=feedback_analysis.get("feedback_text", "Thank you for your response."),
            metadata=json.dumps(feedback_analysis)
        )
        self.db.add(feedback_message)
        
        # Update conversation step
        conversation.current_step = "feedback"
        self.db.commit()
        
        # Create continue question
        continue_question = self._generate_continue_question(feedback_analysis)
        continue_message = Message(
            conversation_id=conversation.id,
            message_type=MessageType.AI_CONTINUE_QUESTION,
            content=continue_question
        )
        self.db.add(continue_message)
        self.db.commit()
        
        return ChatbotResponse(
            message=feedback_analysis.get("feedback_text", "Thank you for your response."),
            message_type=MessageType.AI_FEEDBACK,
            conversation_id=conversation.id,
            next_step="continue_question",
            feedback=feedback_analysis,
            should_continue=True
        )

    def process_continue_response(self, conversation_id: int, response: str) -> ChatbotResponse:
        """Process student's response to continue question"""
        conversation = self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if not conversation:
            raise ValueError("Conversation not found")
        
        # Save student's continue response
        continue_response = Message(
            conversation_id=conversation.id,
            message_type=MessageType.STUDENT_CONTINUE_RESPONSE,
            content=response
        )
        self.db.add(continue_response)
        
        # Check if student wants to continue
        should_continue = self._parse_continue_response(response)
        
        if should_continue:
            # Generate additional feedback or questions
            additional_feedback = self._generate_additional_feedback(conversation_id)
            feedback_message = Message(
                conversation_id=conversation.id,
                message_type=MessageType.AI_FEEDBACK,
                content=additional_feedback
            )
            self.db.add(feedback_message)
            conversation.current_step = "feedback"
        else:
            # End conversation
            conversation.status = ConversationStatus.COMPLETED
            conversation.completed_at = datetime.utcnow()
            conversation.current_step = "completed"
        
        self.db.commit()
        
        return ChatbotResponse(
            message=additional_feedback if should_continue else "Thank you for using SAWA! Your conversation has been archived.",
            message_type=MessageType.AI_FEEDBACK,
            conversation_id=conversation.id,
            next_step="completed" if not should_continue else "continue_question",
            should_continue=should_continue
        )

    def _generate_continue_question(self, feedback_analysis: Dict[str, Any]) -> str:
        """Generate a question asking if student wants to continue"""
        return ("Based on my feedback, would you like to discuss more about this topic? "
                "You can ask questions, explore different aspects, or work on improving specific areas. "
                "Just let me know what you'd like to focus on next!")

    def _parse_continue_response(self, response: str) -> bool:
        """Parse student's response to determine if they want to continue"""
        response_lower = response.lower()
        continue_indicators = ["yes", "yeah", "sure", "continue", "more", "discuss", "explore", "help"]
        stop_indicators = ["no", "nope", "stop", "end", "finished", "done", "thanks", "thank you"]
        
        for indicator in continue_indicators:
            if indicator in response_lower:
                return True
        
        for indicator in stop_indicators:
            if indicator in response_lower:
                return False
        
        # Default to continue if unclear
        return True

    def _generate_additional_feedback(self, conversation_id: int) -> str:
        """Generate additional feedback based on conversation history"""
        # Get conversation messages
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        # Use AI service to generate contextual feedback
        return self.ai_service.generate_additional_feedback(messages)

    def get_conversation_history(self, conversation_id: int) -> Dict[str, Any]:
        """Get complete conversation history"""
        conversation = self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ValueError("Conversation not found")
        
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        feedback_analyses = self.db.query(FeedbackAnalysis).filter(
            FeedbackAnalysis.conversation_id == conversation_id
        ).all()
        
        return {
            "conversation": conversation,
            "messages": messages,
            "feedback_analyses": feedback_analyses
        }
