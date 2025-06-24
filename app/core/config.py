"""Application configuration and settings"""

import os
from typing import Optional
from pydantic import BaseSettings, EmailStr

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application settings
    app_name: str = "HST Professional Services"
    app_description: str = "Professional technology consulting and business services"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Contact information
    contact_email: EmailStr = "info@hst.ie"
    contact_phone: str = "+353 1 234 5678"
    company_address: str = "Dublin, Ireland"
    
    # Email settings (for contact form)
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # External API keys
    unsplash_access_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()