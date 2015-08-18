#!/usr/bin/env python

"""
Converts document repository to LaTeX.
"""

from argparse import ArgumentParser

from xmldoc.document import Document
from xmldoc.latex_renderer import LaTeXRenderer

parser = ArgumentParser(description=__doc__)
parser.add_argument("input", help="path to document repository")
parser.add_argument("output", help="path to epub2 file", nargs="?")
args = parser.parse_args()

document = Document(args.input)
renderer = LaTeXRenderer(document)
latex_content = renderer.run()

if args.output:
    with open(args.output, "w") as output_file:
        output_file.write(latex_content)
else:
    print(latex_content)
