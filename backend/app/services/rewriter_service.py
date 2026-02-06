from google import genai
from google.genai import types
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

class RewriterService:
    def __init__(self):
        try:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            self.model = "gemini-2.0-flash"
            logger.info("RewriterService initialized with Google GenAI SDK.")
        except Exception as e:
            logger.error(f"Failed to initialize RewriterService: {e}")
            raise

    def rewrite(self, text: str) -> str:
        if not text or not text.strip():
            return ""

        try:
            prompt = f"Objectively rewrite this text to be polite. Maintain the original meaning. Text: {text}"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are a text transformation engine. Your task is to rewrite inputs to be polite and objective. Remove insults but keep the core message. Do not be conversational.",
                    temperature=0.1,
                    candidate_count=1,
                    max_output_tokens=100,
                    safety_settings=[
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                            threshold=types.HarmBlockThreshold.BLOCK_NONE
                        ),
                    ]
                )
            )
            
            if not response.text:
                return "I would prefer not to say that."

            rewritten = response.text.strip()
            
            # Clean up common model prefixes (just in case)
            prefixes = ["Rewritten:", "Polite version:", "Output:", "Input:"]
            for p in prefixes:
                if rewritten.lower().startswith(p.lower()):
                    rewritten = rewritten[len(p):].strip()
            
            if rewritten.startswith('"') and rewritten.endswith('"'):
                rewritten = rewritten[1:-1]
            
            return rewritten

        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return "I would prefer not to say that."
