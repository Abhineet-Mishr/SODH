from fastapi import APIRouter, HTTPException

from ..schemas.research_suggestions import ResearchSuggestionRequest, ResearchSuggestionResponse
from ..services.research_suggestions import research_suggestion_service
from ..services.credits import credit_service
from ..config import FEATURE_A_CREDITS

router = APIRouter(prefix="/api/literature", tags=["research-suggestions"])

@router.post("/research-suggestions", response_model=ResearchSuggestionResponse)
async def get_research_suggestions(request: ResearchSuggestionRequest):
    """Generate AI-assisted research brainstorming suggestions."""
    if credit_service.get_balance() < FEATURE_A_CREDITS:
         raise HTTPException(status_code=402, detail="Payment Required: Insufficient credits.")

    try:
        response = research_suggestion_service.generate_suggestions(request)
        return response
    except Exception as e:
        error_msg = str(e)
        if "Internal Configuration" in error_msg:
             raise HTTPException(status_code=500, detail=error_msg)
        if "AI processing" in error_msg or "invalid structured data" in error_msg:
             raise HTTPException(status_code=502, detail=error_msg)
        if "Insufficient credits" in error_msg:
             raise HTTPException(status_code=402, detail=error_msg)
        raise HTTPException(status_code=500, detail="Unexpected error during processing.")
