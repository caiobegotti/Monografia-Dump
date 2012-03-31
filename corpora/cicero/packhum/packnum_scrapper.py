#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
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
   
    filename = title.replace(' ', '_') + '.xml'
    w = XMLWriter(filename, encoding='utf-8')
    xml = w.start("text")
    
    w.element("author", 'marcus tullius cicero')
    w.element("title", title) 
    w.element("source", base) 
    
    for x in range(0, 500):
        lines = []
        section = source + str(x)
        reference = base + 'loc/474/' + str(x) + '/0'
        try:
            page = etree.parse(section, etree.HTMLParser(encoding='utf-8'))
        except Exception, err:
            print 'Text Error: ' + str(err)
        try:
            matches = page.xpath("//tr/td[1]//text()")
        except Exception, err:
            print 'Match Error: ' + str(err)
        empty = u'\xa0\xa0'
        for m in matches:
            if m.startswith(empty):
                lines.append(''.join(m.replace(empty,'')))
            else:
                lines.append(''.join(m))
        paragraph = ' '.join(lines)
        w.element("paragraph", paragraph)
        if len(matches) == 0:
            break
        time.sleep(5)
    w.close(xml)
