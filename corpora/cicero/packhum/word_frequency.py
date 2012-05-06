#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import string
import optparse

from itertools import islice

from CatXMLReader import CategorizedXMLCorpusReader

from CatXMLReader import stopless
from CatXMLReader import punctless

from nltk.corpus import stopwords
from nltk.corpus import cicero

from nltk import FreqDist
from nltk import Text

parser = optparse.OptionParser("Usage: %prog [options]")
parser.add_option("-s", "--stopwords", action="store_true", dest="stopwords",
                  default=False, help="include stopwords in the calculations")
parser.add_option("-p", "--plot", action="store_true", dest="plot",
                  default=False, help="plot the frequency distribution of terms")
parser.add_option("-l", "--limit", type="int", dest="limit",
                  default=100, help="prints calculation of first (default: 100) terms")
parser.add_option("-c", "--count", type="int", dest="count",
                  default=100, help="shows only counts higher than (default: 100)")

(options, args) = parser.parse_args()
#if options is None:
#    parser.print_help()
#    exit(-1)

class MyFreqDist(FreqDist):
    def plot(self, *args, **kwargs):
        try:
            import pylab
        except ImportError:
            raise ValueError('The plot function requires the matplotlib package (pylab).')
        
        if len(args) == 0:
            args = [len(self)]
        samples = list(islice(self, *args))
        
        cumulative = _get_kwarg(kwargs, 'cumulative', False)
        if cumulative:
            freqs = list(self._cumulative_frequencies(samples))
        else:
            freqs = [self[sample] for sample in samples]
        
        if not "linewidth" in kwargs:
            kwargs["linewidth"] = 2
        if "title" in kwargs:
            pylab.title(kwargs["title"])
            del kwargs["title"]
        if "xlabel" in kwargs:
            pylab.xlabel(kwargs["xlabel"])
            del kwargs["xlabel"]
        if "ylabel" in kwargs:
            pylab.ylabel(kwargs["ylabel"])
            del kwargs["ylabel"]
        
        pylab.grid(True, color="silver")
        pylab.plot(freqs, 'ko-', **kwargs)
        pylab.xticks(range(len(samples)), [str(s) for s in samples], rotation=90)
        pylab.tight_layout()
        pylab.savefig('word_frequency.pdf', dpi=300)
        pylab.show()

def _get_kwarg(kwargs, key, default):
    if key in kwargs:
        arg = kwargs[key]
        del kwargs[key]
    else:
        arg = default
    return arg
        
categories = 'categories.txt'
reader = CategorizedXMLCorpusReader(cicero.root,
                                    cicero.abspaths(),
                                    cat_file=categories)

data = reader.words(cicero.fileids())

if options.stopwords is True:
    filtered = punctless(data)
else:
    filtered = punctless(stopless(data))

dist = MyFreqDist(Text(filtered))

if options.plot is True:
    dist.plot(options.limit,
              cumulative=False,
              title=u'Gráfico de frequência (100 termos mais usados)',
              ylabel=u'Ocorrências',
              xlabel=u'Termos')
else:
    for item in dist.items()[:options.limit]:
        if len(item[0]) > 1 and item[1] >= options.count:
            print item[0] + ':' + str(item[1])
