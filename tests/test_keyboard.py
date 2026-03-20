import arcade

from progetto_grande.gameview import GameView
from progetto_grande.map import MAP_DECOUVERTE
from progetto_grande.constants import PLAYER_MOVEMENT_SPEED


def test_last_pressed_horizontal_key(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    view.on_key_press(arcade.key.RIGHT, 0)
    view.on_update(1 / 60)
    assert view.player.change_x == PLAYER_MOVEMENT_SPEED

    view.on_key_press(arcade.key.LEFT, 0)
    view.on_update(1 / 60)
    assert view.player.change_x == -PLAYER_MOVEMENT_SPEED

    view.on_key_release(arcade.key.RIGHT, 0)
    view.on_update(1 / 60)
    assert view.player.change_x == -PLAYER_MOVEMENT_SPEED

    view.on_key_release(arcade.key.LEFT, 0)
    view.on_update(1 / 60)
    assert view.player.change_x == 0
