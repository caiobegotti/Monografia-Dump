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

if not len(argv) == 2:
    exit('Usage: ' + argv[0] + " 'latin word to lemmatize'")

term = argv[1].lower().strip()
parser = etree.HTMLParser()

try:
    tree = etree.parse('http://www.ilc.cnr.it/lemlat/cgi-bin/LemLat_cgi.cgi?World+Form=' + term, parser)
    element = tree.xpath('//tr/td/ol/li/u//text()')
    print element[0]
except:
    exit('Word form not recognized or lemlat service is unavailable now')
