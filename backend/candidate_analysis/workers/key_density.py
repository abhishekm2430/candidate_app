# from celery import Celery
# cel = Celery('key_density', broker = 'redis://localhost:6379//')
import tika
import re
from flashtext.keyword import KeywordProcessor
import csv
import numpy as np
import os.path
import collections
from tika import parser
from candidate_analysis.models import CandidateDocument
from candidate_analysis.models import CandidateDocumentKeyword
from candidate_analysis.framework.db import db
from candidate_analysis.framework.utils import from_root_path
from candidate_analysis.models import Keyword
tika.initVM()
keyword_processor = KeywordProcessor()
# print("Initiallinging celery")
# cel = app.config['CELERY_CLIENT']
def getSentences(content):
    sentences = []
    temp = ''
    isStop = False
    for c in content:
        if(isStop):
            if(c == ' '): 
                temp += c
            elif(c == '\n'):
                sentences.append(temp)
                isStop = False
                temp = ''
            else:
                isStop = False
                temp += c
        elif(c != '\n'):
            if(c == '.'):
                isStop = True
            temp += c

    return sentences


def findMatches(content):
    sentences = getSentences(content)
    index = 0
    found = []

    for sent in sentences:
        keywords_found = keyword_processor.extract_keywords(sent)
        
        for keyword in keywords_found:
            found.append(keyword)
        index += 1
    return found

#@cel.task()
def calc_density(doc_id=None):
    print("code for calculating density")
    #keyword_processor = KeywordProcessor()
    inserted_list = []
    doc = CandidateDocument.query.filter_by(candidate_document_id = doc_id).first()
    document_path = doc.document_path
    technology_path = from_root_path('data/technologies.csv')

    with open(technology_path, 'r') as csvread:
        filereader = csv.reader(csvread)
        for row in filereader:
            inserted_list.append(row)

    inserted_list = np.delete(inserted_list,[0],axis=0)
    technologies = np.array(inserted_list)[:, 2]
    for keyword in technologies:
        keyword_processor.add_keyword(keyword)

    # document_path = (path obtained from database)

    parsed = parser.from_file(document_path)
    # print(parsed["metadata"])
    content = parsed["content"]

    matches = findMatches(content)
    TotalMatch = len(matches)
    collection = collections.Counter(np.array(matches))

    for ele in collection:
        collection[ele] = collection[ele] / TotalMatch

    print(collection)
    if(collection.get('HERE') is not None):
        del collection['HERE']
    if(collection.get('NOW') is not None):
        del collection['NOW']

    for key in collection:
        match_keyword = Keyword.query.filter_by(keyword = key).first()
        candidate_doc_keyword = CandidateDocumentKeyword(candidate_document_id = doc_id, keyword_id = match_keyword.keyword_id, density = collection[key])
        db.session.add(candidate_doc_keyword)
        db.session.commit()

    #return collection
    #load_json(collection)


#result = calc_density()
def load_json(collection):
    import json
    with open('result1.json', 'w') as fp:
        json.dump(collection, fp)