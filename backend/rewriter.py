import os
import requests
from dotenv import load_dotenv

load_dotenv()

class MessageRewriter:
    def __init__(self):
        """
        Initialize the rewriter. 
        Using direct HTTP requests for maximum stability.
        Model: google/flan-t5-base (flan-t5-large returned 410 Gone)
        """
        print("Initializing Rewriter Logic for HF API (facebook/bart-large-cnn)...")
        self.api_url = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}
        print("Rewriter Configured.")

    def rewrite_message(self, text: str) -> str:
        """
        Rewrites the input text using direct API call.
        """
        if not text or not text.strip():
            return ""

        # Construct the prompt (BART is a summarizer, so we frame it as a task)
        prompt = f"Rewrite to be polite: {text}"
        
        try:
            # Raw HTTP Request
            payload = {
                "inputs": prompt,
                "parameters": {"max_new_tokens": 64, "temperature": 0.2, "do_sample": True}
            }
            
            # Increased timeout for "Model Loading" (Cold Start)
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code != 200:
                print(f"API Error Status: {response.status_code}")
                # print(f"API Error Body: {response.text}")
                response.raise_for_status()
            
            response_json = response.json()
            
            # BART Summarization format: [{'summary_text': '...'}]
            if isinstance(response_json, list) and len(response_json) > 0:
                # Check for 'summary_text' (BART) or 'generated_text' (T5/GPT)
                rewritten = response_json[0].get("summary_text") or response_json[0].get("generated_text", "")
            else:
                rewritten = str(response_json)
                
            rewritten = rewritten.strip()
            
            # Remove the prompt if it was echoed back (common in some models)
            if rewritten.startswith(prompt):
                rewritten = rewritten[len(prompt):].strip()

            # Safety checks
            if rewritten.lower() == text.lower() or "stupid" in rewritten.lower():
                return "I do not agree with that."
                
            return rewritten

        except Exception as e:
            print(f"!!! HF REWRITER API ERROR !!!: {e}")
            return "I would prefer not to say that."
