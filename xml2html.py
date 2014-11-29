#!/usr/bin/env python3

import argparse
import os
import sys
import xml.etree.ElementTree as ET

from DocParser import *
from XHTMLRenderer import *

def error(message):
    print("ERROR:", message, file=sys.stderr)

parser = argparse.ArgumentParser(descrption="Converts XML extract to XHTML.")
parser.add_argument("-f", "--force", help="force output overwrite", action="store_true")
parser.add_argument("input", help="path to input file")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

# Check input file existance
if not os.path.isfile(args.input):
    error("{} does not exist".format(args.input))
    sys.exit(1)

# Check output file existance (do not overwrite by default)
if not args.force and os.path.isfile(args.output):
    error("{} already exists, use -f to force overwrite".format(args.output))
    sys.exit(2)

root = ET.parse(args.input).getroot()
parser = DocParser(root, XHTMLRenderer())

with open(args.output, "w") as file:
    file.write(parser.run())
