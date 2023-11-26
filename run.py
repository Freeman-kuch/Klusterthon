from kluster import create_app, make_celery
from kluster.config import AppConfig


app = create_app(AppConfig)


# Create Celery instance
celery = make_celery(app)

if __name__ == "__main__":
    app.run(
        debug=True,
        ssl_context="adhoc",
    )
