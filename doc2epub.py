#!/usr/bin/env python

"""
Converts document repository to EPUB2.
"""

from argparse import ArgumentParser

from xmldoc.document import DocumentDir

parser = ArgumentParser(description=__doc__)
parser.add_argument("input", help="path to document repository")
parser.add_argument("output", help="path to EPUB file")
args = parser.parse_args()

document = DocumentDir(args.input)
document.export_epub(args.output)
