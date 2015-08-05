#!/usr/bin/env python3

import argparse
from jinja2 import Environment, FileSystemLoader
import os
import xml.etree.ElementTree as ET

import docparser
import latex_renderer

parser = argparse.ArgumentParser(description="Converts XML extract to LaTeX.")
parser.add_argument("input", help="path to input file")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

root = ET.parse(args.input).getroot()

renderer = latex_renderer.LaTeXRenderer()
parser = docparser.DocParser(root, renderer)

main_content = parser.run()

templates_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(templates_folder))
template = env.get_template('latex_render.tex')
template_render = template.render(
    title='Document Title',
    subtitle='Subtitle of the document',
    author_name='Author Name',
    packages=renderer.packages,
    main_content=main_content,
)

with open(args.output, "w") as output_file:
    output_file.write(template_render)
