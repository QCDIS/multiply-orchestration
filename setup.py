#!/usr/bin/env python

from setuptools import setup

requirements = [
]

__version__ = None
with open('multiply_orchestration/version.py') as f:
    exec(f.read())

setup(name='multiply-orchestration',
      version=__version__,
      description='MULTIPLY Orchestration',
      author='Tonio Fincke (Brockmann Consult GmbH)',
      packages=['multiply_orchestration'],
      install_requires=requirements
)
