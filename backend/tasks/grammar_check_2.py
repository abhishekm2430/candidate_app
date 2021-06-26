import pandas as pd
import textract
import re
import psycopg2
from urllib.parse import urlparse
import tldextract
import language_check
import spacy
from spacy import displacy
import json

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

def create_database_connection():
    conn = psycopg2.connect(database = "candidate_analysis", user = "postgres", password = "mindfire", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    return conn, cur ;

def get_document_path(cur, doc_id):
    query = "SELECT * FROM candidate_documents WHERE candidate_document_id = " + str(doc_id)
    cur.execute(query)
    doc = cur.fetchone()
    print(doc)
    document_path = str(doc[6])
    return document_path, doc ;

def get_grammar_rule(cur, rule_id):
    query = "SELECT * FROM grammar_rules WHERE grammar_rule_id = '{}'".format(str(rule_id))
    cur.execute(query)
    result = cur.fetchone()
    return result


def get_document_lines_info(cur, sentences):
    candidate_doc_lines, grammer_scores = [],{}
    count = 1;
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
        for rule_id in errors['rule_ids']:
            if(grammer_scores.get(rule_id) == None):
                result = get_grammar_rule(cur, rule_id)
                if result:
                    if result[2] == None:
                        grammer_scores[rule_id] = 0
                    else:
                        grammer_scores[rule_id] = float(result[2])
                        total_score = total_score + grammer_scores[rule_id]
            else:
                total_score = total_score + grammer_scores[rule_id]

        if(total_score > 1000):
            total_score = 1000
        total_score = total_score/10

        candidate_doc_line['grammer_score'] = total_score
        candidate_doc_lines.append(candidate_doc_line)
        count = count + 1
    return candidate_doc_lines


def grammar(doc_id):
    conn, cur = create_database_connection()
    document_path, doc = get_document_path(cur, doc_id)
    text_docx = textract.process(document_path).decode('utf-8')

    doc1 = nlp(text_docx)
    sentences = list(doc1.sents)
    candidate_doc_lines = get_document_lines_info(cur, sentences)

    total_doc_score = 0
    for doc_line in candidate_doc_lines:
        query = "INSERT INTO candidate_document_lines(candidate_document_id, document_line_text, grammar_issue, grammar_score) \
                VALUES ({}, '{}', {}, {})".format(doc_id, doc_line['line_text'], doc_line['issue'], doc_line['grammer_score'])

        cur.execute(query)
        conn.commit()
        if(doc_line['grammer_score'] > 0):
            total_doc_score += doc_line['grammer_score']
            print(doc_line)

    if(total_doc_score > 1000):
            total_doc_score = 1000
    total_doc_score = 100 - total_doc_score/10

    query = "UPDATE candidate_documents SET grammar_score = {} WHERE candidate_document_id = {}".format(total_doc_score, str(doc[0]))
    cur.execute(query)
    conn.commit()
    conn.close()

    print(total_doc_score)
    return total_doc_score
