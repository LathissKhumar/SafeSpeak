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
        # Configure the model
        self.model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction="You are a text transformation engine. Your task is to rewrite inputs to be polite and objective. Remove insults but keep the core message. Do not be conversational."
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
                f"Objectively rewrite this text to be polite. Maintain the original meaning. Text: {text}",
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=100,
                    temperature=0.1
                ),
                safety_settings={
                    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            rewritten = response.text.strip()
            
            # Clean up common model prefixes
            prefixes = ["Rewritten:", "Polite version:", "Output:", "Input:"]
            for p in prefixes:
                if rewritten.lower().startswith(p.lower()):
                    rewritten = rewritten[len(p):].strip()
            
            # Clean up quotes
            if rewritten.startswith('"') and rewritten.endswith('"'):
                rewritten = rewritten[1:-1]
            
            return rewritten

        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "I would prefer not to say that."
