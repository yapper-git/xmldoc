#!/usr/bin/env python

import sys
from lxml import etree

xml_filename = sys.argv[1]

try:
    xml_doc = etree.parse(xml_filename)
except:
    print("not well formed")
    sys.exit()

xmlschema_doc = etree.parse("extract.xsd")
xmlschema = etree.XMLSchema(xmlschema_doc)

if xmlschema.validate(xml_doc):
    print("success")
else:
    print("failed")

try:
    xmlschema.assertValid(xml_doc)
except etree.DocumentInvalid as e:
    print(e)
