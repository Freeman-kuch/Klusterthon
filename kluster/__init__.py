from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from kluster.config import AppConfig
from celery import Celery
import os

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

def make_celery(app):
    celery = Celery(
        app.import_name, 
        #backend=app.config['CELERY_RESULT_BACKEND'], 
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(config_class=AppConfig):
    """
    Create a new instance of the app with the given configuration.
    :param config_class: configuration class
    :return: app
    """
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)

    # Configure Celery inside the factory function
    app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'amqp://localhost:5672')
    app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')
    
    # Initialize Flask extensions
    CORS(app, supports_credentials=True)
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Import blueprints
    from kluster.auth.auth import auth
    from kluster.errors.error_handler import error
    from kluster.routes.patients import patients
    from kluster.profile.profile import profile_bp

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(error)
    app.register_blueprint(patients)
    app.register_blueprint(profile_bp)
    
    # Create db tables if they do not exist
    with app.app_context():
        db.create_all()

    return app


