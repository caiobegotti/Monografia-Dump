#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

# this is a python query script to interface with
# CHLT LEMLAT's web lemmatizer for latin:
# http://www.ilc.cnr.it/lemlat/lemlat/index.html

from sys import argv
from sys import exit

from lxml import etree

def lemmatize(term):
    term = term.lower().strip()
    parser = etree.HTMLParser()

    tree = etree.parse('http://www.ilc.cnr.it/lemlat/cgi-bin/LemLat_cgi.cgi?World+Form=' + term, parser)
    element = tree.xpath('//u//text()')
    if element and element[0] is not None:
        return element[0]

if __name__ == "__main__":
    if not len(argv) == 2:
        exit('Usage: ' + argv[0] + " 'latin word to lemmatize'")
    else:
        res = lemmatize(argv[1])
        if res is not None:
            print res
