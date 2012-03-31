#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree

refs = []
urls = []

browse = 'http://latin.packhum.org/author/474'
page = etree.parse(browse, etree.HTMLParser(encoding='utf-8'))
matches = page.xpath("//span[@class='wnam']//text()")

num = 1
for entry in matches:
    refs.append(('http://latin.packhum.org/dx/text/474/%s/0' % str(num), entry.lower()))
    num += 1

for r in refs:
    print r[1], r[0]
