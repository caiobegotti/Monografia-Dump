#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

# prototype: cat ../../stopwords/latin.* | sort -u | while read i; do export x=$(grep -c "^${i}$" /tmp/full.txt); export t=$(wc -l /tmp/full.txt | cut -d' ' -f2); echo -e "${x}\t${t}\t${i}\t\t$(echo "(${x} / ${t}) * 100" | bc -l)"; done

import glob

from nltk.tokenize import word_tokenize

stopwords = []
with file('../../stopwords/latin.txt', 'r') as content:
    for line in content.read():
        stopwords.append(line)

text = []
for loop in glob.glob('ready/*.txt'):
    with file(loop, 'r') as content:
        text.append(content.read())

data = ' '.join(text)
tokens = word_tokenize(data)
print stopwords