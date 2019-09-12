#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.5.6'

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'nltk==3.4.5',
    'pronouncing==0.2.0'
]

setup(
    name='spooner',
    packages=find_packages(exclude=['docs', 'tests']),
    author="Danny McVey",
    version=version,
    #long_description=readme(),
    description='Spoonerisms on demand',
    install_requires=requirements,
)
