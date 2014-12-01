#!/usr/bin/env python3

import argparse
from lxml import etree
import os
import sys

XML_SCHEMA = "extract.xsd"

parser = argparse.ArgumentParser(
    description="Validates XML extract against XML Schema Definition (XSD).")
parser.add_argument("file", help="path to XML file")
args = parser.parse_args()

absolute_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    XML_SCHEMA)
xsd_doc = etree.parse(absolute_path)
xmlschema = etree.XMLSchema(xsd_doc)

try:
    xml_doc = etree.parse(args.file)
    xmlschema.assertValid(xml_doc)
except Exception as exception:
    print(exception, file=sys.stderr)
    sys.exit(1)

print("validates")

