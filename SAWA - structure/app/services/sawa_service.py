"""
SAWA Service implementing the CER + Toulmin framework with Socratic questioning
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from app.models.sawa_conversation import SAWAConversation, SAWAStage
from app.models.sawa_message import SAWAMessage, MessageType
from app.models.sawa_rubric import SAWARubric
from app.schemas.sawa import SAWAResponse, StudentResponse, PrepSheet

class SAWAService:
    def __init__(self, db: Session):
        self.db = db
        self.stage_sequence = [
            SAWAStage.CLAIM,
            SAWAStage.EVIDENCE,
            SAWAStage.REASONING,
            SAWAStage.BACKING,
            SAWAStage.QUALIFIER,
            SAWAStage.REBUTTAL
        ]

    def start_conversation(self, user_id: int, topic: str) -> SAWAResponse:
        """Start a new SAWA conversation"""
        conversation = SAWAConversation(
            user_id=user_id,
            topic=topic,
            current_stage=SAWAStage.CLAIM,
            stage_iteration=0
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        # Get the first Socratic question
        question = self._get_socratic_question(SAWAStage.CLAIM, 0)
        
        # Create message
        message = SAWAMessage(
            conversation_id=conversation.id,
            message_type=MessageType.SOCRATIC_QUESTION,
            content=question,
            stage=SAWAStage.CLAIM.value,
            iteration=0
        )
        self.db.add(message)
        self.db.commit()
        
        return SAWAResponse(
            message=question,
            conversation_id=conversation.id,
            current_stage=SAWAStage.CLAIM.value,
            stage_iteration=0,
            should_continue=True,
            prep_sheet_ready=False
        )

    def process_response(self, conversation_id: int, response: str) -> SAWAResponse:
        """Process student response and determine next action"""
        conversation = self.db.query(SAWAConversation).filter(
            SAWAConversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ValueError("Conversation not found")
        
        # Save student response
        message = SAWAMessage(
            conversation_id=conversation.id,
            message_type=MessageType.STUDENT_RESPONSE,
            content=response,
            stage=conversation.current_stage.value,
            iteration=conversation.stage_iteration
        )
        self.db.add(message)
        
        # Evaluate response using rubric
        score = self._evaluate_response(conversation.current_stage, response)
        message.rubric_score = score
        
        # Check if response meets threshold (Level 2.5+)
        if score >= 3:  # Proficient or Advanced
            # Save response and advance to next stage
            self._save_stage_response(conversation, response, score)
            return self._advance_to_next_stage(conversation)
        else:
            # Provide feedback and re-ask question
            message.feedback_triggered = True
            self.db.commit()
            return self._provide_feedback_and_reask(conversation, score)

    def _evaluate_response(self, stage: SAWAStage, response: str) -> int:
        """Evaluate student response using SAWA rubric (1-4 scale)"""
        # This is a simplified evaluation - in production, you'd use AI or more sophisticated NLP
        response_lower = response.lower()
        
        if stage == SAWAStage.CLAIM:
            return self._evaluate_claim(response)
        elif stage == SAWAStage.EVIDENCE:
            return self._evaluate_evidence(response)
        elif stage == SAWAStage.REASONING:
            return self._evaluate_reasoning(response)
        elif stage == SAWAStage.BACKING:
            return self._evaluate_backing(response)
        elif stage == SAWAStage.QUALIFIER:
            return self._evaluate_qualifier(response)
        elif stage == SAWAStage.REBUTTAL:
            return self._evaluate_rebuttal(response)
        
        return 1  # Default to weak

    def _evaluate_claim(self, response: str) -> int:
        """Evaluate claim response (Level 1-4)"""
        response_lower = response.lower()
        
        # Level 1: Factual statement, not arguable
        if any(word in response_lower for word in ["is a", "exists", "are", "is"]):
            if len(response.split()) < 10:  # Very short, likely factual
                return 1
        
        # Level 2: Vague or simplistic
        if len(response.split()) < 15:
            return 2
        
        # Level 3: Clear, arguable, specific
        if any(word in response_lower for word in ["suggest", "indicate", "show", "demonstrate"]):
            return 3
        
        # Level 4: Nuanced, scoped, condition-aware
        if any(word in response_lower for word in ["generally", "likely", "under", "conditions", "though", "however"]):
            return 4
        
        return 3  # Default to proficient

    def _evaluate_evidence(self, response: str) -> int:
        """Evaluate evidence response (Level 1-4)"""
        response_lower = response.lower()
        
        # Level 1: No evidence or irrelevant
        if len(response.split()) < 10:
            return 1
        
        # Level 2: One piece, limited specificity
        if any(word in response_lower for word in ["study", "report", "data"]):
            if not any(word in response_lower for word in ["multiple", "several", "meta", "analysis"]):
                return 2
        
        # Level 3: Multiple sources, some evaluation
        if any(word in response_lower for word in ["multiple", "several", "meta", "analysis", "peer", "review"]):
            return 3
        
        # Level 4: Multiple sources, explicit evaluation
        if any(word in response_lower for word in ["limitation", "bias", "credible", "reliable", "evaluation"]):
            return 4
        
        return 3

    def _evaluate_reasoning(self, response: str) -> int:
        """Evaluate reasoning response (Level 1-4)"""
        response_lower = response.lower()
        
        # Level 1: Restates evidence/claim
        if any(phrase in response_lower for phrase in ["because the study", "the data shows", "as shown"]):
            return 1
        
        # Level 2: Implicit reasoning
        if any(word in response_lower for word in ["if", "then", "because"]):
            if len(response.split()) < 20:
                return 2
        
        # Level 3: Explicit principle
        if any(word in response_lower for word in ["principle", "mechanism", "rule", "general"]):
            return 3
        
        # Level 4: Explicit, nuanced principle
        if any(word in response_lower for word in ["though", "however", "limitation", "assumption"]):
            return 4
        
        return 3

    def _evaluate_backing(self, response: str) -> int:
        """Evaluate backing response (Level 1-4)"""
        response_lower = response.lower()
        
        # Level 1: No backing
        if len(response.split()) < 10:
            return 1
        
        # Level 2: Vague appeal to authority
        if any(phrase in response_lower for phrase in ["experts say", "scientists believe", "studies show"]):
            return 2
        
        # Level 3: Explicit principle/theory
        if any(word in response_lower for word in ["theory", "principle", "model", "consensus"]):
            return 3
        
        # Level 4: Explicit principle + evidence
        if any(word in response_lower for word in ["decades", "research", "evidence", "consensus"]):
            return 4
        
        return 3

    def _evaluate_qualifier(self, response: str) -> int:
        """Evaluate qualifier response (Level 1-4)"""
        response_lower = response.lower()
        
        # Level 1: Absolute claim
        if any(word in response_lower for word in ["always", "never", "all", "every", "prove", "guarantee"]):
            return 1
        
        # Level 2: Implicit qualifier
        if not any(word in response_lower for word in ["generally", "likely", "often", "usually", "under"]):
            return 2
        
        # Level 3: Explicit conditional
        if any(word in response_lower for word in ["generally", "likely", "often", "usually"]):
            return 3
        
        # Level 4: Explicit with conditions
        if any(word in response_lower for word in ["under", "conditions", "though", "however", "may vary"]):
            return 4
        
        return 3

    def _evaluate_rebuttal(self, response: str) -> int:
        """Evaluate rebuttal response (Level 1-4)"""
        response_lower = response.lower()
        
        # Level 1: No counterargument
        if any(phrase in response_lower for phrase in ["no counter", "no argument", "everyone agrees"]):
            return 1
        
        # Level 2: Vague or strawman
        if any(phrase in response_lower for phrase in ["some people", "critics say", "opponents argue"]):
            if len(response.split()) < 20:
                return 2
        
        # Level 3: Credible counter with response
        if any(word in response_lower for word in ["study", "research", "evidence", "however", "but"]):
            return 3
        
        # Level 4: Strong counter with nuanced response
        if any(word in response_lower for word in ["limit", "scope", "concede", "though", "however"]):
            return 4
        
        return 3

    def _get_socratic_question(self, stage: SAWAStage, iteration: int) -> str:
        """Get Socratic question for the current stage"""
        questions = {
            SAWAStage.CLAIM: [
                "What one-sentence position do you want to defend on this issue?",
                "Could you add a condition that makes it more precise?",
                "Make it contestable—something a critic might disagree with."
            ],
            SAWAStage.EVIDENCE: [
                "What specific information will you use to support your claim?",
                "Where does this evidence come from, and why should your audience trust it?",
                "Name at least one credible source type and why you trust it."
            ],
            SAWAStage.REASONING: [
                "How does this evidence support your claim?",
                "What general rule or mechanism makes the evidence count?",
                "Don't just repeat evidence—what rule makes it count for your claim?"
            ],
            SAWAStage.BACKING: [
                "What broader scientific principle supports your reasoning?",
                "Which established theory or model justifies this link?",
                "Name a theory, model, or consensus that makes your reasoning trustworthy."
            ],
            SAWAStage.QUALIFIER: [
                "Is your claim always true, or under certain conditions?",
                "How confident are you in your claim, based on current evidence?",
                "Science rarely deals in absolutes—restate with 'likely,' 'generally,' or under specific conditions."
            ],
            SAWAStage.REBUTTAL: [
                "What is the strongest counterargument to your claim?",
                "What would a knowledgeable opponent say?",
                "Strengthen this by naming the strongest real counter a critic might raise."
            ]
        }
        
        stage_questions = questions.get(stage, ["Please elaborate on your response."])
        return stage_questions[min(iteration, len(stage_questions) - 1)]

    def _get_feedback_nudge(self, stage: SAWAStage, score: int) -> str:
        """Get feedback nudge based on stage and score"""
        feedback_templates = {
            SAWAStage.CLAIM: {
                1: "Make it contestable by stating a position someone could reasonably doubt.",
                2: "Could you add a condition that makes it more precise?"
            },
            SAWAStage.EVIDENCE: {
                1: "Name at least one source type and one criterion (e.g., peer review, sample size).",
                2: "Where does this evidence come from, and why should your audience trust it?"
            },
            SAWAStage.REASONING: {
                1: "State a general rule or mechanism linking the two.",
                2: "Don't just repeat evidence—what rule makes it count for your claim?"
            },
            SAWAStage.BACKING: {
                1: "Name a theory, model, or prior finding that justifies your rule.",
                2: "What broader scientific principle supports your reasoning?"
            },
            SAWAStage.QUALIFIER: {
                1: "Calibrate scope using a condition or likelihood.",
                2: "Science rarely deals in absolutes—restate with 'likely,' 'generally,' or under specific conditions."
            },
            SAWAStage.REBUTTAL: {
                1: "Strengthen the counter by using the best opposing case.",
                2: "What would a knowledgeable opponent say?"
            }
        }
        
        stage_feedback = feedback_templates.get(stage, {})
        return stage_feedback.get(score, "Please provide more detail.")

    def _save_stage_response(self, conversation: SAWAConversation, response: str, score: int):
        """Save student response for the current stage"""
        if conversation.current_stage == SAWAStage.CLAIM:
            conversation.claim_response = response
            conversation.claim_score = score
        elif conversation.current_stage == SAWAStage.EVIDENCE:
            conversation.evidence_response = response
            conversation.evidence_score = score
        elif conversation.current_stage == SAWAStage.REASONING:
            conversation.reasoning_response = response
            conversation.reasoning_score = score
        elif conversation.current_stage == SAWAStage.BACKING:
            conversation.backing_response = response
            conversation.backing_score = score
        elif conversation.current_stage == SAWAStage.QUALIFIER:
            conversation.qualifier_response = response
            conversation.qualifier_score = score
        elif conversation.current_stage == SAWAStage.REBUTTAL:
            conversation.rebuttal_response = response
            conversation.rebuttal_score = score

    def _advance_to_next_stage(self, conversation: SAWAConversation) -> SAWAResponse:
        """Advance to the next stage in the sequence"""
        current_index = self.stage_sequence.index(conversation.current_stage)
        
        if current_index < len(self.stage_sequence) - 1:
            # Move to next stage
            next_stage = self.stage_sequence[current_index + 1]
            conversation.current_stage = next_stage
            conversation.stage_iteration = 0
            
            # Get Socratic question for next stage
            question = self._get_socratic_question(next_stage, 0)
            
            # Create message
            message = SAWAMessage(
                conversation_id=conversation.id,
                message_type=MessageType.SOCRATIC_QUESTION,
                content=question,
                stage=next_stage.value,
                iteration=0
            )
            self.db.add(message)
            self.db.commit()
            
            return SAWAResponse(
                message=question,
                conversation_id=conversation.id,
                current_stage=next_stage.value,
                stage_iteration=0,
                should_continue=True,
                prep_sheet_ready=False
            )
        else:
            # All stages complete - generate prep sheet
            return self._generate_prep_sheet(conversation)

    def _provide_feedback_and_reask(self, conversation: SAWAConversation, score: int) -> SAWAResponse:
        """Provide feedback and re-ask the same question"""
        feedback = self._get_feedback_nudge(conversation.current_stage, score)
        
        # Create feedback message
        feedback_message = SAWAMessage(
            conversation_id=conversation.id,
            message_type=MessageType.FEEDBACK_NUDGE,
            content=feedback,
            stage=conversation.current_stage.value,
            iteration=conversation.stage_iteration,
            feedback_triggered=True
        )
        self.db.add(feedback_message)
        
        # Increment iteration and get next question
        conversation.stage_iteration += 1
        question = self._get_socratic_question(conversation.current_stage, conversation.stage_iteration)
        
        # Create next question message
        question_message = SAWAMessage(
            conversation_id=conversation.id,
            message_type=MessageType.SOCRATIC_QUESTION,
            content=question,
            stage=conversation.current_stage.value,
            iteration=conversation.stage_iteration
        )
        self.db.add(question_message)
        self.db.commit()
        
        return SAWAResponse(
            message=f"{feedback}\n\n{question}",
            conversation_id=conversation.id,
            current_stage=conversation.current_stage.value,
            stage_iteration=conversation.stage_iteration,
            should_continue=True,
            prep_sheet_ready=False
        )

    def _generate_prep_sheet(self, conversation: SAWAConversation) -> SAWAResponse:
        """Generate the final prep sheet"""
        prep_sheet = PrepSheet(
            claim=conversation.claim_response or "",
            evidence_plan=conversation.evidence_response or "",
            reasoning=conversation.reasoning_response or "",
            backing=conversation.backing_response or "",
            qualifier=conversation.qualifier_response or "",
            rebuttal_plan=conversation.rebuttal_response or ""
        )
        
        # Save prep sheet
        conversation.prep_sheet_generated = True
        conversation.prep_sheet_content = prep_sheet.json()
        conversation.current_stage = SAWAStage.COMPLETED
        conversation.completed_at = datetime.utcnow()
        
        # Create prep sheet message
        message = SAWAMessage(
            conversation_id=conversation.id,
            message_type=MessageType.PREP_SHEET,
            content=prep_sheet.json(),
            stage=SAWAStage.COMPLETED.value
        )
        self.db.add(message)
        self.db.commit()
        
        prep_sheet_text = f"""
🎉 **SAWA Prep Sheet Complete!**

**Claim:** {prep_sheet.claim}

**Evidence Plan:** {prep_sheet.evidence_plan}

**Reasoning (Warrant):** {prep_sheet.reasoning}

**Backing:** {prep_sheet.backing}

**Qualifier:** {prep_sheet.qualifier}

**Rebuttal Plan:** {prep_sheet.rebuttal_plan}

You're now ready to draft your scientific argumentative essay! Use this prep sheet as your roadmap.
"""
        
        return SAWAResponse(
            message=prep_sheet_text,
            conversation_id=conversation.id,
            current_stage=SAWAStage.COMPLETED.value,
            stage_iteration=0,
            should_continue=False,
            prep_sheet_ready=True,
            prep_sheet=prep_sheet
        )

    def get_conversation_history(self, conversation_id: int) -> Dict[str, Any]:
        """Get complete conversation history"""
        conversation = self.db.query(SAWAConversation).filter(
            SAWAConversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise ValueError("Conversation not found")
        
        messages = self.db.query(SAWAMessage).filter(
            SAWAMessage.conversation_id == conversation_id
        ).order_by(SAWAMessage.created_at).all()
        
        return {
            "conversation": conversation,
            "messages": messages
        }
