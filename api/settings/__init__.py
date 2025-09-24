"""Django settings module initialization.

This module determines which settings module to import based on the
DJANGO_SETTINGS_MODULE environment variable or defaults to development.
"""

import os

# Default to development settings if not specified
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings.dev")

# Import the appropriate settings module
django_settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")

if django_settings_module == "api.settings.prod":
    from .prod import *
elif django_settings_module == "api.settings.dev":
    from .dev import *
else:
    # Default to development
    from .dev import *
