import pytest

from progetto_grande.map import GridCell, MAP_DECOUVERTE


def test_map_get_returns_correct_cells() -> None:
    assert MAP_DECOUVERTE.get(0, 0) == GridCell.BUSH
    assert MAP_DECOUVERTE.get(39, 19) == GridCell.BUSH
    assert MAP_DECOUVERTE.get(5, 2) == GridCell.CRYSTAL
    assert MAP_DECOUVERTE.get(6, 5) == GridCell.CRYSTAL
    assert MAP_DECOUVERTE.get(2, 2) == GridCell.GRASS


def test_map_get_invalid_coordinates() -> None:
    with pytest.raises(IndexError):
        MAP_DECOUVERTE.get(-1, 0)

    with pytest.raises(IndexError):
        MAP_DECOUVERTE.get(0, -1)

    with pytest.raises(IndexError):
        MAP_DECOUVERTE.get(40, 0)

    with pytest.raises(IndexError):
        MAP_DECOUVERTE.get(0, 20)
