#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import codecs

def normalizer():
    for loop in glob.glob('ready/*.txt'):
        text = ''
        with file(loop, 'r') as content:
            text = content.read().lower()

        # fixes the linebreaking of corpora
        text = text.replace("- ", "")

        # fixes unused letters for their real latin ones
        text = text.replace("v","u")
        text = text.replace("j","i")
       
        with file(loop, 'w') as content:
            content.write(text)

if __name__ == "__main__":
    normalizer()
