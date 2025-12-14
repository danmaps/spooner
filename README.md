[![Documentation Status](https://readthedocs.org/projects/spooner/badge/?version=latest)](https://spooner.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/spooner.svg)](https://pypi.org/project/spooner/)
[![codecov](https://codecov.io/gh/danmaps/spooner/branch/master/graph/badge.svg)](https://codecov.io/gh/danmaps/spooner)
[![Build Status](https://dev.azure.com/danmaps/spooner/_apis/build/status/danmaps.spooner?branchName=master)](https://dev.azure.com/danmaps/spooner/_build/latest?definitionId=1&branchName=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) 

# spooner

Generates [spoonerisms](https://en.wikipedia.org/wiki/Spoonerism) by swapping phonemes instead of just letters. The package ships a small Flask playground so you can watch the sound swap happen in the browser.

| STANDARD DISCLAIMER: Spoonerisms made by this program are not guaranteed to be funny, but they *are* technically spoonerisms. |
| --- | 


Inspired by [a great podcast episode](https://testandcode.com/80), I created this to learn about packaging, flit, tox, pytest, and coverage. I also threw in a few learning experiences related to  Azure pipelines and black. It went surprisingly well, so now I have a thing that lives on the internet. Anyone can install and play with it! Neat!

Under the hood, Spooner leans on the [CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) via the `pronouncing` library. Each word is broken into its ARPAbet phonemes, the leading consonant clusters are swapped, and only outputs that exist in the dictionary are returned. That means the results are real words instead of random letter jumbles. When a word is missing from the dictionary, you’ll get a friendly error so you can try something more common.


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

`spoon_details` is handy when you want to show *how* a spoonerism was built:

~~~
>>> sp.spoon_details("trail snacks")
{'original_words': ['trail', 'snacks'], 'phonemes': [['T', 'R', 'EY1', 'L'], ['S', 'N', 'AE1', 'K', 'S']], 'swapped_phonemes': [['S', 'N', 'EY1', 'L'], ['T', 'R', 'AE1', 'K', 'S']], 'spoonerisms': {'trail': ['snail'], 'snacks': ['tracks', 'trax']}, 'sample_result': ['snail', 'tracks']}
~~~

### Experimental web front end

There is a tiny Flask app (`spooner.webapp`) that powers a static front end in `templates/` and `static/`. Start it locally to type in two words, animate the phoneme swap, and view the raw phoneme breakdown. It’s intentionally minimal—there’s no persistence or user accounts—but it demonstrates how the API response can drive UI animations.

~~~
FLASK_APP=spooner.webapp flask run
~~~

