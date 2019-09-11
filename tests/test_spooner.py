import spooner

import pytest


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", [['snail'], ['tracks', 'trax']]),
        ("blushing crow", [['crushing'], ['bleau', 'blow', 'blowe']]),
        ("jelly beans", [['beli', 'belli', 'belly'], ['genes', 'jeanes', 'jeans']]),
    ]
)


def test_spoon(text,expected):
    assert spooner.spoon(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", ["snail tracks", "snail trax"]),
        ("a blushing crow", ["a crushing blow", "a crushing bleau", "a crushing blowe"]),
        #("three cheers for our dear old queen", ""),
        # ("I've got hope in my soul",""),
        # ("you missed my history lecture",""),
        # ("funny bone",""),
        # ("Is the dean busy",""),
        # ("jelly beans",""),
    ]
)

def test_samples(text,expected):
    assert spooner.spoonsentence(text) in expected
