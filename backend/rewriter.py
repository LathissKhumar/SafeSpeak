import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

class MessageRewriter:
    def __init__(self):
        """
        Initialize the rewriter with Hugging Face Inference API (google/flan-t5-large).
        We can use 'large' since it runs on the server!
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

        # Construct the prompt
        input_text = f"Rewrite this politely for a child: {text}"
        
        try:
            # API Call
            # text_generation returns a string directly if not detailed
            response = self.client.text_generation(
                input_text, 
                model=self.model,
                max_new_tokens=64,
                temperature=0.7
            )
            # Response is the generated text
            return response.strip()
        except Exception as e:
            print(f"Rewriting API Error: {e}")
            return text # Fallback to original
