from . import sp

import pytest


@pytest.mark.parametrize("text, expected", [("trail", ["T", "R", "EY1", "L"])])
def test_phonemes(text, expected):
    assert sp.phonemes(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", [["snail"], ["tracks", "trax"]]),
        ("blushing crow", [["crushing"], ["bleau", "blow", "blowe"]]),
        ("jelly beans", [["beli", "belli", "belly"], ["genes", "jeanes", "jeans"]]),
        ("hello world", None),
        ("run for", [["fun"], ["roar", "roehr", "rohr"]]),
        ("loving shepherd", [["shoving"], ["leopard", "lepard", "leppard"]]),
    ],
)
def test_spoon(text, expected):
    assert sp.spoon(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", ["snail tracks", "snail trax"]),
        (
            "a blushing crow",
            ["a crushing blow", "a crushing bleau", "a crushing blowe"],
        ),
        ("this program is the best", ""),
        (
            "run for the hills",
            [
                "fun roar the hills",
                "fun roehr the hills",
                "fun rohr the hills",
                "run whore the fills",
                "run hoare the fills",
                "run hoar the fills",
                "run hoerr the fills",
                "run horr the fills",
            ],
        ),
    ],
)
def test_samples(text, expected):
    assert sp.spoonsentence(text) in expected
