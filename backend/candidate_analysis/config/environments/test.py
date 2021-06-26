# from framework import app
# from flask_jwt_extended import (
#     JWTManager, jwt_required, create_access_token,
#     get_jwt_identity
# )
# class Test(object):
#     def __init__(self):
#         self.type = "test"

# test = Test()
env = {
    "TYPE": "test",
    "DEBUG": False,
    "JWT_SECRET_KEY": "super-secret",
    "SECRET_KEY": "nobodyknows",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}
    # ,
    # "JWT": JWTManager(app)
# app.debug = DEBUG

# app.config["JWT_SECRET_KEY"] = "super-secret"
