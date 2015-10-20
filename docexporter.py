#!/usr/bin/env python

"""
Converts document repository to another format (EPUB2/HTML/LaTeX).
"""

from argparse import ArgumentParser

from xmldoc.document import DocumentDir

parser = ArgumentParser(description=__doc__)
parser.add_argument("-f", "--format", help="export format", default='epub', choices=['epub', 'html', 'latex'])
parser.add_argument("input", help="path to document repository")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

document = DocumentDir(args.input)

if args.format == 'epub':
    document.export_epub(args.output)
elif args.format == 'html':
    with open(args.output, "w") as output_file:
        output_file.write(document.export_html())
elif args.format == 'latex':
    with open(args.output, "w") as output_file:
        output_file.write(document.export_latex())
