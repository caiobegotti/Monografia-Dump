#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import codecs
from lxml import etree
from elementtree.SimpleXMLWriter import XMLWriter

refs = []
urls = []

base = 'http://latin.packhum.org/'
browse = base + 'author/474'
try:
    page = etree.parse(browse, etree.HTMLParser(encoding='utf-8'))
except Exception, err:
    print 'Browse Error: ' + str(err)

matches = page.xpath("//span[@class='wnam']//text()")

num = 1
for entry in matches:
    refs.append((base + 'dx/text/474/%s/' % str(num), entry.lower()))
    num += 1

for param in refs:
    source = param[0]
    title = param[1]
   
    print 'processando-------------------- ' + title
   
    filename = title.replace(' ', '_')
    w = XMLWriter(filename + '.xml', encoding='utf-8')
    xml = w.start("document")
    
    w.element("author", 'marcus tullius cicero')
    w.element("title", title) 
    w.element("source", base) 
    
    for x in range(0, 500):
        lines = []
        section = source + str(x)
        reference = base + 'loc/474/' + str(x) + '/0'

        print '     lendo pagina-------------- ' + section

        try:
            page = etree.parse(section, etree.HTMLParser(encoding='utf-8'))
        except Exception, err:
            print 'Text Error: ' + str(err)
        try:
            entry = page.xpath("//tr/td[1]//text()")
        except Exception, err:
            print 'Match Error: ' + str(err)
            f = codecs.open("file.txt", "a", "utf8")
            f.write('\nMatch Error: ' + str(err) + ' [missing] ' + section)
            f.close()
            break
        empty = u'\xa0\xa0'
        if len(entry) > 0:
            for e in entry:
                if e.startswith(empty):
                    lines.append(''.join(e.replace(empty,'')))
                else:
                    lines.append(''.join(e))
        paragraph = ' '.join(lines)
        w.start("page", id=str(x))
        w.element("paragraph")
        path = 'ready/' + filename + '-' + str(x) + '.txt'
        y = codecs.open(path, "w", "utf8")
        y.write(paragraph)
        y.write
        w.end("page")
        if len(entry) == 0:
            print 'EOF: ' + str(x)
            break
        time.sleep(5)
    w.close(xml)
