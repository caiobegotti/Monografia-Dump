# http://stackoverflow.com/questions/6849600/does-anyone-have-a-categorized-xml-corpus-reader-for-nltk
from CatXMLReader import CategorizedXMLCorpusReader

from nltk.corpus import cicero
from nltk import Text

fileids = cicero.abspaths()
reader = CategorizedXMLCorpusReader('/', fileids, cat_file='cats.txt')
words = Text(reader.words(fileids))
print words.concordance('ut')
