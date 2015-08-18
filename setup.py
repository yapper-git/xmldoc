#!/usr/bin/env python

from distutils.core import setup

setup(
    name='xmldoc',
    version='0.1',
    py_modules=['xmldoc'],
    install_requires=['jinja2', 'lxml'],
)
