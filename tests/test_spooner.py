import spooner

import pytest
from pytest import param

@pytest.mark.parametrize(
    "text","expected",
    [
        param("three cheers for our dear old queen", 
        "['dear', 'queen'] -> [['queer'], ['dean', 'deane', 'deen']]")
        param("I've got hope in my soul",)
        param("you missed my history lecture",)
        param("a blushing crow",)
        param("There’s nothing like a good spoonerism to tickle your funny bone",)
        param("Is the dean busy",)
        param("jelly beans",)
        param("trail snacks",)
        param("call box",)
    ]

def test_samples(text,expected):
    assert expected in spooner.spoonsentence(text)