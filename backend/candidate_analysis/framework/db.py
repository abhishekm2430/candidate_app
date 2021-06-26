from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask import current_app
# from flask.cli import with_appcontext

# @with_appcontext
# def db():
#     return current_app.config["DB"]

db = SQLAlchemy()
migrate = Migrate(db=db)
