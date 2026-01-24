import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

class MessageRewriter:
    def __init__(self):
        """
        Initializes the MessageRewriter using Google Gemini API.
        Model: gemini-1.5-flash (Fast, Free Tier compatible)
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("CRITICAL: GEMINI_API_KEY not found in environment!")
            return

        print("Initializing Rewriter Logic with Google Gemini (gemini-2.0-flash)...")
        genai.configure(api_key=api_key)
        
        # Configure the model
        self.model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction="You are a helpful assistant that rewrites toxic or rude messages into polite, kind, and constructive versions. Keep the meaning but remove the toxicity. Output ONLY the rewritten text."
        )
        print("Rewriter Configured.")

    def rewrite_message(self, text: str) -> str:
        """
        Rewrites the input text using Google Gemini.
        """
        if not text or not text.strip():
            return ""

        try:
            # Generate content
            response = self.model.generate_content(
                f"Rewrite this to be polite: '{text}'",
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=100,
                    temperature=0.3
                )
            )
            
            rewritten = response.text.strip()
            
            # Clean up potential quotes if the model adds them
            if rewritten.startswith('"') and rewritten.endswith('"'):
                rewritten = rewritten[1:-1]
            
            return rewritten

        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "I would prefer not to say that."
