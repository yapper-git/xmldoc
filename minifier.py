#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET
import os
import sys

from Minifier import Minifier

parser = argparse.ArgumentParser(description="Minifies an XML extract.")
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

try:
    tree = ET.parse(args.input)
except OSError as exception:
    print(exception, file=sys.stderr)
    sys.exit(1)
except ET.ParseError as exception:
    print(exception, file=sys.stderr)
    sys.exit(2)

minifier = Minifier(tree)
newtree = minifier.run()
newtree.write(args.output)
