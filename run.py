from kluster import create_app
from kluster.config import AppConfig
from kluster.celery_utils import celery

app = create_app(AppConfig)

if __name__ == "__main__":
    app.run(
        debug=True,
        ssl_context="adhoc",
    )
