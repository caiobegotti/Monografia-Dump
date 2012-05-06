#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

from CatXMLReader import CategorizedXMLCorpusReader

from CatXMLReader import stopless
from CatXMLReader import punctless

from nltk.corpus import stopwords
from nltk.corpus import cicero

from nltk import FreqDist
from nltk import Text

for corpus in cicero.fileids():
    print 'Corpus: ' + corpus

    reader = CategorizedXMLCorpusReader(cicero.root,
                                        cicero.abspaths(),
                                        cat_file='categories.txt')
    data = Text(reader.words([corpus]))
    dist = FreqDist(data)
   
    print 'Data lenght: ' + str(len(data))
    print 'Distribution of: ' + str(len(dist))
    print '\nCOUNT\tP(%)\tTERM'

    total = len(dist.items())
    for item in dist.items():
        if len(item[0]) >= 1:
            percentage = dist.freq(item[0]) * 100
            percentage = '{0:.3}'.format(percentage)
            print '%d\t%s\t%s' % (item[1], percentage + '%', item[0])
