"""
AI service for OpenAI integration and scientific argument analysis
"""

import openai
from typing import Dict, Any, List
import json
import re

from app.core.config import settings

class AIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    def analyze_scientific_argument(self, prompt_content: str, student_response: str, expected_elements: str = None) -> Dict[str, Any]:
        """Analyze student's scientific argument using AI"""
        
        if not self.client:
            # Fallback to rule-based analysis if OpenAI is not available
            return self._rule_based_analysis(student_response)
        
        try:
            system_prompt = """You are an expert science educator specializing in scientific argumentation. 
            Analyze the student's response to a scientific prompt and provide detailed feedback.
            
            Evaluate the response on these criteria (0-10 scale):
            1. Argument Structure: Clear thesis, logical flow, proper organization
            2. Evidence Quality: Use of relevant scientific evidence, data, examples
            3. Scientific Accuracy: Correct scientific concepts and reasoning
            4. Clarity: Clear communication, appropriate language, coherence
            
            Provide:
            - Numerical scores for each criterion
            - Overall score (0-10)
            - List of strengths
            - List of areas for improvement
            - Specific suggestions for improvement
            - Confidence score (0-1) for your analysis
            
            Format your response as JSON with these exact keys:
            {
                "argument_structure_score": number,
                "evidence_quality_score": number,
                "scientific_accuracy_score": number,
                "clarity_score": number,
                "overall_score": number,
                "strengths": ["strength1", "strength2"],
                "areas_for_improvement": ["area1", "area2"],
                "specific_suggestions": ["suggestion1", "suggestion2"],
                "confidence_score": number
            }"""
            
            user_prompt = f"""
            PROMPT: {prompt_content}
            
            STUDENT RESPONSE: {student_response}
            
            EXPECTED ELEMENTS: {expected_elements or "Not specified"}
            
            Please analyze this student's response and provide detailed feedback.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse JSON response
            analysis_text = response.choices[0].message.content
            analysis = json.loads(analysis_text)
            
            return analysis
            
        except Exception as e:
            print(f"AI analysis failed: {e}")
            # Fallback to rule-based analysis
            return self._rule_based_analysis(student_response)

    def generate_additional_feedback(self, messages: List) -> str:
        """Generate additional contextual feedback based on conversation history"""
        
        if not self.client:
            return "I'd be happy to help you explore this topic further. What specific aspect would you like to discuss?"
        
        try:
            # Build conversation context
            conversation_context = []
            for message in messages[-6:]:  # Last 6 messages for context
                role = "assistant" if message.message_type.value.startswith("ai_") else "user"
                conversation_context.append(f"{role}: {message.content}")
            
            context_text = "\n".join(conversation_context)
            
            system_prompt = """You are a helpful science tutor. Based on the conversation history, 
            provide encouraging and constructive feedback to help the student continue learning. 
            Be supportive and guide them toward deeper understanding."""
            
            user_prompt = f"""
            Conversation history:
            {context_text}
            
            Provide helpful feedback to encourage continued learning and exploration.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Additional feedback generation failed: {e}")
            return "I'd be happy to help you explore this topic further. What specific aspect would you like to discuss?"

    def _rule_based_analysis(self, student_response: str) -> Dict[str, Any]:
        """Fallback rule-based analysis when AI is not available"""
        
        # Basic text analysis
        word_count = len(student_response.split())
        sentence_count = len(re.findall(r'[.!?]+', student_response))
        
        # Check for scientific indicators
        scientific_terms = ['hypothesis', 'evidence', 'data', 'experiment', 'theory', 'research', 'study', 'analysis']
        scientific_count = sum(1 for term in scientific_terms if term.lower() in student_response.lower())
        
        # Check for argument structure indicators
        argument_indicators = ['because', 'therefore', 'however', 'furthermore', 'moreover', 'consequently']
        argument_count = sum(1 for term in argument_indicators if term.lower() in student_response.lower())
        
        # Calculate scores based on heuristics
        structure_score = min(10, (argument_count * 2) + (sentence_count * 0.5))
        evidence_score = min(10, scientific_count * 2)
        clarity_score = min(10, word_count / 10)  # Assuming 100 words = 10 points
        accuracy_score = 7  # Default moderate score
        
        overall_score = (structure_score + evidence_score + clarity_score + accuracy_score) / 4
        
        # Generate basic feedback
        strengths = []
        improvements = []
        suggestions = []
        
        if structure_score >= 7:
            strengths.append("Good use of logical connectors and argument structure")
        else:
            improvements.append("Argument structure could be clearer")
            suggestions.append("Try using words like 'because', 'therefore', 'however' to connect ideas")
        
        if evidence_score >= 7:
            strengths.append("Good use of scientific terminology")
        else:
            improvements.append("Include more scientific evidence and terminology")
            suggestions.append("Reference specific studies, data, or scientific concepts")
        
        if clarity_score >= 7:
            strengths.append("Clear and well-explained response")
        else:
            improvements.append("Response could be more detailed")
            suggestions.append("Expand on your ideas with more explanation and examples")
        
        return {
            "argument_structure_score": round(structure_score, 1),
            "evidence_quality_score": round(evidence_score, 1),
            "scientific_accuracy_score": round(accuracy_score, 1),
            "clarity_score": round(clarity_score, 1),
            "overall_score": round(overall_score, 1),
            "strengths": strengths,
            "areas_for_improvement": improvements,
            "specific_suggestions": suggestions,
            "confidence_score": 0.6  # Lower confidence for rule-based analysis
        }
