"""Core Celery tasks for the ecommerce application.

This module contains asynchronous tasks that can be executed by Celery workers.
"""

import logging

from celery import shared_task
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, ignore_result=True)
def cleanup_expired_sessions(self):
    """Clean up expired sessions from the database.

    This task removes all sessions that have expired to keep the database clean.
    """
    try:
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired_sessions.count()
        expired_sessions.delete()

        logger.info(f"Cleaned up {count} expired sessions")
        return f"Successfully cleaned up {count} expired sessions"
    except Exception as exc:
        logger.error(f"Error cleaning up sessions: {exc}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@shared_task(bind=True)
def send_notification_email(self, recipient_email, subject, message):
    """Send a notification email asynchronously.

    Args:
        recipient_email (str): Email address of the recipient
        subject (str): Email subject
        message (str): Email message body
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )

        logger.info(f"Email sent successfully to {recipient_email}")
        return f"Email sent to {recipient_email}"
    except Exception as exc:
        logger.error(f"Error sending email to {recipient_email}: {exc}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@shared_task(bind=True)
def generate_report(self, report_type, filters=None):
    """Generate reports asynchronously.

    Args:
        report_type (str): Type of report to generate
        filters (dict, optional): Filters to apply to the report
    """
    try:
        # This is a placeholder for report generation logic
        # You can implement specific report generation based on report_type

        logger.info(f"Generating {report_type} report with filters: {filters}")

        # Simulate report generation
        import time

        time.sleep(2)  # Simulate processing time

        return f"{report_type} report generated successfully"
    except Exception as exc:
        logger.error(f"Error generating {report_type} report: {exc}")
        raise self.retry(exc=exc, countdown=60, max_retries=3)
