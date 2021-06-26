import pandas as pd
import tika
import numpy as np
from node import Node
import re
from nltk.stem import WordNetLemmatizer
from get_sentence import getSentences
from rule_tree import tree
import os.path
from tika import parser
tika.initVM()
lemmatizer = WordNetLemmatizer()

class Document:
    def __init__(self, filename):
        parsed = parser.from_file(filename)
        content = parsed["content"]
        self.sentences = getSentences(content)

    def get_root_words(self, word, next_word):
        word = lemmatizer.lemmatize(word.replace(".", ""))
        word = lemmatizer.lemmatize(word.replace(".", ""), pos = 'v')
        next_word = lemmatizer.lemmatize(next_word.replace(".", ""))
        next_word = lemmatizer.lemmatize(next_word.replace(".", ""), pos = 'v')
        if(word.isnumeric()):
            word = 'NUM'

        return word, next_word ;

    def regex_mathching(self, word):
        regex = re.findall(r'\d+th', word)
        return regex

    def match_rules(self, parent, next_word):
        child = parent.children.get(next_word)
        if child:
            if(type(child) is Node):
                return child.children.get("section")
            else:
                return child
        else:
            return parent.children.get("section")
# ' |;|,|·|:|\t'
    def generate_lines_info(self):
        lines_info, line_id = [], 1
        for sent in self.sentences:
            sections = []
            wordlist = re.split('[.!#$%*^&·():’<>?/\|}{~,-]|\s',sent.lower())
            wordlist = [c for c in wordlist if c != ''] 
            print(wordlist) 
            for index in range(len(wordlist)-1):
                word, next_word = self.get_root_words(wordlist[0], wordlist[index + 1])
                if(self.regex_mathching(word)):
                    sections.append("education")
                    break
                parent = tree.get(word)
                if parent:
                    sections.append(self.match_rules(parent, next_word))
                    break
                    
            info = {"id": line_id, "line_content": sent, "sections": sections}
            lines_info.append(info)
            line_id += 1
        return lines_info

doc = Document('/home/abhishek/testing1.docx')
line_details = doc.generate_lines_info()
for line in line_details:
    print(line, "\n")





#print(doc._Document__regex_mathching("103th4rjks"))













