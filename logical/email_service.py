import config
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional
import traceback

EMAIL_HOST = config.smtp_host
EMAIL_HOST_USER = config.smtp_username
EMAIL_HOST_PASSWORD = config.smtp_password
EMAIL_PORT = config.smtp_port



def send(subject: str, body: str, from_address: str, to_address: str, cc: Optional[str] = None):
    """
    Send an email using SMTP
    
    Args:
        subject (str): Email subject
        body (str): Email body (HTML format)
        from_address (str): Sender email address
        to_address (str): Recipient email address
        cc (str, optional): CC email address(es)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address
        
        if cc:
            msg['Cc'] = cc

        body_html = MIMEText(body, 'html')
        msg.attach(body_html)

        # Create SMTP connection
        s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        s.starttls()
        s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        
        # Send email
        s.sendmail(from_address, to_address, msg.as_string())
        s.quit()
        
        logging.info(f"Email sent successfully to {to_address} with subject: {subject}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send email to {to_address}: {str(e)}")
        print(traceback.format_exc())
        print(e.__traceback__)
        return False


def send_contact_us_notification(contact_data: dict, admin_email: str):
    """
    Send contact us form notification to admin
    
    Args:
        contact_data (dict): Contact form data
        admin_email (str): Admin email address
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = f"New Contact Form Submission - {contact_data.get('name', 'Unknown')}"
        
        body = f"""
        <html>
        <body>
            <h2>New Contact Form Submission</h2>
            <p><strong>Name:</strong> {contact_data.get('name', 'N/A')}</p>
            <p><strong>Email:</strong> {contact_data.get('email', 'N/A')}</p>
            <p><strong>Phone:</strong> {contact_data.get('phone', 'N/A')}</p>
            <p><strong>WhatsApp:</strong> {contact_data.get('whatsappNumber', 'N/A')}</p>
            <p><strong>Message:</strong></p>
            <p>{contact_data.get('message', 'N/A')}</p>
            <hr>
            <p><em>This email was sent from the KSeekers website contact form.</em></p>
        </body>
        </html>
        """
        
        return send(subject, body, EMAIL_HOST_USER, admin_email)
        
    except Exception as e:
        logging.error(f"Failed to send contact us notification: {str(e)}")
        return False


def send_contact_us_confirmation(contact_data: dict):
    """
    Send confirmation email to the person who submitted the contact form
    
    Args:
        contact_data (dict): Contact form data
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = "Thank you for contacting KSeekers"
        
        body = f"""
        <html>
        <body>
            <h2>Thank you for contacting KSeekers!</h2>
            <p>Dear {contact_data.get('name', 'Valued Customer')},</p>
            <p>We have received your message and will get back to you as soon as possible.</p>
            <p><strong>Your message:</strong></p>
            <p style="background-color: #f5f5f5; padding: 10px; border-left: 3px solid #007bff;">
                {contact_data.get('message', 'N/A')}
            </p>
            <p>If you have any urgent queries, please feel free to contact us directly.</p>
            <hr>
            <p><strong>Best regards,</strong><br>KSeekers Team</p>
        </body>
        </html>
        """
        
        return send(subject, body, EMAIL_HOST_USER, contact_data.get('email', ''))
        
    except Exception as e:
        logging.error(f"Failed to send contact us confirmation: {str(e)}")
        return False
