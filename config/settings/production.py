from .base import *  # noqa

ALLOWED_HOSTS = [
    "api.example.com",
    "localhost",
    "127.0.0.1",
    "server_ip_address",
]
CSRF_TRUSTED_ORIGINS = ["api.example.com"]
DEBUG = False
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
