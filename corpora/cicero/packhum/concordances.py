#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

# stems: http://stackoverflow.com/questions/9777871/using-conditional-variables-with-nltks-concordance-module

import glob
import optparse

from nltk.tokenize import word_tokenize
from nltk.corpus.reader import XMLCorpusReader
from nltk import Text

def lookup():
    parser = optparse.OptionParser("Usage: %prog [options]")
    parser.add_option("-l", "--lookup", type="string", dest="term",
                      help="look up concordances for a word")
    parser.add_option("-f", "--fake", action="store_true", dest="fake",
                      default=False, help="considers non-ciceronian texts")
    parser.add_option("-s", "--stem", type="string", dest="stem",
                      help="look up the corpora for a given stem")
 
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
    lookup()
