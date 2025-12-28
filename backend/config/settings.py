from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Groq API
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "mixtral-8x7b-32768"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/aivideostudio"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Application
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # Paths
    OUTPUT_PATH: str = "/app/output"
    TEMP_PATH: str = "/app/temp"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    
    # Edge-TTS Voices
    ARABIC_VOICE_MALE: str = "ar-SA-HamedNeural"
    ARABIC_VOICE_FEMALE: str = "ar-EG-SalmaNeural"
    ENGLISH_VOICE_MALE: str = "en-US-GuyNeural"
    ENGLISH_VOICE_FEMALE: str = "en-US-JennyNeural"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
