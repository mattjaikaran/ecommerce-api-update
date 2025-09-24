"""Email utilities for sending templated emails."""

from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email_template(
    template_name: str,
    context: dict[str, Any],
    recipient_email: str,
    subject: str,
    from_email: str | None = None,
) -> bool:
    """Send an email using a template.

    Args:
        template_name: Path to the email template
        context: Template context variables
        recipient_email: Recipient's email address
        subject: Email subject line
        from_email: Sender's email address (uses default if None)

    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        html_content = render_to_string(template_name, context)

        send_mail(
            subject=subject,
            message="",  # Plain text version
            html_message=html_content,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return True
    except Exception:
        # Log the error in production
        return False


def send_bulk_email(
    template_name: str,
    recipients: list[dict[str, Any]],
    subject: str,
    from_email: str | None = None,
) -> dict[str, int]:
    """Send bulk emails using a template.

    Args:
        template_name: Path to the email template
        recipients: List of recipient dicts with 'email' and 'context' keys
        subject: Email subject line
        from_email: Sender's email address

    Returns:
        Dictionary with 'sent' and 'failed' counts
    """
    sent_count = 0
    failed_count = 0

    for recipient in recipients:
        success = send_email_template(
            template_name=template_name,
            context=recipient.get("context", {}),
            recipient_email=recipient["email"],
            subject=subject,
            from_email=from_email,
        )

        if success:
            sent_count += 1
        else:
            failed_count += 1

    return {"sent": sent_count, "failed": failed_count}


def send_welcome_email(user_email: str, user_name: str) -> bool:
    """Send welcome email to new user.

    Args:
        user_email: User's email address
        user_name: User's display name

    Returns:
        True if email sent successfully, False otherwise
    """
    context = {
        "user_name": user_name,
        "site_name": getattr(settings, "SITE_NAME", "Ecommerce Store"),
    }

    return send_email_template(
        template_name="emails/welcome.html",
        context=context,
        recipient_email=user_email,
        subject="Welcome to our store!",
    )


def send_order_confirmation_email(order, customer_email: str) -> bool:
    """Send order confirmation email.

    Args:
        order: Order instance
        customer_email: Customer's email address

    Returns:
        True if email sent successfully, False otherwise
    """
    context = {
        "order": order,
        "site_name": getattr(settings, "SITE_NAME", "Ecommerce Store"),
    }

    return send_email_template(
        template_name="emails/order_confirmation.html",
        context=context,
        recipient_email=customer_email,
        subject=f"Order Confirmation #{order.id}",
    )
