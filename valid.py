#!/usr/bin/env python3

import argparse
from lxml import etree
import os
import sys

XML_SCHEMA = "extract.xsd"

parser = argparse.ArgumentParser(description="Validates XML extract against XML Schema Definition (XSD).")
parser.add_argument("file", help="path to XML file")
args = parser.parse_args()

xsd_doc = etree.parse(XML_SCHEMA)
xmlschema = etree.XMLSchema(xsd_doc)

try:
    xml_doc = etree.parse(args.file)
    xmlschema.assertValid(xml_doc)
except OSError as exception:
    print(exception, file=sys.stderr)
    sys.exit(1)
except etree.XMLSyntaxError as exception:
    print(exception, file=sys.stderr)
    sys.exit(2)
except etree.DocumentInvalid as exception:
    print(exception, file=sys.stderr)
    sys.exit(3)

print("validates")
