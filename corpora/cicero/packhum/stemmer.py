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


# stackoverflow.com/questions/3411006/fastest-implementation-to-do-multiple-string-substitutions-in-python
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


def stemmer(entry):
    orig = []
    nouns = []
    verbs = []

    entry = entry.split()[0]

    # step 2
    entry = multi_replace([('j', 'i'), ('v', 'u')], entry.replace('\n', ''))

    # hackish buffer
    buffer = entry
    orig.append(buffer)

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
            break

    # step 5
    if len(entry) >= 2:
        nouns.append(entry)

    # step 6
    i = ['iuntur', 'erunt', 'untur', 'iunt', 'unt', 'i']
    bi = ['beris', 'bor', 'bo', 'bi']
    eri = ['ero', 'eri']

    # repeat removal of que for verbs
    if buffer not in que:
        if buffer.endswith('que'):
            buffer = buffer[:-3]
    else:
        nouns.append(buffer)
        verbs.append(buffer)

    endings = [i, bi, eri]
    for ending in [i]:
        buffer = ending_fixer(buffer, ending)

    for v in verb_suffix:
        if buffer.endswith(v):
            buffer = buffer[:-len(v)]

    # step 7
    if len(buffer) >= 2:
        verbs.append(buffer)

    return zip(orig, nouns, verbs)


def ending_fixer(buffer, ending):
    items = ending[:-1]
    toremove = ending[-1]
    for item in items:
        if buffer.endswith(item):
            buffer = buffer.replace(item, toremove)
    return buffer


if __name__ == "__main__":
    # step 1
    with open(sys.argv[1], 'r') as joined:
        total = 0
        ok = 0
        for line in joined:
            total += 1
            res = stemmer(line)
            if res is not None:
                for r in res:
                    outline = '{0: <30}{1: <25}{2}'.format(r[0], r[1], r[2])
                    print(outline)
                    compareto = multi_replace([('j', 'i'), ('v', 'u')], line.replace('\n', ''))
                    if cmp(compareto, outline) == 0:
                        ok += 1
                    else:
                        print("ERROR: {} | {}").format(compareto, outline)
        print("ACCURACY: {}% ({}/{})").format(float(100*ok)/float(total), ok, total)
