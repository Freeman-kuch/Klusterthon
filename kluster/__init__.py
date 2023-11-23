from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from flask_login import LoginManager
from kluster.config import AppConfig

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=AppConfig):
    """
    Create a new instance of the app with the given configuration.

    :param config_class: configuration class
    :return: app
    """
    # Initialize Flask
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        print(f"using db")

    # Initialize CORS
    CORS(app, supports_credentials=True)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Flask-login Manager
    login_manager.init_app(app)

    # Register blueprints

    from kluster.auth.auth import auth
    from kluster.errors.error_handler import error

    app.register_blueprint(auth)
    app.register_blueprint(error)

    # create db tables from models if not exists
    with app.app_context():
        print("creating tables")
        db.create_all()

    return app
