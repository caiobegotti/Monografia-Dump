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

list = [
'cicero_de_republica.xml',
'cicero_brutus.xml',
'cicero_de_divinatione.xml',
'cicero_rhetorica_ad_herennium_sp.xml',
'cicero_de_inventione.xml',
'cicero_de_natura_deorum.xml',
'cicero_de_officiis.xml',
'cicero_tusculanae_disputationes.xml',
'cicero_de_finibus.xml',
'cicero_philippicae.xml',
'cicero_de_oratore.xml',
'cicero_in_verrem.xml',
'cicero_epistulae_ad_familiares.xml',
'cicero_epistulae_ad_atticum.xml',
'cicero_tusculanae_disputationes.xml'
]

total = []
for corpus in list:
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
    if len(stat) >= 25000:
        for item in dist.items()[:150]:
            if len(item[0]) >= 2:
                lemma = lemmatize(item[0])
                if lemma is not None:
                    if lemma not in total:
                        definitions[item[0]] = lemma
                        total.append(lemma)
    print corpus + ': ' + ', '.join(sorted(definitions.values()))
