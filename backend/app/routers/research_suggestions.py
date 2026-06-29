from slowapi import Limiter
from slowapi.util import get_remote_address
limiter = Limiter(key_func=get_remote_address)
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from ..schemas.research_suggestions import ResearchSuggestionRequest, ResearchSuggestionResponse
from ..services.research_suggestions import research_suggestion_service
from ..services.credits import deduct_credits
from ..config import FEATURE_A_CREDITS
from ..services.auth import get_current_user
from ..models.user import User
from ..database import get_db

router = APIRouter(prefix="/api/literature", tags=["research-suggestions"])

@router.post("/research-suggestions", response_model=ResearchSuggestionResponse)
@limiter.limit("5/minute")
async def get_research_suggestions(
    request: Request,
    body: ResearchSuggestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-assisted research brainstorming suggestions."""
    # Pre-check credits
    if current_user.credits < FEATURE_A_CREDITS:
         raise HTTPException(status_code=402, detail="Payment Required: Insufficient credits.")

    try:
        response = research_suggestion_service.generate_suggestions(body)
    except Exception as e:
        error_msg = str(e)
        if "Internal Configuration" in error_msg:
             raise HTTPException(status_code=500, detail=error_msg)
        if "AI processing" in error_msg or "invalid structured data" in error_msg:
             raise HTTPException(status_code=502, detail=error_msg)
        raise HTTPException(status_code=500, detail="Unexpected error during processing.")

    # Deduct credits only if successful
    deduct_credits(db, current_user, FEATURE_A_CREDITS)
    return response
