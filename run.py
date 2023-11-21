from kluster import create_app
from kluster.config import AppConfig


app = create_app(AppConfig)


if __name__ == "__main__":
    app.run(debug=True)
