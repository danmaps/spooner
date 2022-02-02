[![Documentation Status](https://readthedocs.org/projects/spooner/badge/?version=latest)](https://spooner.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/spooner.svg)](https://pypi.org/project/spooner/)
[![codecov](https://codecov.io/gh/danmaps/spooner/branch/master/graph/badge.svg)](https://codecov.io/gh/danmaps/spooner)
[![Build Status](https://dev.azure.com/danmaps/spooner/_apis/build/status/danmaps.spooner?branchName=master)](https://dev.azure.com/danmaps/spooner/_build/latest?definitionId=1&branchName=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) 

# spooner

Generates [spoonerisms](https://en.wikipedia.org/wiki/Spoonerism) based on sounds in words. Created just for fun and learning.

| STANDARD DISCLAIMER: Spoonerisms made by this program are not guaranteed to be funny, but they *are* technically spoonerisms. |
| --- | 


Inspired by [this create podcase episode](https://testandcode.com/80), I created this to learn about packaging, flit, tox, pytest, and coverage. It went surprisingly well, so now I have a thing that lives on the internet. Anyone can install and play with it! Neat!


## Installation

~~~
pip install spooner
~~~


## Usage

Use it like this:
~~~
>>> import spooner as sp
>>> sp.phonemes("trail")
['T', 'R', 'EY1', 'L']
~~~
~~~
>>> sp.spoon("trail snacks")
{'trail': ['snail'], 'snacks': ['tracks', 'trax']}
~~~
~~~
>>> sp.sentence("let's eat trail snacks")
["let's treat ail snacks", "let's treat ale snacks", "let's eat snail tracks", "let's eat snail trax"]
~~~

