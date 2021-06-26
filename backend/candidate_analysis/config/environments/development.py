# from framework import app
# from flask_jwt_extended import (
#     JWTManager, jwt_required, create_access_token,
#     get_jwt_identity
# )
# class Development(object):
#     def __init__(self):
#         self.type = "development"

# development = Development()

env = {
    "TYPE": "development",
    "DEBUG": True,
    "JWT_SECRET_KEY": "super-secret",
    "SECRET_KEY": "nobodyknows",
    "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:mindfire@localhost:5432/candidate_analysis",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "CELERY_BROKER":"redis://localhost:6379//",
    "CELERY_BACKEND":"redis://localhost:6379//"
}
    # ,
    # "JWT": JWTManager(app)
    # app.debug = DEBUG

    # app.config["JWT_SECRET_KEY"] = "super-secret"
