#!/usr/bin/env python

"""
Converts document repository to EPUB2.
"""

from argparse import ArgumentParser

from epub2 import EpubBuilder, EpubNavPoint

from document import Document
from epub_renderer import EpubRenderer

parser = ArgumentParser(description=__doc__)
parser.add_argument("input", help="path to input file")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

document = Document(args.input)
renderer = EpubRenderer(document)

renderer.run(args.output)
