import os
from datetime import timedelta


class Config:
    # Flask-WTF Secret Key
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")

    # Database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///site.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CSRF and session security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    # Session duration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
