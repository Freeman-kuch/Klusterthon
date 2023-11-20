from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
class App_Config():
    """_summary_"""

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
