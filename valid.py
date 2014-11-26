#!/usr/bin/env python

import sys
from lxml import etree

xml_filename = sys.argv[1]
xml_doc = etree.parse(xml_filename)

xmlschema_doc = etree.parse("extract.xsd")
xmlschema = etree.XMLSchema(xmlschema_doc)

print(repr(xmlschema.validate(xml_doc)))

try:
    xmlschema.assertValid(xml_doc)
except etree.DocumentInvalid as e:
    print(repr(e))
