#!/usr/bin/env python

from setuptools import setup

requirements = [
    'multiply_data_access',
    'multiply_prior_engine',
    'multiply_core',
    'pyyaml',
    'shapely'
]

setup(name='multiply-orchestration',
      version='0.1.dev1',
      description='MULTIPLY Orchestration',
      author='Tonio Fincke (Brockmann Consult GmbH)',
      packages=['multiply_orchestration'],
      # entry_points={
      #     'console_scripts': [
      #         'example = cli_example.cli_example:main'
      #     ]
      # }
      install_requires=requirements
)