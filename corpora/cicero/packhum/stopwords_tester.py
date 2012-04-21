#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import glob

from nltk import Text
from nltk.tokenize import word_tokenize
from nltk.corpus import cicero

from CatXMLReader import CategorizedXMLCorpusReader

def stopwords():
    stopwords = []
    with file('../../stopwords/latin.txt', 'r') as content:
        for line in content.readlines():
            stopwords.append(line.replace('\n',''))
    return stopwords

def tokenizer():
    fileids = cicero.abspaths()
    reader = CategorizedXMLCorpusReader('/', fileids, cat_file='cats.txt')
    tokens = Text(reader.words(fileids))
    return tokens

tokens = tokenizer()
for s in stopwords():
    counter = tokens.count(s)
    percentage = (float(counter)/float(len(tokens)))*100
    print "%d\t%f\t%s" % (counter, percentage, s)
