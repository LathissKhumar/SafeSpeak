import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class MessageRewriter:
    def __init__(self):
        """
        Initialize the rewriter with Hugging Face Inference API.
        Using google/flan-t5-large for Balance of Speed & Intelligence.
        """
        print("Initializing Rewriter Logic for HF API (google/flan-t5-large)...")
        token = os.getenv("HF_API_KEY")
        self.client = InferenceClient(token=token)
        self.model = "google/flan-t5-large"
        print("Rewriter Configured.")

    def rewrite_message(self, text: str) -> str:
        """
        Rewrites the input text to be polite and child-safe using HF API.
        """
        if not text or not text.strip():
            return ""

        # Construct the prompt - T5 works best with standard instructions
        prompt = f"Rewrite this text to be polite, kind, and safe for children: {text}"
        
        try:
            # API Call
            response = self.client.text_generation(
                prompt, 
                model=self.model,
                max_new_tokens=64,
                temperature=0.2, # Low temp for consistency
                return_full_text=False
            )
            # Response is the generated text
            rewritten = response.strip()
            
            return rewritten

        except Exception as e:
            print(f"Rewriting API Error: {e}")
            return "I would prefer not to say that."
