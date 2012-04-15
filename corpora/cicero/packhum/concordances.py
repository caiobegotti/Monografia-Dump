#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import glob
import optparse

from nltk.tokenize import word_tokenize

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
        print options

if __name__ == "__main__":
    search()
