#!/usr/bin/env python

import argparse
from lxml import etree
import os
import sys

XML_SCHEMA = "extract.xsd"

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", "-v", help="FIXME", action="store_true")
parser.add_argument("file", help="path to XML file")
args = parser.parse_args()

xsd_doc = etree.parse(XML_SCHEMA)

try:
    xml_doc = etree.parse(args.file)
    xmlschema = etree.XMLSchema(xsd_doc)
    xmlschema.assertValid(xml_doc)
except OSError as exception:
    print(exception)
    sys.exit(1)
except etree.XMLSyntaxError as exception:
    print(exception)
    sys.exit(2)
except etree.DocumentInvalid as exception:
    print(exception)
    sys.exit(3)

print("validates")
sys.exit(0)
