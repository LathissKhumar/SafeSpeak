import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class MessageRewriter:
    def __init__(self):
        """
        Initialize the rewriter with Hugging Face Inference API.
        Using mistralai/Mistral-7B-Instruct-v0.3 for intelligent rewriting.
        """
        print("Initializing Rewriter Logic for HF API (mistralai/Mistral-7B-Instruct-v0.3)...")
        token = os.getenv("HF_API_KEY")
        self.client = InferenceClient(token=token)
        self.model = "mistralai/Mistral-7B-Instruct-v0.3"
        print("Rewriter Configured.")

    def rewrite_message(self, text: str) -> str:
        """
        Rewrites the input text to be polite and child-safe using HF API.
        """
        if not text or not text.strip():
            return ""

        # Construct the prompt using Mistral [INST] format
        prompt = f"[INST] Rewrite the following Toxic message into a Polite, Child-Safe version. Output ONLY the polite sentence.\n\nToxic: \"{text}\"\nPolite: [/INST]"
        
        try:
            # API Call
            response = self.client.text_generation(
                prompt, 
                model=self.model,
                max_new_tokens=64,
                temperature=0.3,
                return_full_text=False
            )
            # Response is the generated text
            rewritten = response.strip()
            
            return rewritten

        except Exception as e:
            print(f"Rewriting API Error: {e}")
            return "I would prefer not to say that."
