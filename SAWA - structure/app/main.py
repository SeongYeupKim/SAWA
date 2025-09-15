"""
SAWA - Scientific Argumentative Writing Assistant
Main Application implementing the CER + Toulmin framework
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json

# Initialize FastAPI app
app = FastAPI(
    title="SAWA - Scientific Argumentative Writing Assistant",
    description="A pre-writing facilitator for scientific argumentative essays using CER + Toulmin framework",
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
    prep_sheet: Optional[Dict[str, str]] = None

# In-memory storage for demo
conversations = {}
conversation_counter = 1

# SAWA stages
SAWA_STAGES = ["claim", "evidence", "reasoning", "backing", "qualifier", "rebuttal"]

# Socratic questions for each stage
SOCRATIC_QUESTIONS = {
    "claim": [
        "What one-sentence position do you want to defend on this issue?",
        "Could you add a condition that makes it more precise?",
        "Make it contestable—something a critic might disagree with."
    ],
    "evidence": [
        "What specific information will you use to support your claim?",
        "Where does this evidence come from, and why should your audience trust it?",
        "Name at least one credible source type and why you trust it."
    ],
    "reasoning": [
        "How does this evidence support your claim?",
        "What general rule or mechanism makes the evidence count?",
        "Don't just repeat evidence—what rule makes it count for your claim?"
    ],
    "backing": [
        "What broader scientific principle supports your reasoning?",
        "Which established theory or model justifies this link?",
        "Name a theory, model, or consensus that makes your reasoning trustworthy."
    ],
    "qualifier": [
        "Is your claim always true, or under certain conditions?",
        "How confident are you in your claim, based on current evidence?",
        "Science rarely deals in absolutes—restate with 'likely,' 'generally,' or under specific conditions."
    ],
    "rebuttal": [
        "What is the strongest counterargument to your claim?",
        "What would a knowledgeable opponent say?",
        "Strengthen this by naming the strongest real counter a critic might raise."
    ]
}

# Feedback templates
FEEDBACK_TEMPLATES = {
    "claim": {
        1: "Make it contestable by stating a position someone could reasonably doubt.",
        2: "Could you add a condition that makes it more precise?"
    },
    "evidence": {
        1: "Name at least one source type and one criterion (e.g., peer review, sample size).",
        2: "Where does this evidence come from, and why should your audience trust it?"
    },
    "reasoning": {
        1: "State a general rule or mechanism linking the two.",
        2: "Don't just repeat evidence—what rule makes it count for your claim?"
    },
    "backing": {
        1: "Name a theory, model, or prior finding that justifies your rule.",
        2: "What broader scientific principle supports your reasoning?"
    },
    "qualifier": {
        1: "Calibrate scope using a condition or likelihood.",
        2: "Science rarely deals in absolutes—restate with 'likely,' 'generally,' or under specific conditions."
    },
    "rebuttal": {
        1: "Strengthen the counter by using the best opposing case.",
        2: "What would a knowledgeable opponent say?"
    }
}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SAWA - Scientific Argumentative Writing Assistant",
        "description": "A pre-writing facilitator for scientific argumentative essays using CER + Toulmin framework",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SAWA API"}

@app.post("/api/sawa/start", response_model=SAWAResponse)
async def start_sawa_conversation(request: SAWAStartRequest):
    """Start a new SAWA conversation with a scientific topic"""
    global conversation_counter
    
    conversation_id = conversation_counter
    conversation_counter += 1
    
    # Create conversation
    conversations[conversation_id] = {
        "topic": request.topic,
        "current_stage": "claim",
        "stage_iteration": 0,
        "responses": {},
        "scores": {}
    }
    
    # Get first Socratic question
    question = SOCRATIC_QUESTIONS["claim"][0]
    
    return SAWAResponse(
        message=question,
        conversation_id=conversation_id,
        current_stage="claim",
        stage_iteration=0,
        should_continue=True,
        prep_sheet_ready=False
    )

@app.post("/api/sawa/respond", response_model=SAWAResponse)
async def process_sawa_response(response: StudentResponse):
    """Process student response in SAWA conversation"""
    conversation_id = response.conversation_id
    
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation = conversations[conversation_id]
    current_stage = conversation["current_stage"]
    
    # Evaluate response (simplified scoring)
    score = evaluate_response(current_stage, response.content)
    conversation["scores"][current_stage] = score
    
    # Check if response meets threshold (Level 3+)
    if score >= 3:
        # Save response and advance to next stage
        conversation["responses"][current_stage] = response.content
        return advance_to_next_stage(conversation_id, conversation)
    else:
        # Provide feedback and re-ask question
        return provide_feedback_and_reask(conversation_id, conversation, score)

def evaluate_response(stage: str, response: str) -> int:
    """Evaluate student response using SAWA rubric (1-4 scale)"""
    response_lower = response.lower()
    
    if stage == "claim":
        # Level 1: Factual statement
        if any(word in response_lower for word in ["is a", "exists", "are", "is"]) and len(response.split()) < 10:
            return 1
        # Level 2: Vague
        if len(response.split()) < 15:
            return 2
        # Level 3: Clear, arguable
        if any(word in response_lower for word in ["suggest", "indicate", "show", "demonstrate"]):
            return 3
        # Level 4: Nuanced, scoped
        if any(word in response_lower for word in ["generally", "likely", "under", "conditions", "though"]):
            return 4
        return 3
    
    elif stage == "evidence":
        # Level 1: No evidence
        if len(response.split()) < 10:
            return 1
        # Level 2: One piece, limited
        if any(word in response_lower for word in ["study", "report", "data"]) and not any(word in response_lower for word in ["multiple", "several", "meta"]):
            return 2
        # Level 3: Multiple sources
        if any(word in response_lower for word in ["multiple", "several", "meta", "analysis", "peer"]):
            return 3
        # Level 4: Multiple sources with evaluation
        if any(word in response_lower for word in ["limitation", "bias", "credible", "reliable"]):
            return 4
        return 3
    
    elif stage == "reasoning":
        # Level 1: Restates evidence
        if any(phrase in response_lower for phrase in ["because the study", "the data shows"]):
            return 1
        # Level 2: Implicit reasoning
        if any(word in response_lower for word in ["if", "then", "because"]) and len(response.split()) < 20:
            return 2
        # Level 3: Explicit principle
        if any(word in response_lower for word in ["principle", "mechanism", "rule", "general"]):
            return 3
        # Level 4: Explicit, nuanced
        if any(word in response_lower for word in ["though", "however", "limitation", "assumption"]):
            return 4
        return 3
    
    elif stage == "backing":
        # Level 1: No backing
        if len(response.split()) < 10:
            return 1
        # Level 2: Vague appeal
        if any(phrase in response_lower for phrase in ["experts say", "scientists believe"]):
            return 2
        # Level 3: Explicit principle
        if any(word in response_lower for word in ["theory", "principle", "model", "consensus"]):
            return 3
        # Level 4: Explicit + evidence
        if any(word in response_lower for word in ["decades", "research", "evidence", "consensus"]):
            return 4
        return 3
    
    elif stage == "qualifier":
        # Level 1: Absolute
        if any(word in response_lower for word in ["always", "never", "all", "every", "prove"]):
            return 1
        # Level 2: Implicit
        if not any(word in response_lower for word in ["generally", "likely", "often", "usually"]):
            return 2
        # Level 3: Explicit conditional
        if any(word in response_lower for word in ["generally", "likely", "often", "usually"]):
            return 3
        # Level 4: Explicit with conditions
        if any(word in response_lower for word in ["under", "conditions", "though", "however"]):
            return 4
        return 3
    
    elif stage == "rebuttal":
        # Level 1: No counter
        if any(phrase in response_lower for phrase in ["no counter", "no argument", "everyone agrees"]):
            return 1
        # Level 2: Vague
        if any(phrase in response_lower for phrase in ["some people", "critics say"]) and len(response.split()) < 20:
            return 2
        # Level 3: Credible counter
        if any(word in response_lower for word in ["study", "research", "evidence", "however"]):
            return 3
        # Level 4: Strong counter with nuanced response
        if any(word in response_lower for word in ["limit", "scope", "concede", "though"]):
            return 4
        return 3
    
    return 3  # Default to proficient

def advance_to_next_stage(conversation_id: int, conversation: Dict[str, Any]) -> SAWAResponse:
    """Advance to the next stage in the sequence"""
    current_index = SAWA_STAGES.index(conversation["current_stage"])
    
    if current_index < len(SAWA_STAGES) - 1:
        # Move to next stage
        next_stage = SAWA_STAGES[current_index + 1]
        conversation["current_stage"] = next_stage
        conversation["stage_iteration"] = 0
        
        # Get Socratic question for next stage
        question = SOCRATIC_QUESTIONS[next_stage][0]
        
        return SAWAResponse(
            message=question,
            conversation_id=conversation_id,
            current_stage=next_stage,
            stage_iteration=0,
            should_continue=True,
            prep_sheet_ready=False
        )
    else:
        # All stages complete - generate prep sheet
        return generate_prep_sheet(conversation_id, conversation)

def provide_feedback_and_reask(conversation_id: int, conversation: Dict[str, Any], score: int) -> SAWAResponse:
    """Provide feedback and re-ask the same question"""
    current_stage = conversation["current_stage"]
    feedback = FEEDBACK_TEMPLATES[current_stage].get(score, "Please provide more detail.")
    
    # Increment iteration and get next question
    conversation["stage_iteration"] += 1
    question = SOCRATIC_QUESTIONS[current_stage][min(conversation["stage_iteration"], len(SOCRATIC_QUESTIONS[current_stage]) - 1)]
    
    return SAWAResponse(
        message=f"{feedback}\n\n{question}",
        conversation_id=conversation_id,
        current_stage=current_stage,
        stage_iteration=conversation["stage_iteration"],
        should_continue=True,
        prep_sheet_ready=False
    )

def generate_prep_sheet(conversation_id: int, conversation: Dict[str, Any]) -> SAWAResponse:
    """Generate the final prep sheet"""
    prep_sheet = {
        "claim": conversation["responses"].get("claim", ""),
        "evidence_plan": conversation["responses"].get("evidence", ""),
        "reasoning": conversation["responses"].get("reasoning", ""),
        "backing": conversation["responses"].get("backing", ""),
        "qualifier": conversation["responses"].get("qualifier", ""),
        "rebuttal_plan": conversation["responses"].get("rebuttal", "")
    }
    
    prep_sheet_text = f"""
🎉 **SAWA Prep Sheet Complete!**

**Claim:** {prep_sheet['claim']}

**Evidence Plan:** {prep_sheet['evidence_plan']}

**Reasoning (Warrant):** {prep_sheet['reasoning']}

**Backing:** {prep_sheet['backing']}

**Qualifier:** {prep_sheet['qualifier']}

**Rebuttal Plan:** {prep_sheet['rebuttal_plan']}

You're now ready to draft your scientific argumentative essay! Use this prep sheet as your roadmap.
"""
    
    return SAWAResponse(
        message=prep_sheet_text,
        conversation_id=conversation_id,
        current_stage="completed",
        stage_iteration=0,
        should_continue=False,
        prep_sheet_ready=True,
        prep_sheet=prep_sheet
    )

@app.get("/api/sawa/rubric/{facet}")
async def get_sawa_rubric(facet: str):
    """Get SAWA rubric for a specific facet"""
    # Simplified rubric for demo
    rubric = {
        "claim": {
            "levels": [
                {"level": 1, "name": "weak", "description": "No claim or factual statement"},
                {"level": 2, "name": "developing", "description": "Vague or simplistic claim"},
                {"level": 3, "name": "proficient", "description": "Clear, arguable, and specific claim"},
                {"level": 4, "name": "advanced", "description": "Nuanced, arguable, scoped claim"}
            ]
        },
        "evidence": {
            "levels": [
                {"level": 1, "name": "weak", "description": "No evidence or irrelevant fact"},
                {"level": 2, "name": "developing", "description": "One piece of evidence, limited specificity"},
                {"level": 3, "name": "proficient", "description": "Multiple relevant pieces of evidence"},
                {"level": 4, "name": "advanced", "description": "Multiple sources, triangulated, with evaluation"}
            ]
        },
        "reasoning": {
            "levels": [
                {"level": 1, "name": "weak", "description": "Restates evidence or claim without explanation"},
                {"level": 2, "name": "developing", "description": "Implicit or oversimplified reasoning"},
                {"level": 3, "name": "proficient", "description": "Explicit principle or mechanism links evidence to claim"},
                {"level": 4, "name": "advanced", "description": "Explicit, nuanced principle with acknowledgment of assumptions"}
            ]
        },
        "backing": {
            "levels": [
                {"level": 1, "name": "weak", "description": "No backing provided"},
                {"level": 2, "name": "developing", "description": "Vague appeal to authority"},
                {"level": 3, "name": "proficient", "description": "Explicit principle, theory, or prior study cited"},
                {"level": 4, "name": "advanced", "description": "Explicit principle plus supporting evidence or consensus"}
            ]
        },
        "qualifier": {
            "levels": [
                {"level": 1, "name": "weak", "description": "Absolute claim, no qualifier"},
                {"level": 2, "name": "developing", "description": "Implicit qualifier but vague"},
                {"level": 3, "name": "proficient", "description": "Explicit, conditional qualifier"},
                {"level": 4, "name": "advanced", "description": "Explicit qualifier with nuance tied to evidence limitations"}
            ]
        },
        "rebuttal": {
            "levels": [
                {"level": 1, "name": "weak", "description": "No counterargument mentioned"},
                {"level": 2, "name": "developing", "description": "Vague or strawman counterargument"},
                {"level": 3, "name": "proficient", "description": "Identifies a credible counter and offers a limited response"},
                {"level": 4, "name": "advanced", "description": "Identifies a strong counter and provides a principled, nuanced response strategy"}
            ]
        }
    }
    
    if facet not in rubric:
        raise HTTPException(status_code=404, detail=f"Rubric not found for facet: {facet}")
    
    return rubric[facet]

@app.get("/api/sawa/reasoning-schemes")
async def get_reasoning_schemes():
    """Get available reasoning schemes"""
    schemes = [
        {
            "scheme_type": "causal",
            "description": "Causal or mechanistic reasoning connects evidence to claims through cause–effect or mechanism explanations.",
            "importance": [
                "Establishes explanatory power beyond correlation",
                "Connects empirical findings to underlying scientific models",
                "Opens space for qualifiers (scope of mechanism)"
            ],
            "socratic_prompts": [
                "What cause–effect relationship explains why your evidence supports your claim?",
                "What mechanism connects this process to your claim?",
                "Could another cause explain the same evidence?",
                "What conditions are necessary for this cause–effect to hold?"
            ],
            "examples": [
                "GMO: 'If long-term feeding studies show no adverse effects, what biological mechanism explains why GMOs are safe?'",
                "Climate: 'If global temperatures rise, how does greenhouse gas trapping explain the warming mechanism?'"
            ]
        },
        {
            "scheme_type": "correlation",
            "description": "Correlation reasoning links patterns in data without specifying cause.",
            "importance": [
                "Useful for pattern detection",
                "Limited without causal justification",
                "Needs qualifiers to avoid overclaiming"
            ],
            "socratic_prompts": [
                "What pattern in the data supports your claim?",
                "How strong is the association?",
                "Could the pattern be explained by another factor?",
                "Does correlation prove causation here? Why or why not?"
            ],
            "examples": [
                "GMO: 'Feeding study animals showed no differences in weight—what pattern supports safety claims?'",
                "Climate: 'Temperature rise and CO₂ levels correlate—how do you avoid overstating causation?'"
            ]
        }
    ]
    return schemes

@app.get("/api/sawa/qualifier-patterns")
async def get_qualifier_patterns():
    """Get qualifier patterns and sentence stems"""
    patterns = [
        {
            "pattern_type": "certainty_scale",
            "description": "Certainty scale from absolute to conditional",
            "sentence_stems": [
                "In most cases, …",
                "Generally, …",
                "The evidence suggests that …",
                "It is likely that …",
                "This is true when …",
                "Under [specific condition], …"
            ],
            "examples": [
                "GMO: 'GMOs are generally safe for human health, though safety may vary depending on trait.'",
                "Climate: 'Human greenhouse gas emissions are very likely the primary cause of global warming since 1950.'"
            ]
        },
        {
            "pattern_type": "probability_scale",
            "description": "Probability scale from certain to unlikely",
            "sentence_stems": [
                "Certainly …",
                "Very likely …",
                "Likely …",
                "Possible …",
                "Unlikely …"
            ],
            "examples": [
                "Vaccines: 'mRNA vaccines reduce hospitalization risk by 80–95%, though effectiveness wanes over time.'"
            ]
        }
    ]
    return patterns

@app.get("/api/sawa/rebuttal-strategies")
async def get_rebuttal_strategies():
    """Get rebuttal strategies and response templates"""
    strategies = [
        {
            "strategy_type": "concede_with_boundary",
            "description": "Accept counter but limit its scope",
            "examples": [
                "Yes, some small studies found anomalies, but they are not generalizable.",
                "Some studies show enzyme changes. → Concede with boundary: effects exist but are inconsistent and small-scale."
            ],
            "response_templates": [
                "Although some evidence suggests __, these findings are limited because __.",
                "While __ is a concern, it does not outweigh the broader evidence supporting __."
            ]
        },
        {
            "strategy_type": "limit_scope",
            "description": "Restate claim with narrower conditions",
            "examples": [
                "Vaccines reduce hospitalizations within 6 months, though boosters are needed later.",
                "Effectiveness wanes after 6 months; I would qualify my claim by time and note boosters restore effectiveness."
            ],
            "response_templates": [
                "This claim may not hold in __ context, but in __ it remains valid.",
                "While __ is a concern, it does not outweigh the broader evidence supporting __."
            ]
        },
        {
            "strategy_type": "competing_mechanism",
            "description": "Propose alternative explanation for counter evidence",
            "examples": [
                "Temperature anomalies reflect natural variability, not the main warming trend.",
                "Natural variability explains short-term patterns, but attribution studies confirm long-term anthropogenic forcing."
            ],
            "response_templates": [
                "An alternative explanation is __, but current evidence more strongly supports __.",
                "While __ is a concern, it does not outweigh the broader evidence supporting __."
            ]
        },
        {
            "strategy_type": "challenge_credibility",
            "description": "Question reliability of counter evidence",
            "examples": [
                "This study had a small sample size and inconsistent methods.",
                "Some studies show enzyme differences in GMO-fed animals; I would limit my claim by noting small samples and inconsistent protocols."
            ],
            "response_templates": [
                "Some critics argue __, yet methodological weaknesses (e.g., __) reduce its credibility.",
                "While __ is a concern, it does not outweigh the broader evidence supporting __."
            ]
        }
    ]
    return strategies

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
