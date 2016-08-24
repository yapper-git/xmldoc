#!/usr/bin/env python

from distutils.core import setup

setup(
    name='xmldoc',
    version='0.2',
    py_modules=['xmldoc'],
    install_requires=['jinja2', 'lxml'],
    description='Tools to manage own XML format for documents',
    url='https://github.com/yapper-git/xmldoc',
)
