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

# fancy dictionary
from collections import defaultdict

list = [
'cicero_de_republica.xml',
'cicero_brutus.xml',
'cicero_de_divinatione.xml',
'cicero_rhetorica_ad_herennium_sp.xml',
'cicero_de_inventione.xml',
#'cicero_de_natura_deorum.xml',
#'cicero_de_officiis.xml',
#'cicero_de_finibus.xml',
#'cicero_philippicae.xml',
#'cicero_de_oratore.xml',
#'cicero_in_verrem.xml',
#'cicero_epistulae_ad_familiares.xml',
#'cicero_epistulae_ad_atticum.xml',
#'cicero_tusculanae_disputationes.xml'
]

total = defaultdict(int)
for corpus in cicero.fileids():
    print corpus
    reader = CategorizedXMLCorpusReader(cicero.root,
                                        cicero.abspaths(),
                                        cat_file='categories.txt')
    try:
        dist = FreqDist(Text(punctless(stopless(reader.words([corpus])))))
    except UnicodeEncodeError as e:
        print str(e)
        break

    definitions = {}
    stat = reader.words([corpus])
    for item in dist.items()[:1000]:
        entry = item[0]
        if len(entry) >= 2:
            lemma = lemmatize(item[0])
            if lemma is not None:
                if lemma not in total:
                    definitions[entry] = lemma
                num = dist[entry]
                total[lemma] += num
    #print sum(total.values()), len(stat)
    #print corpus + ': ' + ', '.join(sorted(definitions.values()))

res = sorted(total.items(), key=lambda x: x[1], reverse=True)
for r in res:
    print str(r[1]) + ':' +  r[0]

print sum(total.values())
