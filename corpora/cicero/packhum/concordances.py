#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import glob
import optparse

from CatXMLReader import CategorizedXMLCorpusReader

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
                  default=25, help="how many matches to display")
parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
                  default=False, help="do not print headers or stats")

(options, args) = parser.parse_args()
if options.term is None:
    parser.print_help()
    exit(-1)

reset = '\033[1;m'
red = '\033[1;31m'

class MyText(Text):
    def search(self, word, width, lines):
        res = self.concordance(word, width, lines)
        if res is not None:
            print res

    def concordance(self, word, width=150, lines=25):
        if '_concordance_index' not in self.__dict__:
            if options.quiet is False:
                print "Building index..."
            self._concordance_index = MyConcordanceIndex(self.tokens, key=lambda s:s.lower())           
        self._concordance_index.print_concordance(word, width, lines)

class MyConcordanceIndex(ConcordanceIndex):
    def print_concordance(self, word, width=150, lines=25):
        half_width = (width - len(word) - 2) / 2
        context = width/4
        
        offsets = self.offsets(word)
        if offsets:
            lines = min(lines, len(offsets))
            if options.quiet is False:
                print "Displaying %s of %s matches:" % (lines, len(offsets))
            for i in offsets:
                if lines <= 0:
                    break
                left = (' ' * half_width +
                        ' '.join(self._tokens[i-context:i]))
                right = ' '.join(self._tokens[i+1:i+context])
                left = left[-half_width:]
                right = right[:half_width]
                print '[' + left, red + self._tokens[i] + reset, right + ']'
                lines -= 1
        else:
            if options.quiet is False:
                print "No matches found for " + word
            exit(-1)
 
def corpora_loader(fake):
    reader = CategorizedXMLCorpusReader(cicero.root,
                                        cicero.abspaths(),
                                        cat_file='categories.txt')

    if fake is True:
        categories = cicero.categories()
    else:
        categories = cicero.categories()[:-1]
    
    data = Text(reader.words(categories=categories)) 
    return data

if __name__ == "__main__":
    content = corpora_loader(fake=options.fake)
    text = MyText(content)
    res = text.search(options.term,
                      options.width,
                      options.count)
    if res is not None:
        print res
