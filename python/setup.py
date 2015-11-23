#!/usr/bin/python
from setuptools import setup
import os

setup(name=os.environ.get('PACKAGENAME', 'ramldoc'),
      version=os.environ.get('PACKAGEVER', '1.0'),
      author="Eric Chazan",
      author_email="eric.chazan@sungardas.com",
      license='Sungard AS Proprietary',
      packages=['ramldoc']
)
