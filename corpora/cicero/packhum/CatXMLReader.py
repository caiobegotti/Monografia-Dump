# http://stackoverflow.com/questions/6849600/does-anyone-have-a-categorized-xml-corpus-reader-for-nltk

from nltk.corpus.reader import CategorizedCorpusReader
from nltk.corpus.reader import XMLCorpusReader

class CategorizedXMLCorpusReader(CategorizedCorpusReader, XMLCorpusReader):
    def __init__(self, *args, **kwargs):
        CategorizedCorpusReader.__init__(self, kwargs)
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
        words=[]
        fileids = self._resolve(fileids, categories)
        for fileid in fileids:
            words+=XMLCorpusReader.words(self, fileid)
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
        sents=nltk.PunktSentenceTokenizer().tokenize(text)
        return sents

    def paras(self, fileids=None, categories=None):
        return CategorizedCorpusReader.paras(self, self._resolve(fileids, categories))
