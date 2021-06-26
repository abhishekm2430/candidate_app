import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from candidate_analysis.config.environments import env
from .db import db, migrate
from candidate_analysis import models, controllers
from candidate_analysis.config import initializers
from candidate_analysis.controllers import sessions_controller, dashboards_controller
from candidate_analysis.config.initializers.init_celery import make_celery
from logging.config import dictConfig
import logging
from .utils import from_root_path

def create_app():
    if os.environ["FLASK_ENV"] == "development":
        handler = {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
            'level': 'DEBUG'
        }
    elif os.environ["FLASK_ENV"] == "production":
        handler = {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': from_root_path("log/{}".format(env['LOG_FILE'])),
            'level': 'DEBUG'
        }
    app = Flask(__name__, instance_relative_config=True)
    app.config['LOGGER_HANDLER_POLICY'] = 'always'  # 'always' (default), 'never',  'production', 'debug'
    app.config['LOGGER_NAME'] = 'application_log' # define which logger to use for Flask
    # app.logger

    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'application': handler
        },
        'loggers': {
            'application_log': {
                'handlers': ['application'],
                'level': 'DEBUG',
                'propagate': True
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['application']
        }
    })

    log_handler = logging.getLogger('application_log').handlers[0]
    app.logger.addHandler(log_handler)

    app.config.from_mapping(env, silent=True)
    app.config["JWT"] = JWTManager(app)
    db.init_app(app)

    migrate.init_app(app)
    app.config['CELERY_CLIENT'] = make_celery(app)

    app.register_blueprint(sessions_controller.blueprint)
    app.register_blueprint(dashboards_controller.blueprint)

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({ 'status': 500, 'error_code': 'ApplicationError', 'message': 'Something went wrong', 'data': {} }), 500
    # app.config["DB"] = init_db_connection(app)
    # app.config["MIGRATE"] = init_migration(app)
    return app
# from .init_envs import app
# from .parse_options import options

# def init_app():
#     app.run()

# def
