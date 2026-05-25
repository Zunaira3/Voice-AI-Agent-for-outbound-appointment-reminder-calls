from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Vapi Configuration
    VAPI_API_KEY: str
    VAPI_ASSISTANT_ID: str
    
    # App Configuration
    APP_NAME: str = "Voice AI Agent"
    DEBUG: bool = False
    BASE_URL: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()