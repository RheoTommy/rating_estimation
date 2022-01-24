from src.lib.problems import is_during_contest, get_difficulty


def test_is_during_contest():
    queries = [
        ("abc221", 1633181189),
        ("abc221", 1633184965),
        ("abc218", 1631367447),
        ("abc218", 1631515804),
    ]
    expect = [True, False, True, False]
    assert is_during_contest(queries) == expect


def test_get_difficulty():
    queries = [
        "abc221_a",
        "abc221_b",
        "abc221_c",
        "abc221_d",
        "abc221_e",
        "abc221_f",
        "abc221_g",
        "abc221_h",
    ]
    expect = [-1081, -371, 378, 832, 1515, 2093, 2914, 2793]
    assert get_difficulty(queries) == expect
