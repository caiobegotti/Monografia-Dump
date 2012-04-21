from CatXMLReader import CategorizedXMLCorpusReader

from nltk.corpus import cicero
from nltk import Text

fileids = cicero.abspaths()
cats = cicero.root + '/categories.txt'
reader = CategorizedXMLCorpusReader('/', fileids, cat_file=cats)

words = Text(reader.words(fileids))
print words.concordance('ut')
