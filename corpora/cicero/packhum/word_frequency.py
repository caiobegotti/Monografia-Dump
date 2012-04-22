#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import string

from nltk import Text
from nltk import FreqDist

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords
from nltk.corpus import cicero

from CatXMLReader import CategorizedXMLCorpusReader

class MyFreqDist(FreqDist):
    def tabulate(self, *args, **kwargs):
        if len(args) == 0:
            args = [len(self)]
        
        samples = list(islice(self, *args))
        cumulative = _get_kwarg(kwargs, 'cumulative', False)
        
        if cumulative:
            freqs = list(self._cumulative_frequencies(samples))
        else:
            freqs = [self[sample] for sample in samples]
        
        for i in range(len(samples)):
            print '4s'
            print "%4s" % str(samples[i]),
        print
        
        for i in range(len(samples)):
            print "%4d" % freqs[i],
        print

fileids = cicero.abspaths()
reader = CategorizedXMLCorpusReader('/', fileids, cat_file='categories.txt')
stopwords = stopwords.words('latin')
punct = string.punctuation
punct += u'\u00a7'
punct += u'\u00b3'
punct += u'\u00b2'
punct += u'\u00b7'
punct += u'\u00b9'
punct += u'\u2014'
punct += u'\u2019'
punct += u'\u2020'
punct += u'\u2184'
punct += u'\u221e'
punct += u'\u23d1'
words = reader.words(fileids)
for word in words:
    if word in stopwords or word in punct:
        words.remove(word)


with file('./cicero.txt', 'w') as content:
    content.write(words)

print len(words), len(reader.words(fileids))

#tokens = Text(filtered)[0:200]
#dist = MyFreqDist(tokens)
#print dist.tabulate()
