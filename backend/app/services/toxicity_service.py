from huggingface_hub import InferenceClient
from app.core.config import get_settings
from app.schemas.analysis import AnalysisResult
from app.core.logging import logger

settings = get_settings()

class ToxicityService:
    def __init__(self):
        try:
            self.client = InferenceClient(token=settings.HF_API_KEY)
            self.model_id = settings.TOXICITY_MODEL
            logger.info("ToxicityService initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize ToxicityService: {e}")
            raise

    def analyze(self, text: str) -> AnalysisResult:
        if not text or not text.strip():
            return AnalysisResult(label="clean", score=0.0, severity=0.0)

        try:
            # API Call
            scores = self.client.text_classification(text, model=self.model_id)
            # scores is a list of dicts: [{'label': 'neutral', 'score': 0.9}, ...]
        except Exception as e:
            logger.error(f"HF API Error: {e}")
            return AnalysisResult(label="error", score=0.0, severity=0.0)

        toxic_score = 0.0
        
        # Determine toxicity
        for item in scores:
            label = item['label']
            score = item['score']
            
            if label == 'toxic':
                toxic_score = score
            elif label == 'neutral':
                pass
            else:
                if score > 0.5:
                    toxic_score = max(toxic_score, score)

        severity_score = int(toxic_score * 100)
        
        if severity_score < 20: 
            label = "clean"
        elif severity_score < 40:
            label = "mild"
        elif severity_score < 80:
            label = "toxic"
        else:
            label = "severe"

        return AnalysisResult(
            label=label,
            score=toxic_score,
            severity=severity_score
        )
