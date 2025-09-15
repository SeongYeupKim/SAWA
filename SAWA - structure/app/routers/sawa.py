"""
SAWA API endpoints implementing the CER + Toulmin framework
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.sawa import (
    SAWAStartRequest,
    StudentResponse,
    SAWAResponse,
    SAWAHistoryResponse,
    SAWAConversationResponse,
    SAWAMessageResponse,
    SAWARubricResponse,
    ReasoningScheme,
    QualifierPattern,
    RebuttalStrategy
)
from app.services.sawa_service import SAWAService
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/start", response_model=SAWAResponse)
async def start_sawa_conversation(
    request: SAWAStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new SAWA conversation with a scientific topic"""
    try:
        sawa_service = SAWAService(db)
        response = sawa_service.start_conversation(
            user_id=current_user.id,
            topic=request.topic
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting conversation: {str(e)}")

@router.post("/respond", response_model=SAWAResponse)
async def process_sawa_response(
    response: StudentResponse,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process student response in SAWA conversation"""
    try:
        sawa_service = SAWAService(db)
        sawa_response = sawa_service.process_response(
            conversation_id=response.conversation_id,
            response=response.content
        )
        return sawa_response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing response: {str(e)}")

@router.get("/history/{conversation_id}", response_model=SAWAHistoryResponse)
async def get_sawa_conversation_history(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complete SAWA conversation history"""
    try:
        sawa_service = SAWAService(db)
        history = sawa_service.get_conversation_history(conversation_id)
        return history
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@router.get("/conversations", response_model=List[SAWAConversationResponse])
async def get_user_sawa_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all SAWA conversations for the current user"""
    from app.models.sawa_conversation import SAWAConversation
    
    conversations = db.query(SAWAConversation).filter(
        SAWAConversation.user_id == current_user.id
    ).order_by(SAWAConversation.created_at.desc()).all()
    
    return conversations

@router.get("/rubric/{facet}", response_model=SAWARubricResponse)
async def get_sawa_rubric(
    facet: str,
    db: Session = Depends(get_db)
):
    """Get SAWA rubric for a specific facet"""
    from app.models.sawa_rubric import SAWARubric
    
    rubric_entries = db.query(SAWARubric).filter(
        SAWARubric.facet == facet
    ).order_by(SAWARubric.level).all()
    
    if not rubric_entries:
        raise HTTPException(status_code=404, detail=f"Rubric not found for facet: {facet}")
    
    levels = []
    for entry in rubric_entries:
        levels.append({
            "level": entry.level,
            "level_name": entry.level_name,
            "description": entry.description,
            "example_responses": entry.example_responses.split('\n') if entry.example_responses else [],
            "socratic_prompts": entry.socratic_prompts.split('\n') if entry.socratic_prompts else [],
            "feedback_templates": entry.feedback_templates.split('\n') if entry.feedback_templates else []
        })
    
    return SAWARubricResponse(facet=facet, levels=levels)

@router.get("/reasoning-schemes", response_model=List[ReasoningScheme])
async def get_reasoning_schemes():
    """Get available reasoning schemes"""
    schemes = [
        ReasoningScheme(
            scheme_type="causal",
            description="Causal or mechanistic reasoning connects evidence to claims through cause–effect or mechanism explanations.",
            importance=[
                "Establishes explanatory power beyond correlation",
                "Connects empirical findings to underlying scientific models",
                "Opens space for qualifiers (scope of mechanism)"
            ],
            socratic_prompts=[
                "What cause–effect relationship explains why your evidence supports your claim?",
                "What mechanism connects this process to your claim?",
                "Could another cause explain the same evidence?",
                "What conditions are necessary for this cause–effect to hold?"
            ],
            examples=[
                "GMO: 'If long-term feeding studies show no adverse effects, what biological mechanism explains why GMOs are safe?'",
                "Climate: 'If global temperatures rise, how does greenhouse gas trapping explain the warming mechanism?'"
            ]
        ),
        ReasoningScheme(
            scheme_type="correlation",
            description="Correlation reasoning links patterns in data without specifying cause.",
            importance=[
                "Useful for pattern detection",
                "Limited without causal justification",
                "Needs qualifiers to avoid overclaiming"
            ],
            socratic_prompts=[
                "What pattern in the data supports your claim?",
                "How strong is the association?",
                "Could the pattern be explained by another factor?",
                "Does correlation prove causation here? Why or why not?"
            ],
            examples=[
                "GMO: 'Feeding study animals showed no differences in weight—what pattern supports safety claims?'",
                "Climate: 'Temperature rise and CO₂ levels correlate—how do you avoid overstating causation?'"
            ]
        )
    ]
    return schemes

@router.get("/qualifier-patterns", response_model=List[QualifierPattern])
async def get_qualifier_patterns():
    """Get qualifier patterns and sentence stems"""
    patterns = [
        QualifierPattern(
            pattern_type="certainty_scale",
            description="Certainty scale from absolute to conditional",
            sentence_stems=[
                "In most cases, …",
                "Generally, …",
                "The evidence suggests that …",
                "It is likely that …",
                "This is true when …",
                "Under [specific condition], …"
            ],
            examples=[
                "GMO: 'GMOs are generally safe for human health, though safety may vary depending on trait.'",
                "Climate: 'Human greenhouse gas emissions are very likely the primary cause of global warming since 1950.'"
            ]
        ),
        QualifierPattern(
            pattern_type="probability_scale",
            description="Probability scale from certain to unlikely",
            sentence_stems=[
                "Certainly …",
                "Very likely …",
                "Likely …",
                "Possible …",
                "Unlikely …"
            ],
            examples=[
                "Vaccines: 'mRNA vaccines reduce hospitalization risk by 80–95%, though effectiveness wanes over time.'"
            ]
        )
    ]
    return patterns

@router.get("/rebuttal-strategies", response_model=List[RebuttalStrategy])
async def get_rebuttal_strategies():
    """Get rebuttal strategies and response templates"""
    strategies = [
        RebuttalStrategy(
            strategy_type="concede_with_boundary",
            description="Accept counter but limit its scope",
            examples=[
                "Yes, some small studies found anomalies, but they are not generalizable.",
                "Some studies show enzyme changes. → Concede with boundary: effects exist but are inconsistent and small-scale."
            ],
            response_templates=[
                "Although some evidence suggests __, these findings are limited because __.",
                "While __ is a concern, it does not outweigh the broader evidence supporting __."
            ]
        ),
        RebuttalStrategy(
            strategy_type="limit_scope",
            description="Restate claim with narrower conditions",
            examples=[
                "Vaccines reduce hospitalizations within 6 months, though boosters are needed later.",
                "Effectiveness wanes after 6 months; I would qualify my claim by time and note boosters restore effectiveness."
            ],
            response_templates=[
                "This claim may not hold in __ context, but in __ it remains valid.",
                "While __ is a concern, it does not outweigh the broader evidence supporting __."
            ]
        ),
        RebuttalStrategy(
            strategy_type="competing_mechanism",
            description="Propose alternative explanation for counter evidence",
            examples=[
                "Temperature anomalies reflect natural variability, not the main warming trend.",
                "Natural variability explains short-term patterns, but attribution studies confirm long-term anthropogenic forcing."
            ],
            response_templates=[
                "An alternative explanation is __, but current evidence more strongly supports __.",
                "While __ is a concern, it does not outweigh the broader evidence supporting __."
            ]
        ),
        RebuttalStrategy(
            strategy_type="challenge_credibility",
            description="Question reliability of counter evidence",
            examples=[
                "This study had a small sample size and inconsistent methods.",
                "Some studies show enzyme differences in GMO-fed animals; I would limit my claim by noting small samples and inconsistent protocols."
            ],
            response_templates=[
                "Some critics argue __, yet methodological weaknesses (e.g., __) reduce its credibility.",
                "While __ is a concern, it does not outweigh the broader evidence supporting __."
            ]
        )
    ]
    return strategies
