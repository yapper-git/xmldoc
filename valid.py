#!/usr/bin/env python

import sys
from lxml import etree

xmlschema_doc = etree.parse("extract.xsd")

xml_filename = sys.argv[1]

try:
    xml_doc = etree.parse(xml_filename)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xmlschema.assertValid(xml_doc)
    print("validates")
except etree.XMLSyntaxError as e:
    # XML not well formed
    print(e)
    sys.exit(1)
except etree.DocumentInvalid as e:
    # No not conform XML Schema Definition
    print(e)
    sys.exit(2)
