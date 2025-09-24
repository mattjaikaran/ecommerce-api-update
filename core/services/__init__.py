"""Core services package."""

from .email import EmailService, default_email_service

__all__ = ["EmailService", "default_email_service"]
