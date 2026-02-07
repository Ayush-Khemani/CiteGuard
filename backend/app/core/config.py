"""
Core configuration for CiteGuard backend.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "CiteGuard API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "postgresql://citeguard:citeguard@localhost:5432/citeguard"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    USE_LOCAL_MODELS: bool = True  # Fallback to local models if no API keys
    
    # Similarity Detection
    SIMILARITY_THRESHOLD: float = 0.85
    SIMILARITY_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    MAX_DOCUMENT_LENGTH: int = 100000  # characters
    
    # External APIs
    SEMANTIC_SCHOLAR_API_KEY: Optional[str] = None
    CROSSREF_EMAIL: Optional[str] = None  # For polite API usage
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "chrome-extension://*",
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".txt", ".docx", ".pdf"}
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Feature Flags
    ENABLE_PARAPHRASING: bool = True
    ENABLE_CITATION_SEARCH: bool = True
    ENABLE_STYLE_ANALYSIS: bool = False  # Phase 2 feature
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()