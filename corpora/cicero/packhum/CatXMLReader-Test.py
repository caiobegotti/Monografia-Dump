#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import string

from itertools import islice

from CatXMLReader import CategorizedXMLCorpusReader

from CatXMLReader import stopless
from CatXMLReader import punctless

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
            print "%4s" % str(samples[i]),
        print
        
        for i in range(len(samples)):
            print "%4d" % freqs[i],
        print

def _get_kwarg(kwargs, key, default):
    if key in kwargs:
        arg = kwargs[key]
        del kwargs[key]
    else:
        arg = default
    return arg

fileids = cicero.abspaths()
cats = cicero.root + '/categories.txt'
reader = CategorizedXMLCorpusReader('/', fileids, cat_file=cats)

data = reader.words(fileids)
filtered = punctless(stopless(data))
dist = MyFreqDist(Text(filtered))

for item in dist.items():
    if len(item[0]) > 1 and item[1] >= 100:
        print item[0] + ':' + str(item[1])

dist.plot(500, cumulative=False)
