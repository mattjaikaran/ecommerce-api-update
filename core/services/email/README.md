# Email Service

A modular, polymorphic email service for Django applications.

## Structure

- `backends.py` - Email backend implementations (Django, simple)
- `service.py` - Main EmailService class
- `templates.py` - Template handling and rendering
- `utils.py` - Convenience functions for common email operations

## Usage

### Basic Usage

```python
from core.services.email import EmailService, default_email_service

# Simple email
success = default_email_service.send_simple_email(
    subject="Welcome!",
    message="Thank you for joining us.",
    recipient_email="user@example.com",
    html_message="<h1>Welcome!</h1>"
)
```

### Templated Emails

```python
template_data = {
    "html_template": "emails/welcome.html",
    "text_template": "emails/welcome.txt",
    "subject_template": "emails/welcome_subject.txt",
    "context": {"user_name": "John", "site_name": "Store"}
}

success = default_email_service.send_templated_email(
    template_data=template_data,
    recipient_email="john@example.com"
)
```

### Bulk Emails

```python
email_data_list = [
    {
        "subject": "Welcome!",
        "message": "Welcome to our store!",
        "recipient_email": "user1@example.com",
    },
    {
        "template_data": {
            "html_template": "emails/newsletter.html",
            "context": {"user_name": "Jane"},
        },
        "recipient_email": "user2@example.com",
    },
]

results = default_email_service.send_bulk_emails(email_data_list)
print(f"Sent: {results['sent']}, Failed: {results['failed']}")
```

### Custom Backends

```python
from core.services.email import EmailService, SimpleEmailBackend

# Use a different backend
service = EmailService(backend=SimpleEmailBackend())
```

## Error Handling

The service uses proper exception handling with `logging.exception` and raises `EmailSendError` for failed sends. Convenience functions return `True`/`False` for backward compatibility.

## Features

- Multiple backend support
- Template rendering (HTML, text, subject)
- Bulk email sending
- Proper error handling and logging
- Type hints and protocols
- Modular, extensible design
