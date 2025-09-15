"""
Simplified SAWA application for testing without database
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json

# Initialize FastAPI app
app = FastAPI(
    title="SAWA - Scientific Argumentative Writing Assistant",
    description="A chatbot API to support students' preparation for scientific argumentative essays",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple data models
class Prompt(BaseModel):
    id: int
    title: str
    content: str
    category: str
    difficulty_level: str
    subject_area: Optional[str] = None

class StudentResponse(BaseModel):
    conversation_id: int
    content: str

class ChatbotResponse(BaseModel):
    message: str
    message_type: str
    conversation_id: int
    next_step: str
    feedback: Optional[Dict[str, Any]] = None
    should_continue: bool = True

# Sample data
SAMPLE_PROMPTS = [
    Prompt(
        id=1,
        title="Climate Change and Greenhouse Gases",
        content="Write a scientific argument about the role of greenhouse gases in climate change. Your argument should include: 1) A clear thesis statement, 2) Evidence from scientific studies, 3) Explanation of the greenhouse effect, 4) Discussion of human activities that contribute to greenhouse gas emissions, and 5) A conclusion that summarizes your position.",
        category="environmental_science",
        difficulty_level="intermediate",
        subject_area="environmental_science"
    ),
    Prompt(
        id=2,
        title="Evolution and Natural Selection",
        content="Present a scientific argument explaining how natural selection drives evolution. Your response should address: 1) The basic principles of natural selection, 2) Evidence for evolution from fossil records, 3) Examples of natural selection in action, 4) How genetic variation contributes to evolution, and 5) Why evolution is considered a scientific theory.",
        category="biology",
        difficulty_level="intermediate",
        subject_area="biology"
    )
]

# In-memory storage for demo
conversations = {}
conversation_counter = 1

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SAWA - Scientific Argumentative Writing Assistant",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SAWA API"}

@app.get("/api/prompts/", response_model=List[Prompt])
async def get_prompts():
    """Get all available prompts"""
    return SAMPLE_PROMPTS

@app.get("/api/prompts/{prompt_id}", response_model=Prompt)
async def get_prompt(prompt_id: int):
    """Get a specific prompt by ID"""
    for prompt in SAMPLE_PROMPTS:
        if prompt.id == prompt_id:
            return prompt
    raise HTTPException(status_code=404, detail="Prompt not found")

@app.post("/api/chatbot/start", response_model=ChatbotResponse)
async def start_conversation(prompt_id: int):
    """Start a new conversation with a prompt"""
    global conversation_counter
    
    # Find the prompt
    prompt = None
    for p in SAMPLE_PROMPTS:
        if p.id == prompt_id:
            prompt = p
            break
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Create conversation
    conversation_id = conversation_counter
    conversation_counter += 1
    
    conversations[conversation_id] = {
        "prompt_id": prompt_id,
        "step": "initial_prompt",
        "messages": []
    }
    
    return ChatbotResponse(
        message=prompt.content,
        message_type="ai_prompt",
        conversation_id=conversation_id,
        next_step="student_response",
        should_continue=True
    )

@app.post("/api/chatbot/respond", response_model=ChatbotResponse)
async def process_student_response(response: StudentResponse):
    """Process student's response to the initial prompt"""
    conversation_id = response.conversation_id
    
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation = conversations[conversation_id]
    
    if conversation["step"] != "initial_prompt":
        raise HTTPException(status_code=400, detail="Invalid conversation step")
    
    # Simple feedback generation
    feedback = generate_simple_feedback(response.content)
    
    # Update conversation
    conversation["step"] = "feedback"
    conversation["messages"].append({
        "type": "student_response",
        "content": response.content
    })
    
    return ChatbotResponse(
        message=feedback["feedback_text"],
        message_type="ai_feedback",
        conversation_id=conversation_id,
        next_step="continue_question",
        feedback=feedback,
        should_continue=True
    )

@app.post("/api/chatbot/continue/{conversation_id}", response_model=ChatbotResponse)
async def process_continue_response(conversation_id: int, response: str):
    """Process student's response to continue question"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation = conversations[conversation_id]
    
    # Check if student wants to continue
    should_continue = "yes" in response.lower() or "continue" in response.lower() or "more" in response.lower()
    
    if should_continue:
        additional_feedback = "Great! I'd be happy to help you explore this topic further. What specific aspect would you like to discuss?"
        conversation["step"] = "feedback"
    else:
        additional_feedback = "Thank you for using SAWA! Your conversation has been archived."
        conversation["step"] = "completed"
    
    return ChatbotResponse(
        message=additional_feedback,
        message_type="ai_feedback",
        conversation_id=conversation_id,
        next_step="completed" if not should_continue else "continue_question",
        should_continue=should_continue
    )

def generate_simple_feedback(content: str) -> Dict[str, Any]:
    """Generate simple feedback based on content analysis"""
    word_count = len(content.split())
    
    # Simple scoring based on content length and keywords
    scientific_terms = ['hypothesis', 'evidence', 'data', 'experiment', 'theory', 'research', 'study', 'analysis']
    scientific_count = sum(1 for term in scientific_terms if term.lower() in content.lower())
    
    argument_indicators = ['because', 'therefore', 'however', 'furthermore', 'moreover', 'consequently']
    argument_count = sum(1 for term in argument_indicators if term.lower() in content.lower())
    
    # Calculate scores
    structure_score = min(10, (argument_count * 2) + 5)
    evidence_score = min(10, scientific_count * 2 + 3)
    clarity_score = min(10, word_count / 10 + 5)
    overall_score = (structure_score + evidence_score + clarity_score) / 3
    
    # Generate feedback
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
    
    feedback_text = f"Thank you for your response! "
    if overall_score >= 8:
        feedback_text += "Excellent work! Your response demonstrates strong scientific argumentation skills."
    elif overall_score >= 6:
        feedback_text += "Good job! Your response shows solid understanding with room for improvement."
    else:
        feedback_text += "Your response shows some understanding, but there are several areas to work on."
    
    if strengths:
        feedback_text += f"\n\n**Strengths:**\n• " + "\n• ".join(strengths)
    
    if improvements:
        feedback_text += f"\n\n**Areas for Improvement:**\n• " + "\n• ".join(improvements)
    
    if suggestions:
        feedback_text += f"\n\n**Specific Suggestions:**\n• " + "\n• ".join(suggestions)
    
    return {
        "feedback_text": feedback_text,
        "scores": {
            "argument_structure": round(structure_score, 1),
            "evidence_quality": round(evidence_score, 1),
            "scientific_accuracy": 7.0,
            "clarity": round(clarity_score, 1),
            "overall": round(overall_score, 1)
        },
        "strengths": strengths,
        "areas_for_improvement": improvements,
        "specific_suggestions": suggestions
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
