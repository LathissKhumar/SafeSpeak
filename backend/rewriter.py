import os
import requests
from dotenv import load_dotenv

load_dotenv()

class MessageRewriter:
    def __init__(self):
        """
        Initialize the rewriter. 
        Using direct HTTP requests for maximum stability.
        Model: google/flan-t5-large
        """
        print("Initializing Rewriter Logic for HF API (google/flan-t5-large)...")
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}
        print("Rewriter Configured.")

    def rewrite_message(self, text: str) -> str:
        """
        Rewrites the input text using direct API call.
        """
        if not text or not text.strip():
            return ""

        # Construct the prompt
        prompt = f"Rewrite this text to be polite, kind, and safe for children: {text}"
        
        try:
            # Raw HTTP Request
            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": 64, "temperature": 0.2}
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=5)
            response.raise_for_status() # Raise error for 4xx/5xx
            
            response_json = response.json()
            
            # T5 response format: [{'generated_text': '...'}]
            if isinstance(response_json, list) and len(response_json) > 0:
                rewritten = response_json[0].get("generated_text", "")
            else:
                rewritten = str(response_json)
                
            rewritten = rewritten.strip()
            
            # Safety checks
            if rewritten.lower() == text.lower() or "asshole" in rewritten.lower() or "stupid" in rewritten.lower():
                return "I do not agree with that."
                
            return rewritten

        except Exception as e:
            print(f"Rewriting API Error: {e}")
            return "I would prefer not to say that."
