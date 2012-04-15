#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import glob
import optparse

from nltk.tokenize import word_tokenize
from nltk.corpus.reader import XMLCorpusReader
from nltk import Text

def search():
    parser = optparse.OptionParser("Usage: %prog [options]")
    parser.add_option("-s", "--search", type="string", dest="term",
                      help="search concordances for a word")
    parser.add_option("-f", "--fake", action="store_true", dest="fake",
                      default=False, help="considers non-ciceronian texts")
 
    (options, args) = parser.parse_args()
    if options.term is None:
        parser.print_help()
        exit(-1)
    else:
        content = corpora_loader()
        text = content.concordance(options.term)
        print text

def corpora_loader():
    data = ''
    for loop in glob.glob('academica.xml'):
        reader = XMLCorpusReader('./', loop)
        data = Text(reader.words())
    return data

if __name__ == "__main__":
    search()
