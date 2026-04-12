import arcade

from progetto_grande.gameview import GameView
from progetto_grande.map import MAP_DECOUVERTE
from progetto_grande.player import Direction


def test_player_keeps_last_direction_when_stopped(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    view.on_key_press(arcade.key.RIGHT, 0)
    view.on_update(1 / 60)
    assert view.player.direction == Direction.EAST

    view.on_key_release(arcade.key.RIGHT, 0)
    view.on_update(1 / 60)
    assert view.player.direction == Direction.EAST

def test_last_pressed_vertical_key(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    view.on_key_press(arcade.key.UP, 0)
    view.on_update(1 / 60)
    assert view.player.change_y > 0

    view.on_key_press(arcade.key.DOWN, 0)
    view.on_update(1 / 60)
    assert view.player.change_y < 0

def test_player_direction_in_diagonal(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    view.on_key_press(arcade.key.RIGHT, 0)
    view.on_key_press(arcade.key.UP, 0)
    view.on_update(1 / 60)

    assert view.player.direction == Direction.NORTH
