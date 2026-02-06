from fastapi import APIRouter, Depends, HTTPException
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.toxicity_service import ToxicityService
from app.services.rewriter_service import RewriterService
from app.services.decision_engine import DecisionService
from app.api.deps import get_toxicity_service, get_rewriter_service, get_decision_service
from datetime import datetime
from app.core.logging import logger

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_message(
    request: AnalysisRequest,
    toxicity_service: ToxicityService = Depends(get_toxicity_service),
    rewriter_service: RewriterService = Depends(get_rewriter_service),
    decision_service: DecisionService = Depends(get_decision_service)
):
    try:
        # 1. Analyze
        analysis_result = toxicity_service.analyze(request.message)
        
        # 2. Decide
        action, reason = decision_service.decide(analysis_result, request.user_id)
        
        # 3. Rewrite if needed
        rewritten_text = None
        if action in ["block_and_rewrite", "warn", "block_and_alert"]:
            rewritten_text = rewriter_service.rewrite(request.message)
            
        return AnalysisResponse(
            analysis=analysis_result,
            action=action,
            reason=reason,
            rewrite=rewritten_text,
            timestamp=datetime.now().isoformat()
        )
            
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
