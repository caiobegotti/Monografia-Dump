#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import glob
import optparse
import string

from CatXMLReader import CategorizedXMLCorpusReader
from CatXMLReader import ciceroabbr

from nltk.corpus import cicero

from nltk import ConcordanceIndex
from nltk import Text

parser = optparse.OptionParser("Usage: %prog [options]")
parser.add_option("-l", "--lookup", type="string", dest="term",
                  help="look up concordances for a word")
parser.add_option("-f", "--fake", action="store_true", dest="fake",
                  default=False, help="considers non-ciceronian texts")
parser.add_option("-w", "--width", type="int", dest="width",
                  default=150, help="width of the context data")
parser.add_option("-c", "--count", type="int", dest="count",
                  default=1, help="how many matches to display")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  default=False, help="print headers or stats")

(options, args) = parser.parse_args()
if options.term is None:
    parser.print_help()
    exit(-1)

reset = '\033[1;m'
red = '\033[1;31m'
green = '\033[1;32m'
yellow = '\033[1;33m'
blue = '\033[1;34m'

class MyText(Text):
    def search(self, corpus, word, width, lines):
        res = self.concordance(word, width, lines, corpus)
        if res is not None:
            print res

    def concordance(self, corpus, word, width=150, lines=1):
        if '_concordance_index' not in self.__dict__:
            if options.verbose is True:
                print "Building index..."
            self._concordance_index = MyConcordanceIndex(self.tokens, key=lambda s:s.lower())           
        self._concordance_index.print_concordance(width, lines, corpus, word)

class MyConcordanceIndex(ConcordanceIndex):
    def print_concordance(self, corpus, word, width=150, lines=1):
        half_width = (width - len(word) - 2) / 2
        context = width/4
        
        offsets = self.offsets(word)
        if offsets:
            lines = min(lines, len(offsets))
            if options.verbose is True:
                print "Displaying %s of %s matches:" % (lines, len(offsets))
            for i in offsets:
                if lines <= 0:
                    break
                left = (' ' * half_width +
                        ' '.join(self._tokens[i-context:i]))
                right = ' '.join(self._tokens[i+1:i+context])
                left = left[-half_width:]
                right = right[:half_width]
                abbr = ciceroabbr(corpus)
                abbrinfo = '[' + abbr + ']'
                abbrinfo = abbrinfo.center(12, ' ').replace(abbr, green + abbr + reset)
                print abbrinfo + '[' + left, yellow + self._tokens[i] + reset, right + ']'
                lines -= 1
        else:
            if options.verbose is True:
                print "No matches found for " + word + " in " + corpus
            #exit(-1)
 
def corpora_loader(corpus, fake):
    reader = CategorizedXMLCorpusReader(cicero.root,
                                        cicero.abspaths(),
                                        cat_file='categories.txt')

    if fake is True:
        categories = cicero.categories()
    else:
        categories = cicero.categories()[:-1]
   
    data = Text(reader.words([corpus]))
    return data

if __name__ == "__main__":
    for corpus in cicero.fileids():
        if corpus in cicero.fileids(['spurious']) and options.fake is False:
            continue
        content = corpora_loader(corpus, fake=options.fake)
        text = MyText(content)
        res = text.search(options.term,
                          options.width,
                          options.count,
                          corpus)
        if res is not None:
            print res
