#!/usr/bin/env python3

import argparse
from jinja2 import Environment, FileSystemLoader
import os
import sys
import xml.etree.ElementTree as ET

import docparser
import xhtml_renderer

DEFAULT_LANG = "en"
DEFAULT_TITLE = "Untitled extract"

parser = argparse.ArgumentParser(description="Converts XML extract to XHTML.")
parser.add_argument("-f", "--force", action="store_true",
                    help="force output overwrite")
parser.add_argument("-l", "--lang",
                    help="extract language ('{}' by default)"
                         .format(DEFAULT_LANG))
parser.add_argument("-t", "--title",
                    help="extract title ('{}' by default)"
                          .format(DEFAULT_TITLE))
parser.add_argument("input", help="path to input file")
parser.add_argument("output", help="path to output file")
args = parser.parse_args()

lang = args.lang if args.lang else DEFAULT_LANG
title = args.title if args.title else DEFAULT_TITLE

if not args.force and os.path.isfile(args.output):
    raise FileExistsError("{} already exists, use -f to force overwrite"
                          .format(args.output))

root = ET.parse(args.input).getroot()

renderer = xhtml_renderer.XHTMLRenderer()
parser = docparser.DocParser(root, renderer)

templates_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')
env = Environment(loader=FileSystemLoader(templates_folder))
template = env.get_template('xhtml_render.html')
template_render = template.render(
    xmlns="http://www.w3.org/1999/xhtml",
    dtd_name="-//W3C//DTD XHTML 1.0 Strict//EN",
    dtd_location="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd",
    lang=lang,
    title=title,
    content=parser.run(),
)

with open(args.output, "w") as file:
    file.write(template_render)
