#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

import string
import optparse
import pylab

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
parser.add_option("-z", "--zipf", action="store_true", dest="zipf",
                  default=False, help="plots a zipf's law log.log graph")
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
        if len(args) == 0:
            args = [len(self)]
        samples = list(islice(self, *args))
        
        cumulative = _get_kwarg(kwargs, 'cumulative', False)
        if cumulative:
            freqs = list(self._cumulative_frequencies(samples))
        else:
            freqs = [self[sample] for sample in samples]
        
        fig = pylab.figure(figsize=(12.5, 5))
        ax = fig.add_subplot(1, 1, 1)
         
        if "title" in kwargs:
            ax.set_title(kwargs["title"])
            del kwargs["title"]
        if "xlabel" in kwargs:
            ax.set_xlabel(kwargs["xlabel"])
            del kwargs["xlabel"]
        if "ylabel" in kwargs:
            ax.set_ylabel(kwargs["ylabel"])
            del kwargs["ylabel"]
        
        ax.plot(freqs, 'k+-', **kwargs)
        ax.grid(True, color="silver")
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
              title= u'Gráfico de frequência (' + str(options.limit) + ' termos)',
              ylabel=u'Ocorrências',
              xlabel=u'Termos')
else:
    print 'Data lenght: ' + str(len(data))
    print 'Filtered data: ' + str(len(filtered))
    print 'Distribution of: ' + str(len(dist))
    print '\nCOUNT\tP(%)\tTERM'

    total = len(dist.items())
    limit = options.limit
    if limit == 0:
        limit = total
    for item in dist.items()[:limit]:
        if len(item[0]) >= 1 and item[1] >= options.count:
            percentage = dist.freq(item[0]) * 100
            percentage = '{0:.3}'.format(percentage)
            print '%d\t%s\t%s' % (item[1], percentage + '%', item[0])

if options.zipf is True:
    ranks = []
    freqs = []
    for rank, word in enumerate(dist):
        ranks.append(rank+1)
        freqs.append(dist[word])

    fig = pylab.figure(figsize=(7.5, 5))
    ax = fig.add_subplot(1, 1, 1)
    ax.loglog(ranks, freqs, 'k-')
    ax.grid(True, color="silver")
    ax.set_title(u'Lei de Zipf (' + str(len(dist.items())) + ' termos)')
    ax.set_ylabel(u'Frequência')
    ax.set_xlabel(u'Ordem')
    pylab.tight_layout()
    pylab.savefig('word_frequency_zipf.pdf', dpi=300)
    pylab.show()
