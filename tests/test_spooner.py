from . import sp
import pytest
# import notify


@pytest.mark.parametrize("text, expected", [("trail", ["T", "R", "EY1", "L"])])
def test_phonemes(text, expected):
    assert sp.phonemes(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", {"trail": ["snail"], "snacks": ["tracks", "trax"]}),
        (
            "crushing blow",
            {
                "blow": ["cro", "crow", "crowe", "krogh", "kroh", "krowe"],
                "crushing": ["blushing"],
            },
        ),
        (
            "jelly beans",
            {
                "jelly": ["beli", "belli", "belly"],
                "beans": ["genes", "jeanes", "jeans"],
            },
        ),
        ("hello world", None),
        ("run for", {"run": ["fun"], "for": ["roar", "roehr", "rohr"]}),
        (
            "loving shepherd",
            {"loving": ["shoving"], "shepherd": ["leopard", "lepard", "leppard"]},
        ),
        ("dental reception", {"dental": ["rental"], "reception": ["deception"]}),
    ],
)
def test_spoon(text, expected):
    assert sp.spoon(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("trail snacks", ["snail tracks", "snail trax"]),
        (
            "a crushing blow",
            [
                "a blushing cro",
                "a blushing crow",
                "a blushing crowe",
                "a blushing krogh",
                "a blushing kroh",
                "a blushing krowe",
            ],
        ),
        ("this program is the best", []),
        (
            "run for the hills",
            [
                "fun roar the hills",
                "fun roehr the hills",
                "fun rohr the hills",
                "run hoar the fills",
                "run hoare the fills",
                "run hoerr the fills",
                "run horr the fills",
                "run whore the fills",
            ],
        ),
    ],
)
def test_sentence(text, expected):
    assert sp.sentence(text) == expected
    # notify.iphone(text, str(expected))
