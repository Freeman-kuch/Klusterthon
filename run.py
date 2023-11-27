from kluster import create_app
from kluster.config import AppConfig

app = create_app(AppConfig)
celery_app = app.extensions["celery"]

if __name__ == "__main__":
    app.run(
        debug=True,
        ssl_context="adhoc",
    )
    celery_app.run
