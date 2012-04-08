#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

# reference: https://gist.github.com/2307114
# double-check: http://en.wiktionary.org/wiki/Appendix:Roman_praenomina

import codecs
import glob
import re

def parser():
    regex = re.compile("[A-Z]'?\w{0,4}\. [A-Z]{0,}\w{0,} [A-Z]{0,}\w{0,}")
    praenomina = []
    
    for file in glob.glob('./*.xml'):
        content = codecs.open(file, "r", "utf8")
        text = content.read()
        for entry in regex.findall(text):
            praenomina.append(entry)
    
    return sorted(set(praenomina))

def replacer():
    list = parser()
    regex = re.compile("^(.*)\. ")
    for entry in list:
        r = regex.search(entry)
        match = r.group(1)
        name = re.sub('^' + match, '(' + match + ')', entry)
        print 'era -> "' + entry + '" e vai virar -> "' + name.replace('.', '') + '"'

if __name__ == "__main__":
    replacer()
