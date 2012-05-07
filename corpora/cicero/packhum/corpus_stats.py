#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

from CatXMLReader import CategorizedXMLCorpusReader
from CatXMLReader import stopless
from CatXMLReader import punctless

from nltk.corpus import cicero

from nltk import FreqDist
from nltk import Text

# experimental
from latin_lemmatizer import lemmatize

for corpus in cicero.fileids():
    reader = CategorizedXMLCorpusReader(cicero.root,
                                        cicero.abspaths(),
                                        cat_file='categories.txt')
    try:
        dist = FreqDist(Text(punctless(stopless(reader.words([corpus])))))
    except UnicodeEncodeError as e:
        print str(e)
        break

    rank = []
    stat = reader.words([corpus])
    if len(stat) >= 25000:
        for item in dist.items()[:100]:
            if len(item[0]) >= 2:
                lemma = ' (%s)' % lemmatize(item[0])
                rank.append(item[0] + lemma)
        print '\n%s: %s' % (corpus, ', '.join(rank))
