from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from flask_jwt_extended import JWTManager
from kluster.config import AppConfig
from kluster.celery_utils import  celery_init_app


db = SQLAlchemy()
jwt = JWTManager()

# app = Flask(__name__)

# app.config['CELERY_BROKER_URL'] = AppConfig.CELERY_BROKER_URL
# app.config['CELERY_RESULT_BACKEND'] = AppConfig.CELERY_RESULT_BACKEND

# celery = Celery(
#     app.import_name,
#     backend=app.config['CELERY_RESULT_BACKEND'],
#     broker=app.config['CELERY_BROKER_URL'],
# )


def create_app(config_class=AppConfig):
    """
    Create a new instance of the app with the given configuration.
    :param config_class: configuration class
    :return: app
    """
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    
    app.config.from_mapping(
        CELERY=dict(
            broker_url=AppConfig.CELERY_BROKER_URL,
            result_backend=AppConfig.CELERY_RESULT_BACKEND,
            task_ignore_result=True,
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    
  
    # Initialize Flask extensions
    CORS(app, supports_credentials=True)
    db.init_app(app)
    jwt.init_app(app)


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

