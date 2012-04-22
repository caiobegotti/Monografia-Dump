#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import string

from itertools import islice

from CatXMLReader import CategorizedXMLCorpusReader

from nltk.corpus import stopwords
from nltk.corpus import cicero

from nltk import FreqDist
from nltk import Text

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
cats = cicero.root + '/categories.txt'
reader = CategorizedXMLCorpusReader('/', fileids, cat_file=cats)

data = reader.words(fileids)
stop = stopwords.words('latin')
words = Text(reader.words(fileids))

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

punctuation = list(punct)

list = [x for x in data if x not in stop]
filtered = [x for x in list if x not in punctuation]

final = []
for f in filtered:
    if f.isalpha():
        final.append(f)

dist = MyFreqDist(Text(final))
keys = dist.keys()

for k in keys[0:100]:
    print k
