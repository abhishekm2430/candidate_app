from celery import Celery
cel = Celery('celery_tasks', broker = 'redis://localhost:6379//')

from grammar_check_2 import grammar
from key_density_2 import calc_density

@cel.task
def grammar_score_calculation(doc_id):
    grammar(doc_id)

@cel.task
def keyword_density_calculation(doc_id):
    calc_density(doc_id)
