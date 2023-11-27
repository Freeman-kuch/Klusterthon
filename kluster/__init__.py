from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from kluster.config import AppConfig
from celery import Celery

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

celery = Celery(__name__, backend=AppConfig.CELERY_RESULT_BACKEND, broker=AppConfig.CELERY_BROKER_URL)

def init_celery(app=None):
    """
    Initialize Celery with Flask app context.
    """
    app = app or create_app()
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

def create_app(config_class=AppConfig):
    """
    Create a new instance of the app with the given configuration.
    :param config_class: configuration class
    :return: app
    """
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    
    # Initialize Flask extensions
    CORS(app, supports_credentials=True)
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Initialize Celery with Flask app
    init_celery(app)

    # Register celery tasks
    from kluster import tasks 


    # Import blueprints
    from kluster.auth.auth import auth
    from kluster.errors.error_handler import error
    from kluster.routes.patients import patients
    from kluster.profile.profile import profile_bp
    from kluster.medications.medication import medication_bp

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(error)
    app.register_blueprint(patients)
    app.register_blueprint(profile_bp)
    app.register_blueprint(medication_bp)

  

    # Create db tables if they do not exist
    with app.app_context():
        db.create_all()

    return app



