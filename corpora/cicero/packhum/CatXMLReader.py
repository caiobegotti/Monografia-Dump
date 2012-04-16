import imp                                                                                                                                                                                                                     
CatXMLReader = imp.load_source('CategorizedXMLCorpusReader','PATH_TO_THIS_FILE/CategorizedXMLCorpusReader.py')
	
CatXMLReader = CatXMLReader.CategorizedXMLCorpusReader('.../nltk_data/corpora/nytimes', file_ids, cat_file='PATH_TO_CATEGORIES_FILE')
	
# Categorized XML Corpus Reader                                                                                                                                                                                                  

from nltk.corpus.reader import CategorizedCorpusReader, XMLCorpusReader
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

        # All of the following methods call the corresponding function in ChunkedCorpusReader                                                                                                                                    
        # with the value returned from _resolve(). We'll start with the plain text methods.                                                                                                                                      
    def raw(self, fileids=None, categories=None):
        return XMLCorpusReader.raw(self, self._resolve(fileids, categories))

    def words(self, fileids=None, categories=None):
        #return CategorizedCorpusReader.words(self, self._resolve(fileids, categories))                                                                                                                                          
        # Can I just concat words over each file in a file list?                                                                                                                                                                 
        words=[]
        fileids = self._resolve(fileids, categories)
        # XMLCorpusReader.words works on one file at a time. Concatenate them here.                                                                                                                                              
        for fileid in fileids:
            words+=XMLCorpusReader.words(self, fileid)
        return words

    # This returns a string of the text of the XML docs without any markup                                                                                                                                                       
    def text(self, fileids=None, categories=None):
        fileids = self._resolve(fileids, categories)
        text = ""
        for fileid in fileids:
            for i in self.xml(fileid).getiterator():
                if i.text:
                    text += i.text
        return text

    # This returns all text for a specified xml field                                                                                                                                                                            
    def fieldtext(self, fileids=None, categories=None):
        # NEEDS TO BE WRITTEN                                                                                                                                                                                                    
        return

    def sents(self, fileids=None, categories=None):
        #return CategorizedCorpusReader.sents(self, self._resolve(fileids, categories))                                                                                                                                          
        text = self.words(fileids, categories)
        sents=nltk.PunktSentenceTokenizer().tokenize(text)
        return sents

    def paras(self, fileids=None, categories=None):
        return CategorizedCorpusReader.paras(self, self._resolve(fileids, categories))
