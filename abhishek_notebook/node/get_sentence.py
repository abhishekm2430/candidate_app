import tika
import re
import numpy as np
import os.path
from tika import parser
tika.initVM()

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