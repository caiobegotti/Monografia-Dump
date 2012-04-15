#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import glob

from nltk.tokenize import word_tokenize

def stopwords():
    stopwords = []
    with file('../../stopwords/latin.txt', 'r') as content:
        for line in content.readlines():
            stopwords.append(line.replace('\n',''))
    return stopwords

def tokenizer():
    text = []
    for loop in glob.glob('ready/*.txt'):
        with file(loop, 'r') as content:
            text.append(content.read())
    tokens = word_tokenize(' '.join(text))
    return tokens

tokens = tokenizer()
for s in stopwords():
    counter = tokens.count(s)
    percentage = (float(counter)/float(len(tokens)))*100
    print "%d\t%f\t%s" % (counter, percentage, s)
