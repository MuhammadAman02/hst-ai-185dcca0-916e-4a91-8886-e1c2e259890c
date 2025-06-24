"""Email service for contact form processing"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings
from app.models.contact import ContactForm

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
    
    async def send_contact_email(self, contact_form: ContactForm) -> bool:
        """Send contact form email to admin"""
        try:
            if not self.smtp_username or not self.smtp_password:
                logger.warning("SMTP credentials not configured, logging contact form instead")
                self._log_contact_form(contact_form)
                return True
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = settings.contact_email
            msg['Subject'] = f"New Contact Form Submission - {contact_form.service}"
            
            # Email body
            body = f"""
            New contact form submission received:
            
            Name: {contact_form.name}
            Email: {contact_form.email}
            Company: {contact_form.company or 'Not provided'}
            Phone: {contact_form.phone or 'Not provided'}
            Service Interest: {contact_form.service}
            
            Message:
            {contact_form.message}
            
            ---
            Sent from HST Professional Services Website
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Contact email sent for {contact_form.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending contact email: {e}")
            # Fallback to logging
            self._log_contact_form(contact_form)
            return False
    
    def _log_contact_form(self, contact_form: ContactForm):
        """Log contact form submission when email fails"""
        logger.info(f"""
        CONTACT FORM SUBMISSION:
        Name: {contact_form.name}
        Email: {contact_form.email}
        Company: {contact_form.company}
        Phone: {contact_form.phone}
        Service: {contact_form.service}
        Message: {contact_form.message}
        """)