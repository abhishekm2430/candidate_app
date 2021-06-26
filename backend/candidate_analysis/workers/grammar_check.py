import pandas as pd
import textract
import re
from urllib.parse import urlparse
import tldextract
import language_check
from candidate_analysis.models import GrammarRule
import spacy
from spacy import displacy
import json
from candidate_analysis.models import CandidateDocument
from candidate_analysis.framework.db import db
from candidate_analysis.models import CandidateDocumentLine

#from flask_migrate import Migrate
from celery import Celery
cel = Celery('grammar_check', broker = 'redis://localhost:6379//')


nlp = spacy.load('en')
tool = language_check.LanguageTool('en-US')

def getCleanData(param, remove_places=True):
        result = removeSpecialCharacters(param)
        result = removeDuplicateStopWords(result, remove_places)
        if result == '':
            return np.nan
        else:
            return result.lower()

def removeTabs(param):
        result = param
        result = result.replace('\t', ' ')
        result = ' '.join(result.split())
        return result.strip()

def addSpaceBeforeParentheses(param):
        return re.sub('\(+', ' (', param).replace('  ', ' ')


def check_grammer(text):
        matches = tool.check(text)
        grammer_issues = {}
        rule_ids = []
        grammer_issues['total'] = len(matches)
        for i in range(0, len(matches)):
            #print(matches[i].ruleId)
            rule_ids.append(matches[i].ruleId)
        
        grammer_issues['rule_ids'] = rule_ids
        return grammer_issues



#@cel.task
def grammar(doc_id):
            
    grammer_scores = {}
    print('Import Library - Done!')
    doc = CandidateDocument.query.filter_by(candidate_document_id = doc_id).first()
    document_path = doc.document_path
    #text_doc = textract.process(document_path).decode('utf-8')
    text_docx = textract.process(document_path).decode('utf-8')
    #text_pdf = textract.process(document_path).decode('utf-8')
    print('Done!')
    text = 'To work in a creative and challanaging environment that encourages learning and creatively, provides exposure to the new heights and stimulates professional growth.'

    doc1 = nlp(text_docx)
    sentences = list(doc1.sents)

    candidate_doc_lines = []

    count = 1;
    #for index, sentence in enumerate(sentences):
    for sentence in sentences:
        line_text = removeTabs(sentence.text)
        errors = check_grammer(line_text)
        candidate_doc_line = {}
        candidate_doc_line['line_id'] = count
        candidate_doc_line['line_text'] = line_text
        issue = False
        if(errors['total'] > 0):
            issue = True
        candidate_doc_line['issue'] = issue
        candidate_doc_line['errors'] = errors

        total_score = 0
        for i in errors['rule_ids']:
            if(grammer_scores.get(i) == None):
                result = GrammarRule.query.filter_by(grammar_rule_id = i).first()
                if result:
                    if result.score == None:
                        grammer_scores[i] = 0
                    else:
                        grammer_scores[i] = float(result.score)
                        total_score = total_score + grammer_scores[i]
                else:
                    grammer_scores[i] = 0
                    total_score = total_score + 0
            else:
                total_score = total_score + grammer_scores[i]

        if(total_score > 1000):
            total_score = 1000
        total_score = total_score/10

        candidate_doc_line['grammer_score'] = total_score
        candidate_doc_lines.append(candidate_doc_line)
        count = count + 1

    total_doc_score = 0
    for doc_line in candidate_doc_lines:
        document_line = CandidateDocumentLine(candidate_document_id = doc_id, document_line_text = doc_line['line_text'], grammar_issue = doc_line['issue'], grammar_score = doc_line['grammer_score'])
        db.session.add(document_line)
        db.session.commit()
        if(doc_line['grammer_score'] > 0):
            total_doc_score += doc_line['grammer_score']
            print(doc_line)

    if(total_doc_score > 1000):
            total_doc_score = 1000
    total_doc_score = total_doc_score/10

    #doc = CandidateDocument.query.filter_by(candidate_document_id = doc_id).first()
    #db.session.add(doc)
    doc.grammar_score = 100 - total_doc_score
    db.session.commit()

    print(total_doc_score)
    return total_doc_score


    # with open('candidate_doc_lines.json', 'w') as fp:
    #     json.dump(candidate_doc_lines, fp)


#grammar()
