#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

# reference: the schinke latin stemming algorithm in python
# http://snowball.tartarus.org/otherapps/schinke/intro.html

import sys

que = ['atque', 'quoque', 'neque', 'itaque', 'absque', 'apsque', 'abusque',
'adaeque', 'adusque', 'deniquep', 'deque', 'susque', 'oblique', 'peraeque',
'plenisque', 'quandoque', 'quisque', 'quaequep', 'cuiusque', 'cuique',
'quemque', 'quamque', 'quaque', 'quique', 'quorumque', 'quarumque',
'quibusque', 'quosque', 'quasque', 'quotusquisque', 'quousque', 'ubique',
'undique', 'usque', 'uterque', 'utique', 'utroque', 'utribique', 'torque',
'coque', 'concoque', 'contorque', 'detorque', 'decoque', 'excoque',
'extorque', 'obtorque', 'optorque', 'retorque', 'recoque', 'attorque',
'incoque', 'intorque', 'praetorque']

noun_suffix = ['ibus', 'ius', 'ae', 'am', 'as', 'em', 'es', 'ia', 'is',
'nt', 'os', 'ud', 'um', 'us', 'a', 'e', 'i', 'o', 'u']

verb_suffix = ['iuntur', 'beris', 'erunt', 'untur', 'iunt', 'mini', 'ntur',
'stis', 'bor', 'ero', 'mur', 'mus', 'ris', 'sti', 'tis', 'tur', 'unt',
'bo', 'ns', 'nt', 'ri', 'm', 'r', 's', 't']

nouns = []
verbs = []

# http://stackoverflow.com/questions/3411006/fastest-implementation-to-do-multiple-string-substitutions-in-python
# this is the multiple replacing algorithm proposed by matt anderson at stackoverflow in 2010
# it should perform faster than python's native replace method on huge corpora
def multi_replace(pairs, text):
    stack = list(pairs)
    stack.reverse()
    def replace(stack, parts):
        if not stack:
            return parts
        stack = list(stack) 
        from_, to = stack.pop()
        # debug
        # print 'split (%r=>%r)' % (from_, to), parts
        split_parts = [replace(stack, part.split(from_)) for part in parts]
        parts = [to.join(split_subparts) for split_subparts in split_parts]
        # debug
        # print 'join (%r=>%r)' % (from_, to), parts
        return parts
    return replace(stack, [text])[0]

def stemmer():
    for entry in sys.stdin.readlines():
        # step 2
        entry = multi_replace([('j', 'i'), ('v', 'u')], entry.replace('\n',''))

        # step 3
        if entry not in que:
            if entry.endswith('que'):
                entry = entry[:-3]
        else:
            nouns.append(entry)
            verbs.append(entry)

        # step 4
        for s in noun_suffix:
            if entry.endswith(s):
                entry = entry[:-len(s)]

        # step 5
        if len(entry) >= 2:
            nouns.append(entry)

        # step 6
        i = ['iuntur', 'erunt', 'untur', 'iunt', 'unt']
        bi = ['beris', 'bor', 'bo']
        eri = ['ero']
        for s in verb_suffix:
            if entry.endswith(s):
                if s in i:
                    entry.replace(s, 'i')
                elif s in bi:
                    entry.replace(s, 'bi')
                elif s in eri:
                    entry.replace(s, 'eri')
                else:
                    entry = entry[:-len(s)]

        # step 7
        if len(entry) >= 2:
            verbs.append(entry)

    print zip(verbs, nouns)

if __name__ == "__main__":
    # step 1
    stemmer()
