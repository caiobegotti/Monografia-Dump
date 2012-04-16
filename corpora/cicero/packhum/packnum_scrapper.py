#!/usr/bin/env python
# -*- coding: utf-8 -*-
# caio begotti <caio1982@gmail.com>
# this is under public domain

# to add some sleep time between fetches
# and not hammer down the server
import time

# to avoid charsetting mess with UTF-8 strings
import codecs
import string

# to check if a text was already fetched
from os.path import exists

# document parser
from lxml import etree

# output generation
from elementtree.SimpleXMLWriter import XMLWriter

refs = []
urls = []

# the root directory of all latin texts in PHI
base = 'http://latin.packhum.org/'

# marcus tullius cicero entry in PHI
browse = base + 'author/474'

try:
    page = etree.parse(browse, etree.HTMLParser(encoding='utf-8'))
except Exception, err:
    print 'Browse Error: ' + str(err)

# gets the list of texts by cicero currently in PHI
matches = page.xpath("//span[@class='wnam']//text()")

counter = 1
for entry in matches:
    # creates a reference list with download addresses for every text
    refs.append((base + 'dx/text/474/%s/' % str(counter), entry.lower()))
    counter += 1

for param in refs:
    source = param[0]
    title = param[1]
  
    # debug 
    print '[%s]' % title
   
    filename = title.replace(' ', '_')
    for p in string.punctuation.replace('_',''):
        filename = filename.replace(p, '')

    w = XMLWriter('cicero_' + filename + '.xml', encoding='utf-8')
    xml = w.start("document")
 
    # metadata entries of the output files   
    w.element("author", 'marcus tullius cicero')
    w.element("title", title) 
    w.element("source", base) 
    
    # upon checking it no text in PHI attributed to cicero
    # has more than 500 pages, so this is a safe download limit
    for x in range(0, 500):
        lines = []
        entry = []
        section = source + str(x)
        reference = base + 'loc/474/' + str(x) + '/0'
        
        # debug
        print '\t<%s>' % section

        # output filename
        path = 'ready/' + filename + '-' + str(x) + '.txt'

        if not exists(path):
            # fetches the current page
            try:
                page = etree.parse(section, etree.HTMLParser(encoding='utf-8'))
            except Exception, err:
                print 'Text Error: ' + str(err)

            # parses the page paragraphs
            try:
                entry = page.xpath("//tr/td[1]//text() | //h3//text()")
            except Exception, err:
                print 'Match Error: ' + str(err)
                # a priori this is not needed but it is helpful for debugging
                f = codecs.open("log.txt", "a", "utf8")
                f.write('\nMatch Error: ' + str(err) + ' [missing] ' + section)
                f.close()

            # checks if the end of text has been reached
            if 'No text' in entry:
                print 'EOF: ' + str(x)
                break
            
            empty = u'\xa0\xa0'
            if len(entry) > 0:
                for e in entry:
                    if e.startswith(empty):
                        # apparently PHI texts have double blank spaces indicating new paragraphs
                        lines.append(''.join(e.replace(empty,'')))
                    else:
                        lines.append(''.join(e))

                paragraph = ' '.join(lines)
                y = codecs.open(path, "w", "utf8")
                y.write(paragraph)
                y.write
        else:
            # if text has been fetched ok, process it
            paragraph = codecs.open(path, "r", "utf8")
            strings = paragraph.read()

            # finally writes the new content to the corpus file
            w.start("page", id=str(x))
            w.element("paragraph", strings)
            w.end("page")

        # give the PHI server some time until the next fetch
        # time.sleep(5)
    # generates the output file
    w.close(xml)
