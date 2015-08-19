#!/usr/bin/env python

"""
Validates document repository (manifest.json and text.xml)
"""

from argparse import ArgumentParser

from xmldoc.validator import Validator

parser = ArgumentParser(description=__doc__)
parser.add_argument("input", help="path to document repository")
args = parser.parse_args()

validator = Validator(args.input)
validator.run()
