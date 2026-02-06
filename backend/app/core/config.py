from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "SafeSpeak API"
    VERSION: str = "2.0.0"
    DEBUG: bool = True
    
    # API Keys
    HF_API_KEY: str
    GEMINI_API_KEY: str
    
    # Model Config
    TOXICITY_MODEL: str = "s-nlp/roberta_toxicity_classifier"
    GENERATIVE_MODEL: str = "gemini-2.0-flash"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
