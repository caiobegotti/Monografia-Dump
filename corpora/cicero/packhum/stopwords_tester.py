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
    with file('../../stopwords/latin', 'r') as content:
        for line in content.readlines():
            stopwords.append(line.replace('\n',''))
    return stopwords

def tokenizer():
    fileids = cicero.abspaths()
    reader = CategorizedXMLCorpusReader('/', fileids, cat_file='categories.txt')
    tokens = Text(reader.words(fileids))
    return tokens

matches = []
tokens = tokenizer()

for s in stopwords():
    counter = tokens.count(s)
    matches.append(counter)
    percentage = (float(counter)/float(len(tokens)))*100
    print "%d\t%f\t%s" % (counter, percentage, s)

total_stat = (float(sum(matches))/float(len(tokens)))*100
print "stopwords: %d (%f percent)" % (sum(matches), total_stat)
