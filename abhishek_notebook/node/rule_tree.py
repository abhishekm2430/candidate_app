import pandas as pd
import numpy as np
from node import Node
import os.path
data = pd.read_csv('Rules.csv')

raw_rules = list(data["Patterns"])
section_list = list(data["Sections"])

def clean_rules(raw_rules):
    cleaned_rules = []
    for word in raw_rules:
        character_array = list(word)
        new_list = []
        for index in range(len(character_array)):
            if not(character_array[index] == "“" or character_array[index] == "”" or character_array[index] == '"'):
                new_list.append(character_array[index])
        rule = "".join(new_list)
        cleaned_rules.append(rule)

    return cleaned_rules



def create_rule_tree(cleaned_rules, section_list):
    tree, index = {}, 0
    for rule in cleaned_rules:
        word = rule.split(" ")
        key = word[0]
        root = Node(key)
        if not(tree.get(key)):
            tree[key]=root
        if(len(word) > 1):
            for idx in range(len(word)):
                child = word[idx]
                if not(child == 'AND' or child == 'OR' or child == '+') and idx > 0:
                    tree[key].children[child] = Node(child)
                    tree[key].children[child].children["section"] = section_list[index]
    
        else:
            tree[key].children["section"] = section_list[index]
        index = index + 1

    return tree

cleaned_rules = clean_rules(raw_rules)
tree = create_rule_tree(cleaned_rules, section_list)

