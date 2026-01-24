import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class ToxicityAnalyzer:
    def __init__(self):
        """
        Initialize the toxicity analyzer with Hugging Face Inference API.
        """
        print("Initializing Logic for HF API (s-nlp/roberta_toxicity_classifier)...")
        token = os.getenv("HF_API_KEY")
        if not token:
            print("WARNING: HF_API_KEY not found in environment variables. API calls may fail or be rate-limited.")
        
        self.client = InferenceClient(token=token)
        self.model_id = "s-nlp/roberta_toxicity_classifier"
        print("Toxicity Analyzer Configured.")

    def analyze_text(self, text: str) -> dict:
        """
        Analyze text for toxicity using HF API.
        """
        if not text or not text.strip():
            return {
                "label": "clean",
                "severity": 0,
                "confidence": 0.0,
                "explanation": "Message is empty."
            }

        try:
            # API Call
            scores = self.client.text_classification(text, model=self.model_id)
            # scores is a list of dicts: [{'label': 'neutral', 'score': 0.9}, ...]
        except Exception as e:
            print(f"!!! HF ANALYZER API ERROR !!!: {e}")
            # Fail gracefully
            return {
                "label": "error",
                "severity": 0,
                "confidence": 0.0,
                "explanation": "Error processing message (API)."
            }

        # Logic to process scores (similar to before)
        max_score = 0
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
                # Treat other bad labels as toxic if they appear
                if score > 0.5:
                    toxic_score = max(toxic_score, score)

        severity_score = int(toxic_score * 100)
        
        user_explanation = "Message appears safe."
        if severity_score >= 10:
             user_explanation = "Message contains toxic content."

        # Classification
        if severity_score < 20: 
            label = "clean"
        elif severity_score < 40:
            label = "mild"
        elif severity_score < 80:
            label = "toxic"
        else:
            label = "severe"

        return {
            "label": label,
            "severity": severity_score,
            "confidence": toxic_score,
            "explanation": user_explanation
        }
