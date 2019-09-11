import spooner

import pytest


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail",['T', 'R', 'EY1', 'L'])
    ]
)


def test_phonemes(text,expected):
    assert spooner.phonemes(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", [['snail'], ['tracks', 'trax']]),
        ("blushing crow", [['crushing'], ['bleau', 'blow', 'blowe']]),
        ("jelly beans", [['beli', 'belli', 'belly'], ['genes', 'jeanes', 'jeans']]),
        ("hello world", None)
    ]
)


def test_spoon(text,expected):
    assert spooner.spoon(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", ["snail tracks", "snail trax"]),
        ("a blushing crow", ["a crushing blow", "a crushing bleau", "a crushing blowe"]),
    ]
)

def test_samples(text,expected):
    assert spooner.spoonsentence(text) in expected
