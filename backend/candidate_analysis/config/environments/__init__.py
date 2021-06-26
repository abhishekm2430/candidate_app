import os

if os.environ["FLASK_ENV"] == "development":
    from .development import env
elif os.environ["FLASK_ENV"] == "production":
    from .production import env
elif os.environ["FLASK_ENV"] == "test":
    from .test import env
