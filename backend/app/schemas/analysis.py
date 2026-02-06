from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class AnalysisRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class AnalysisResult(BaseModel):
    label: str
    score: float
    severity: float

class AnalysisResponse(BaseModel):
    analysis: AnalysisResult
    action: str
    reason: str
    rewrite: Optional[str] = None
    timestamp: str
