from functions.Khelladi_Faiza_2_Fonctions_1602 import grid_around_best


def test_grid_around_best_basic():
    result = grid_around_best(10, 2)
    assert list(result) == [8, 9, 10, 11, 12]


def test_grid_around_best_none():
    result = grid_around_best(None, 2)
    assert result == [None]  