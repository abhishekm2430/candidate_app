import tika
import re
import psycopg2
from flashtext.keyword import KeywordProcessor
import csv
import numpy as np
import os.path
import collections
from tika import parser
tika.initVM()
keyword_processor = KeywordProcessor()

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

def remove_unwanted_keywords(collection):
    print(collection)
    if(collection.get('HERE') is not None):
        del collection['HERE']
    if(collection.get('NOW') is not None):
        del collection['NOW']

    return collection

def get_matched_keyword(cur, key):
    query = "SELECT * FROM keywords WHERE keyword = '{}'".format(key)
    cur.execute(query)
    match_keyword = cur.fetchone()
    return match_keyword


def calc_density(doc_id=None):
    conn, cur = create_database_connection()
    document_path, doc = get_document_path(cur, doc_id)
    inserted_list = []
    technology_path = 'other_files/technologies.csv'

    with open(technology_path, 'r') as csvread:
        filereader = csv.reader(csvread)
        for row in filereader:
            inserted_list.append(row)

    inserted_list = np.delete(inserted_list,[0],axis=0)
    technologies = np.array(inserted_list)[:, 2]
    for keyword in technologies:
        keyword_processor.add_keyword(keyword)

    parsed = parser.from_file(document_path)
    content = parsed["content"]

    matches = findMatches(content)
    total_match = len(matches)
    collection = collections.Counter(np.array(matches))

    for ele in collection:
        collection[ele] = collection[ele] / total_match

    collection = remove_unwanted_keywords(collection)

    for key in collection:
        match_keyword = get_matched_keyword(cur, key)
        query_for_insert = "INSERT INTO candidate_document_keywords(candidate_document_id, keyword_id, density) \
                VALUES ({}, {}, {})".format(doc_id, match_keyword[0], collection[key]) 
        cur.execute(query_for_insert)
        conn.commit()

    conn.close()
