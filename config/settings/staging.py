from .base import *  # noqa

ALLOWED_HOSTS = [
    "localhost",
    "api.staging.example.com",
    "server_ip_address",
    "127.0.0.1",
]
DEBUG = True
CSRF_TRUSTED_ORIGINS = [
    "https://api.staging.example.com",
    "http://localhost",
]
