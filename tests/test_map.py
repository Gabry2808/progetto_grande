import pytest
from progetto_grande.map import GridCell, MAP_DECOUVERTE, InvalidMapFileException, charger_map

def test_map_requires_player() -> None:
    lines = [
        "width: 5",
        "height: 3",
        "---",
        "xxxxx",
        "x   x",
        "xxxxx",
        "---",
    ]
    # if the map has no player, it should raise an error
    with pytest.raises(InvalidMapFileException):
        charger_map(lines)

def test_map_rejects_two_players() -> None:
    lines = [
        "width: 5",
        "height: 3",
        "---",
        "xxxxx",
        "x P x",
        "x P x",
        "---",
    ]
    with pytest.raises(InvalidMapFileException):
        charger_map(lines)

def test_map_reads_main_symbols() -> None:
    lines = [
        "width: 5",
        "height: 3",
        "---",
        "x*  x",
        "x Ovx",
        "x P x",
        "---",
    ]

    game_map = charger_map(lines)

    assert game_map.get(0, 2) == GridCell.BUSH
    assert game_map.get(1, 2) == GridCell.CRYSTAL
    assert game_map.get(2, 1) == GridCell.HOLE
    assert game_map.player_start_x == 2
    assert game_map.player_start_y == 0
    assert game_map.bats == ((3, 1),)

def test_map_get_returns_correct_cells() -> None:
    assert MAP_DECOUVERTE.get(0, 0) == GridCell.BUSH
    assert MAP_DECOUVERTE.get(39, 14) == GridCell.BUSH
    assert MAP_DECOUVERTE.get(10, 1) == GridCell.CRYSTAL
    assert MAP_DECOUVERTE.get(3, 1) == GridCell.GRASS

def test_map_is_walkable() -> None:
    lines = [
        "width: 5",
        "height: 3",
        "---",
        "x*  x",
        "x Ovx",
        "x P x",
        "---",
    ]
    game_map = charger_map(lines)

    assert game_map.is_walkable((1, 0))  # grass
    assert game_map.is_walkable((2, 0))  # player cell = grass
    assert not game_map.is_walkable((0, 0))  # bush
    assert not game_map.is_walkable((2, 1))  # hole
    assert not game_map.is_walkable((-1, 0))  # hors map
    assert not game_map.is_walkable((5, 0))  # hors map

def test_map_get_invalid_coordinates() -> None:
    with pytest.raises(IndexError):
        MAP_DECOUVERTE.get(-1, 0)

    with pytest.raises(IndexError):
        MAP_DECOUVERTE.get(0, -1)

    with pytest.raises(IndexError):
        MAP_DECOUVERTE.get(40, 0)

    with pytest.raises(IndexError):
        MAP_DECOUVERTE.get(0, 15)
