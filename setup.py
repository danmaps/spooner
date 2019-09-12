#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.5.2'

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'nltk==3.4.5'
    'pronouncing==0.2.0'
]

setup(
    name='spooner',
    author="Danny McVey",
    version=version,
    install_requires=['nltk', 'pronouncing'],
)
