# http://stackoverflow.com/questions/6849600/does-anyone-have-a-categorized-xml-corpus-reader-for-nltk

# standard nltk classes
from nltk.corpus.reader import CategorizedCorpusReader
from nltk.corpus.reader import XMLCorpusReader

# stopwords (i.e. latin ones)
from nltk.corpus import stopwords

# for CategorizedCorpusReader's init
from nltk.compat import defaultdict

# punctuations load
import string

class MyCategorizedCorpusReader(CategorizedCorpusReader):
    def _init(self):
        self._f2c = defaultdict(set)
        self._c2f = defaultdict(set)

        if self._pattern is not None:
            for file_id in self._fileids:
                category = re.match(self._pattern, file_id).group(1)
                self._add(file_id, category)

        elif self._map is not None:
            for (file_id, categories) in self._map.items():
                for category in categories:
                    self._add(file_id, category)

        elif self._file is not None:
            for line in self.open(self._file).readlines():
                line = line.strip()
                file_id, categories = line.split(self._delimiter, 1)
                # https://github.com/nltk/nltk/issues/250
                #if file_id not in self.fileids():
                #    raise ValueError('In category mapping file %s: %s '
                #                     'not found' % (self._file, file_id))
                for category in categories.split(self._delimiter):
                    self._add(file_id, category)


class CategorizedXMLCorpusReader(MyCategorizedCorpusReader, XMLCorpusReader):
    def __init__(self, *args, **kwargs):
        MyCategorizedCorpusReader.__init__(self, kwargs)
        XMLCorpusReader.__init__(self, *args, **kwargs)

    def _resolve(self, fileids, categories):
        if fileids is not None and categories is not None:
            raise ValueError('Specify fileids or categories, not both')
        if categories is not None:
            return self.fileids(categories)
        else:
            return fileids

    def raw(self, fileids=None, categories=None):
        return XMLCorpusReader.raw(self, self._resolve(fileids, categories))

    def words(self, fileids=None, categories=None):
        words = []
        fileids = self._resolve(fileids, categories)
        for fileid in fileids:
            words += XMLCorpusReader.words(self, fileid)
        return words

    def text(self, fileids=None, categories=None):
        fileids = self._resolve(fileids, categories)
        text = ""
        for fileid in fileids:
            for i in self.xml(fileid).getiterator():
                if i.text:
                    text += i.text
        return text

    def sents(self, fileids=None, categories=None):
        text = self.words(fileids, categories)
        sents = nltk.PunktSentenceTokenizer().tokenize(text)
        return sents

    def paras(self, fileids=None, categories=None):
        return CategorizedCorpusReader.paras(self, self._resolve(fileids, categories))


def stopless(wordslist):
    stop = stopwords.words('latin')
    filtered = [x for x in wordslist if x not in stop]
    return filtered

def punctless(wordslist):
    punct = string.punctuation
    
    punct += u'\u00a7' # SECTION SIGN
    punct += u'\u00b3' # SUPERSCRIPT THREE
    punct += u'\u00b2' # SUPERSCRIPT TWO
    punct += u'\u00b7' # MIDDLE DOT
    punct += u'\u00b9' # SUPERSCRIPT ONE
    punct += u'\u2014' # EM DASH
    punct += u'\u2019' # RIGHT SINGLE QUOTATION MARK
    punct += u'\u2020' # DAGGER
    punct += u'\u2184' # LATIN SMALL LETTER REVERSED C
    punct += u'\u221e' # INFINITY
    punct += u'\u23d1' # METRICAL BREVE

    punctuation = list(punct)

    words = []
    for w in wordslist:
        if w.isalpha():
            words.append(w)

    filtered = [x for x in words if x not in punctuation]
    return filtered
