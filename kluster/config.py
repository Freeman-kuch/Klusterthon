from dotenv import load_dotenv, find_dotenv
from datetime import timedelta
import os, cloudinary

load_dotenv(find_dotenv())


class AppConfig():
    """_summary_"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_IDENTITY_CLAIM = "sub"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    GOOGLE_CLIENT_ID = os.environ.get("client_id")
    GOOGLE_CLIENT_SECRET = os.environ.get("client_secret")
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    CLOUDINARY_URL = "cloudinary://" + os.environ.get("Cloudinary_API_Key") + ":" + os.environ.get(
        "Cloudinary_API_Secret") + "@" + os.environ.get("Cloudinary_Name")
    STANDARD_TIMEOUT = 1800
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False    
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")