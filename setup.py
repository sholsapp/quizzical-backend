#!/usr/bin/env python

import os

from setuptools import setup

README = None
with open(os.path.abspath('README.md')) as fh:
  README = fh.read()

setup(
  name='quizzical',
  version='1.0',
  description=README,
  author='Stephen Holsapple',
  author_email='sholsapp@gmail.com',
  url='http://www.flask.com',
  packages=['quizzical'],
)
