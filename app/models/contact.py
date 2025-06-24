"""Contact form models and validation"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class ContactForm(BaseModel):
    """Contact form data model with validation"""
    
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    company: Optional[str] = Field(None, max_length=100, description="Company name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    service: str = Field(..., description="Service of interest")
    message: str = Field(..., min_length=10, max_length=2000, description="Message content")
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()
    
    @validator('phone')
    def validate_phone(cls, v):
        if v and v.strip():
            # Basic phone validation
            cleaned = ''.join(filter(str.isdigit, v))
            if len(cleaned) < 7:
                raise ValueError('Phone number too short')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "company": "Tech Corp",
                "phone": "+353 1 234 5678",
                "service": "Technology Consulting",
                "message": "I'm interested in your technology consulting services for our digital transformation project."
            }
        }

class ContactResponse(BaseModel):
    """Contact form response model"""
    
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Thank you for your message. We'll get back to you soon!",
                "timestamp": "2024-01-15T10:30:00"
            }
        }