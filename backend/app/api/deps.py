from functools import lru_cache
from app.services.toxicity_service import ToxicityService
from app.services.rewriter_service import RewriterService
from app.services.decision_engine import DecisionService

@lru_cache()
def get_toxicity_service() -> ToxicityService:
    return ToxicityService()

@lru_cache()
def get_rewriter_service() -> RewriterService:
    return RewriterService()

@lru_cache()
def get_decision_service() -> DecisionService:
    return DecisionService()
