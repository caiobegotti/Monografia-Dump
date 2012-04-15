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
    regex = re.compile("(?:A|Ap|D|C|Cn|K|L|M|Mam|N|O|P|Q|Qu|S|Sp|Ser|Sex|Sec|Seq|Sept|T|Ti|Tit|Vel|Vo)'?\. [A-Z]{0,}\w{0,} [A-Z]{0,}\w{0,}")
    praenomina = []
    
    for loop in glob.glob('ready/*.txt'):
        with file(loop, 'r') as content:
            text = content.read()
            for entry in regex.findall(text):
                praenomina.append(entry)
    
    return sorted(set(praenomina))

def replacer():
    list = parser()
    regex = re.compile("^(.*)\. ")
    for loop in glob.glob('ready/*.txt'):
        with file(loop, 'r') as content:
            text = content.read()
            replaced = ''
            for entry in list:
                r = regex.search(entry)
                match = r.group(1)
                name = re.sub('^' + match, '(' + match + ')', entry)
                name = name.replace('.', '')
                replaced = re.sub(entry, name, text)
                with file(loop, 'w') as content:
                    content.write(replaced)

if __name__ == "__main__":
    for x in parser():
        print x
