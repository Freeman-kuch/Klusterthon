from kluster import create_app, celery
from kluster.config import AppConfig
from kluster import tasks

app = create_app(AppConfig)


if __name__ == "__main__":
    app.run(
        debug=True,
        ssl_context="adhoc",
    )
