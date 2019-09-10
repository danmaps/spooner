import spooner

import pytest
#from pytest import param

@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", ["snail tracks", "snail trax"]),
        #("three cheers for our dear old queen", ""),
        # ("I've got hope in my soul",""),
        # ("you missed my history lecture",""),
        ("a blushing crow", ["a crushing blow", "a crushing bleau", "a crushing blowe"]),
        # ("There’s nothing like a good spoonerism to tickle your funny bone",""),
        # ("Is the dean busy",""),
        # ("jelly beans",""),
    ]
)

def test_samples(text,expected):
    assert spooner.spoonsentence(text) in expected
