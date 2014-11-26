#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
from DocParser import *
from XHTMLRenderer import *

root = ET.parse(sys.argv[1]).getroot()
parser = DocParser(root, XHTMLRenderer())

with open(sys.argv[2], 'w') as file:
    file.write(parser.run())
