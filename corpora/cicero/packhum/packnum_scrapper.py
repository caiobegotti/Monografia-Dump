#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from lxml import etree

refs = []
urls = []

browse = 'http://latin.packhum.org/author/474'
page = etree.parse(browse, etree.HTMLParser(encoding='utf-8'))
#matches = page.xpath("//span[@class='wnam']//text()")

matches = ['pro quinctio oratio']

num = 1
for entry in matches:
    refs.append(('http://latin.packhum.org/dx/text/474/%s/' % str(num), entry.lower()))
    #num += 1

for param in refs:
    print 'processando: ' + param[1]
    for x in range(0, 500):
        section = param[0] + str(x)
        page = etree.parse(section, etree.HTMLParser(encoding='utf-8'))
        matches = page.xpath("//tr/td[1]//text()")
        print ' '.join(matches)
        if len(matches) == 0:
            break
        time.sleep(5)
