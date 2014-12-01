#!/usr/bin/env python3

import argparse
import os
import sys
import xml.etree.ElementTree as ET

from DocParser import *
from MarkdownRenderer import *

parser = argparse.ArgumentParser(description="Converts XML extract to XHTML.")
parser.add_argument("-f", "--force", help="force output overwrite", action="store_true")
parser.add_argument("input", help="path to input file")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

try:
    if not args.force and os.path.isfile(args.output):
        raise FileExistsError("{} already exists, use -f to force overwrite".format(args.output))

    root = ET.parse(args.input).getroot()

    parser = DocParser(root, MarkdownRenderer())

    with open(args.output, "w") as file:
        file.write(parser.run())
except Exception as exception:
    print(exception, file=sys.stderr)
    sys.exit(1)

