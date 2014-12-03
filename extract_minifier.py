#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET
import os
import sys

import minifier

parser = argparse.ArgumentParser(description="Minifies an XML extract.")
parser.add_argument("-f", "--force", action="store_true",
                    help="force output overwrite")
parser.add_argument("input", help="path to input file")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

try:
    if not args.force and os.path.isfile(args.output):
        raise FileExistsError("{} already exists, use -f to force overwrite"
                              .format(args.output))

    tree = ET.parse(args.input)

    minifier.Minifier.run(tree)
    tree.write(args.output)
except OSError as exception:
    print(exception, file=sys.stderr)
    sys.exit(1)

