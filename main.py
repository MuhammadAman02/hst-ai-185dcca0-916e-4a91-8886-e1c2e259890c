"""
Production-ready HST.ie Website Clone with:
✓ Professional business website design with integrated imagery
✓ Multi-page structure (Home, About, Services, Contact, Blog)
✓ Contact form with validation and email processing
✓ SEO-optimized with proper meta tags and structure
✓ Responsive design with professional visual assets
✓ Modern async patterns and performance optimization
✓ Professional business imagery integration with fallbacks
✓ Zero-configuration deployment readiness
"""

import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional
import os
from datetime import datetime
import logging
from pathlib import Path

# Import our professional asset manager
from app.core.assets import ProfessionalAssetManager
from app.core.config import settings
from app.services.email_service import EmailService
from app.models.contact import ContactForm, ContactResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="HST Professional Services",
    description="Professional consulting and technology services website",
    version="1.0.0",
    docs_url="/admin/docs",  # Hide docs from public
    redoc_url="/admin/redoc"
)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Initialize services
asset_manager = ProfessionalAssetManager()
email_service = EmailService()

# Template context processor
def get_base_context():
    """Get base context for all templates"""
    return {
        "site_name": "HST Professional Services",
        "site_description": "Leading technology consulting and professional services",
        "current_year": datetime.now().year,
        "contact_email": settings.contact_email,
        "contact_phone": settings.contact_phone,
        "company_address": settings.company_address,
    }

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Homepage with hero section and services overview"""
    try:
        # Get professional images for homepage
        hero_image = await asset_manager.get_image("business-team", width=1920, height=1080)
        services_images = await asset_manager.get_image_gallery([
            "technology-consulting", "business-strategy", "digital-transformation"
        ], width=400, height=300)
        
        context = {
            **get_base_context(),
            "request": request,
            "page_title": "Professional Technology Consulting Services",
            "page_description": "Leading provider of technology consulting, digital transformation, and business strategy services",
            "hero_image": hero_image,
            "services_images": services_images,
            "services": [
                {
                    "title": "Technology Consulting",
                    "description": "Strategic technology guidance and implementation",
                    "icon": "🚀",
                    "image": services_images[0] if services_images else None
                },
                {
                    "title": "Digital Transformation",
                    "description": "Modernize your business with cutting-edge solutions",
                    "icon": "💡",
                    "image": services_images[1] if len(services_images) > 1 else None
                },
                {
                    "title": "Business Strategy",
                    "description": "Data-driven strategies for sustainable growth",
                    "icon": "📈",
                    "image": services_images[2] if len(services_images) > 2 else None
                }
            ]
        }
        return templates.TemplateResponse("pages/home.html", context)
    except Exception as e:
        logger.error(f"Error loading homepage: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About us page with team information"""
    try:
        # Get professional team and office images
        team_hero = await asset_manager.get_image("professional-team", width=1200, height=600)
        office_images = await asset_manager.get_image_gallery([
            "modern-office", "team-meeting", "workspace"
        ], width=400, height=300)
        
        context = {
            **get_base_context(),
            "request": request,
            "page_title": "About HST - Professional Technology Consultants",
            "page_description": "Learn about our experienced team of technology consultants and business strategists",
            "team_hero": team_hero,
            "office_images": office_images,
            "team_members": [
                {
                    "name": "Sarah Johnson",
                    "title": "Chief Technology Officer",
                    "bio": "15+ years in enterprise technology solutions",
                    "image": await asset_manager.get_image("professional-woman", width=300, height=300)
                },
                {
                    "name": "Michael Chen",
                    "title": "Senior Business Strategist",
                    "bio": "Expert in digital transformation and process optimization",
                    "image": await asset_manager.get_image("professional-man", width=300, height=300)
                },
                {
                    "name": "Emily Rodriguez",
                    "title": "Lead Consultant",
                    "bio": "Specializes in cloud architecture and system integration",
                    "image": await asset_manager.get_image("business-woman", width=300, height=300)
                }
            ],
            "company_stats": [
                {"number": "500+", "label": "Projects Completed"},
                {"number": "50+", "label": "Enterprise Clients"},
                {"number": "15+", "label": "Years Experience"},
                {"number": "99%", "label": "Client Satisfaction"}
            ]
        }
        return templates.TemplateResponse("pages/about.html", context)
    except Exception as e:
        logger.error(f"Error loading about page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/services", response_class=HTMLResponse)
async def services_page(request: Request):
    """Services page with detailed service descriptions"""
    try:
        # Get service-specific images
        services_hero = await asset_manager.get_image("business-consulting", width=1200, height=600)
        service_images = await asset_manager.get_image_gallery([
            "technology-stack", "cloud-computing", "data-analytics", 
            "cybersecurity", "mobile-development", "ai-machine-learning"
        ], width=500, height=400)
        
        context = {
            **get_base_context(),
            "request": request,
            "page_title": "Professional Technology Services - HST",
            "page_description": "Comprehensive technology consulting services including cloud migration, digital transformation, and strategic planning",
            "services_hero": services_hero,
            "detailed_services": [
                {
                    "title": "Cloud Migration & Architecture",
                    "description": "Seamless transition to cloud platforms with optimized architecture design",
                    "features": ["AWS/Azure/GCP Migration", "Architecture Design", "Cost Optimization", "Security Implementation"],
                    "image": service_images[0] if service_images else None
                },
                {
                    "title": "Digital Transformation",
                    "description": "End-to-end digital transformation strategies and implementation",
                    "features": ["Process Automation", "Legacy System Modernization", "Digital Strategy", "Change Management"],
                    "image": service_images[1] if len(service_images) > 1 else None
                },
                {
                    "title": "Data Analytics & AI",
                    "description": "Advanced analytics solutions and artificial intelligence implementation",
                    "features": ["Business Intelligence", "Machine Learning", "Predictive Analytics", "Data Visualization"],
                    "image": service_images[2] if len(service_images) > 2 else None
                },
                {
                    "title": "Cybersecurity Consulting",
                    "description": "Comprehensive security assessments and implementation strategies",
                    "features": ["Security Audits", "Compliance Management", "Incident Response", "Security Training"],
                    "image": service_images[3] if len(service_images) > 3 else None
                },
                {
                    "title": "Custom Software Development",
                    "description": "Tailored software solutions for unique business requirements",
                    "features": ["Web Applications", "Mobile Apps", "API Development", "System Integration"],
                    "image": service_images[4] if len(service_images) > 4 else None
                },
                {
                    "title": "Technology Strategy",
                    "description": "Strategic technology planning and roadmap development",
                    "features": ["Technology Roadmaps", "Vendor Selection", "Budget Planning", "Risk Assessment"],
                    "image": service_images[5] if len(service_images) > 5 else None
                }
            ]
        }
        return templates.TemplateResponse("pages/services.html", context)
    except Exception as e:
        logger.error(f"Error loading services page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Contact page with contact form"""
    try:
        # Get professional contact/office images
        contact_hero = await asset_manager.get_image("business-meeting", width=1200, height=600)
        office_image = await asset_manager.get_image("modern-office-space", width=600, height=400)
        
        context = {
            **get_base_context(),
            "request": request,
            "page_title": "Contact HST - Get Professional Consulting",
            "page_description": "Contact our team of professional technology consultants for your next project",
            "contact_hero": contact_hero,
            "office_image": office_image,
            "contact_info": {
                "address": settings.company_address,
                "phone": settings.contact_phone,
                "email": settings.contact_email,
                "hours": "Monday - Friday: 9:00 AM - 6:00 PM"
            }
        }
        return templates.TemplateResponse("pages/contact.html", context)
    except Exception as e:
        logger.error(f"Error loading contact page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/contact", response_class=HTMLResponse)
async def submit_contact_form(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: EmailStr = Form(...),
    company: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    service: str = Form(...),
    message: str = Form(...),
):
    """Handle contact form submission"""
    try:
        # Validate form data
        contact_form = ContactForm(
            name=name,
            email=email,
            company=company,
            phone=phone,
            service=service,
            message=message
        )
        
        # Send email in background
        background_tasks.add_task(
            email_service.send_contact_email,
            contact_form
        )
        
        # Log the contact submission
        logger.info(f"Contact form submitted by {name} ({email})")
        
        # Redirect to success page
        return RedirectResponse(url="/contact/success", status_code=303)
        
    except ValidationError as e:
        logger.error(f"Contact form validation error: {e}")
        # Return to contact page with error
        contact_hero = await asset_manager.get_image("business-meeting", width=1200, height=600)
        context = {
            **get_base_context(),
            "request": request,
            "page_title": "Contact HST - Get Professional Consulting",
            "contact_hero": contact_hero,
            "error": "Please check your form data and try again.",
            "form_data": {
                "name": name,
                "email": email,
                "company": company,
                "phone": phone,
                "service": service,
                "message": message
            }
        }
        return templates.TemplateResponse("pages/contact.html", context)
    except Exception as e:
        logger.error(f"Error processing contact form: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/contact/success", response_class=HTMLResponse)
async def contact_success(request: Request):
    """Contact form success page"""
    context = {
        **get_base_context(),
        "request": request,
        "page_title": "Thank You - HST Professional Services",
        "page_description": "Thank you for contacting HST Professional Services"
    }
    return templates.TemplateResponse("pages/contact_success.html", context)

@app.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    """Blog/insights page"""
    try:
        # Get blog-related images
        blog_hero = await asset_manager.get_image("business-insights", width=1200, height=600)
        article_images = await asset_manager.get_image_gallery([
            "technology-trends", "business-growth", "digital-innovation"
        ], width=400, height=250)
        
        context = {
            **get_base_context(),
            "request": request,
            "page_title": "Technology Insights & Blog - HST",
            "page_description": "Latest insights on technology trends, business strategy, and digital transformation",
            "blog_hero": blog_hero,
            "featured_articles": [
                {
                    "title": "The Future of Cloud Computing in Enterprise",
                    "excerpt": "Exploring emerging trends in cloud technology and their impact on business operations.",
                    "date": "2024-01-15",
                    "author": "Sarah Johnson",
                    "image": article_images[0] if article_images else None,
                    "slug": "future-cloud-computing-enterprise"
                },
                {
                    "title": "Digital Transformation Success Stories",
                    "excerpt": "Real-world examples of successful digital transformation initiatives and lessons learned.",
                    "date": "2024-01-10",
                    "author": "Michael Chen",
                    "image": article_images[1] if len(article_images) > 1 else None,
                    "slug": "digital-transformation-success-stories"
                },
                {
                    "title": "AI and Machine Learning in Business Strategy",
                    "excerpt": "How artificial intelligence is reshaping business decision-making and strategy development.",
                    "date": "2024-01-05",
                    "author": "Emily Rodriguez",
                    "image": article_images[2] if len(article_images) > 2 else None,
                    "slug": "ai-machine-learning-business-strategy"
                }
            ]
        }
        return templates.TemplateResponse("pages/blog.html", context)
    except Exception as e:
        logger.error(f"Error loading blog page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )