from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from analyzer import ToxicityAnalyzer
from rewriter import MessageRewriter
import decision_engine

# Initialize FastAPI app
app = FastAPI(
    title="SafeSpeak API",
    description="AI Guardian for Children's Online Communication",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific extension ID or domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
analyzer = None
rewriter = None

@app.on_event("startup")
def load_models():
    """
    Load AI models on startup to avoid reloading per request.
    """
    global analyzer, rewriter
    try:
        analyzer = ToxicityAnalyzer()
        rewriter = MessageRewriter()
    except Exception as e:
        print(f"CRITICAL ERROR LOADING MODELS: {e}")

# Input model
class AnalyzeRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

# Output model
class AnalysisResponse(BaseModel):
    analysis: dict
    action: str
    reason: str
    rewrite: Optional[str] = None
    timestamp: str

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_message(request: AnalyzeRequest):
    """
    Analyze a message for toxicity and determine the appropriate action.
    """
    global analyzer, rewriter
    
    if not analyzer or not rewriter:
        raise HTTPException(status_code=503, detail="Models are still loading...")

    text = request.message
    
    # Step 1: Analyze
    analysis_result = analyzer.analyze_text(text)
    
    # Step 2: Decide Action
    decision = decision_engine.decide_action(analysis_result, request.user_id)
    action = decision["action"]
    reason = decision["reason"]
    
    # Step 3: Rewrite if necessary
    rewritten_text = None
    if action in ["block_and_rewrite", "warn", "block_and_alert"]:
        # Only rewrite if it's not clean/allow
        try:
            rewritten_text = rewriter.rewrite_message(text)
        except Exception as e:
            print(f"Rewriting error: {e}")
            rewritten_text = text # Fallback to original if rewrite fails, or empty
    
    return {
        "analysis": analysis_result,
        "action": action,
        "reason": reason,
        "rewrite": rewritten_text,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
