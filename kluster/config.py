from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
class App_Config():
    """_summary_"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    GOOGLE_CLIENT_ID = os.environ.get("client_id")
    GOOGLE_CLIENT_SECRET = os.environ.get("client_secret")
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
