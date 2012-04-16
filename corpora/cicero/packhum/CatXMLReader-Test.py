# local CatXMLReader.py file with its class
# http://stackoverflow.com/questions/6849600/does-anyone-have-a-categorized-xml-corpus-reader-for-nltk
from CatXMLReader import CategorizedXMLCorpusReader

# standard NLTK text class
from nltk import Text

reader = CategorizedXMLCorpusReader(cicero)
#'.../nltk_data/corpora/nytimes', file_ids, cat_file='PATH_TO_CATEGORIES_FILE')
