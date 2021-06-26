from celery import Celery
from candidate_analysis.config.environments import env

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend = env["CELERY_BROKER"],
        broker = env["CELERY_BACKEND"]
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery