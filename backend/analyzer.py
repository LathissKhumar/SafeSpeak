import torch
from transformers import pipeline

class ToxicityAnalyzer:
    def __init__(self):
        """
        Initialize the toxicity analyzer with the s-nlp/roberta_toxicity_classifier model.
        """
        print("Loading Toxicity Model (s-nlp/roberta_toxicity_classifier)...")
        # return_all_scores=True ensures we get probabilities for all labels
        try:
            self.pipeline = pipeline("text-classification", model="s-nlp/roberta_toxicity_classifier", return_all_scores=True)
            print("Toxicity Model Loaded.")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback or re-raise depending on strictness. Here we re-raise.
            raise e

    def analyze_text(self, text: str) -> dict:
        """
        Analyze text for toxicity.
        Returns a dictionary with label, severity score, confidence, and explanation.
        """
        if not text or not text.strip():
            return {
                "label": "clean",
                "severity": 0,
                "confidence": 0.0,
                "explanation": "Message is empty."
            }

        try:
            results = self.pipeline(text)
        except Exception as e:
            print(f"Prediction error: {e}")
            return {
                "label": "error",
                "severity": 0,
                "confidence": 0.0,
                "explanation": "Error processing message."
            }
            
        # Results structure: [[{'label': 'neutral', 'score': 0.9}, {'label': 'toxic', 'score': 0.1}, ...]]
        scores = results[0] 
        
        # s-nlp/roberta_toxicity_classifier labels usually are: neutral, toxic.
        # Or multi-label if trained that way. 
        # Check standard labels for this model: usually binary "neutral" vs "toxic"
        # BUT many variants exist. Let's assume standard behavior for now and be robust.
        
        # If binary (neutral/toxic):
        # We can map 'toxic' score to severity directly.
        
        # If multi-label (like toxic-bert):
        # We adopt the same logic as before.
        
        # Let's inspect labels dynamically or assume standard toxic-bert like classes if it was fine-tuned similarly.
        # The user asked for "roberta-base-toxic", often implies the one by s-nlp or similar which might be binary.
        # However, to support specific categories (threat, insult) requested in the prompt ("Detect: toxic, insult, threat..."),
        # we ideally need a multi-label model. 
        # s-nlp/roberta_toxicity_classifier IS binary (toxic vs neutral) in many versions. 
        # unitary/toxic-bert WAS multi-label.
        # IF the user insists on "roberta-base-toxic" AND specific categories, there is a conflict if the model is binary.
        # I will attempt to interpret the model usage.
        # If the model only returns "neutral" and "toxic", we can't detect "threat" specifically unless we use another model or heuristics.
        # Let's assume the user knows the model they asked for.
        # If it is binary, we map "toxic" score to severity. Label is just "toxic".
        # We can add a generic explanation.
        
        # Let's simply handle whatever labels come back.
        
        max_score = 0
        max_label = "neutral"
        toxic_score = 0.0
        
        # Map for severity logic
        # If multi-label, we can weight them.
        # If binary, we just use toxic score.
        
        for item in scores:
            label = item['label']
            score = item['score']
            
            if score > max_score:
                max_score = score
                max_label = label
            
            if label == 'toxic':
                toxic_score = score
            elif label == 'severe_toxic':
                toxic_score = max(toxic_score, score * 1.2) # Boost
            elif label == 'neutral':
                pass # ignore for toxicity calc
            else:
                 # threat, insult, etc. treat as toxic
                if score > 0.5:
                     toxic_score = max(toxic_score, score)

        # If model is binary "neutral/toxic", toxic_score might be set above.
        # If max_label is 'toxic' and scores don't have 'neutral', etc.
        
        # Let's derive severity from the highest "bad" label score found.
        # If the model is strictly binary [neutral, toxic], then 'toxic' score is our metric.
        
        # Robustness: look for 'toxic' label. If not found, use max score of non-neutral.
        final_toxic_prob = 0.0
        detected_categories = []
        
        for item in scores:
            if item['label'] != 'neutral':
                if item['score'] > 0.5:
                    detected_categories.append(item['label'])
                if item['label'] in ['toxic', 'severe_toxic', 'threat', 'insult', 'identity_hate', 'obscene']:
                     final_toxic_prob = max(final_toxic_prob, item['score'])
                elif item['label'] not in ['neutral', 'clean']: # Unknown bad label
                     final_toxic_prob = max(final_toxic_prob, item['score'])

        # If the model is binary (neutral/toxic), final_toxic_prob is just the toxic score.
        
        severity_score = int(final_toxic_prob * 100)
        
        # Adjustment for specific request: "Detect: toxic, insult, threat, severe_toxic"
        # If the model doesn't output these, we can't reliably detect them. 
        # We will list detected categories in explanation.
        
        user_explanation = "Message appears safe."
        if severity_score >= 10:
             if detected_categories:
                 cats = ", ".join(detected_categories)
                 user_explanation = f"Message contains: {cats}."
             else:
                 user_explanation = "Message contains toxic content."

        # Classification
        if severity_score < 20: # Updated thresholds to match Decision Engine roughly
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
            "confidence": final_toxic_prob,
            "explanation": user_explanation
        }
