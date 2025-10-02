# Email Service

This email service provides functionality to send emails using SMTP.

## Configuration

Add the following environment variables to your `.env` file:

```env
smtp_host=smtp.gmail.com
smtp_username=your-email@gmail.com
smtp_password=your-app-password
smtp_port=587
```

## Usage

### Basic Email Sending

```python
from logical.email_service import send

# Send a simple email
success = send(
    subject="Test Email",
    body="<h1>Hello World!</h1><p>This is a test email.</p>",
    from_address="sender@example.com",
    to_address="recipient@example.com",
    cc="cc@example.com"  # Optional
)
```

### Contact Form Emails

```python
from logical.email_service import send_contact_us_notification, send_contact_us_confirmation

# Contact form data
contact_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '1234567890',
    'whatsappNumber': '9876543210',
    'message': 'Hello, I would like to know more about your services.'
}

# Send notification to admin
send_contact_us_notification(contact_data, "admin@kseekers.com")

# Send confirmation to user
send_contact_us_confirmation(contact_data)
```

## Gmail Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use the app password in your `.env` file

## Features

- HTML email support
- Automatic contact form notifications
- User confirmation emails
- Error handling and logging
- SMTP authentication
