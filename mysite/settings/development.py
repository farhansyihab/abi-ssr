"""
Development settings for Wagtail.
Uses PostgreSQL from base.py - NO SQLITE!
"""

from .base import *

DEBUG = True
SECRET_KEY = "django-insecure-development-key-here"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "172.17.0.1", "192.168.0.102"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ⚠️  NO DATABASE OVERRIDE - using PostgreSQL from base.py
# ⚠️  NO SQLITE CODE HERE!

print("✅ Development mode: Using PostgreSQL from base.py")

try:
    from .local import *
except ImportError:
    pass
