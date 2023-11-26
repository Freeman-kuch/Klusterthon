# celery_utils.py
from flask import Flask
from celery import Celery
import os 

flask_app = Flask(__name__)
# Configure Celery inside the factory function
flask_app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'amqp://localhost:5672')
flask_app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')

def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name, 
        backend=app.config['CELERY_RESULT_BACKEND'], 
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(flask_app)