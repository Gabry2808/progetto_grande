import arcade

from progetto_grande.gameview import GameView
from progetto_grande.map import MAP_DECOUVERTE

def test_map_contains_bats() -> None:
    assert len(MAP_DECOUVERTE.bats) > 0

def test_bat_stays_in_its_range(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    bat = view.bat_list[0]

    for _ in range(200):
        bat.update_bat()

    dx = bat.center_x - bat.start_x
    dy = bat.center_y - bat.start_y
    distance = (dx ** 2 + dy ** 2) ** 0.5

    assert distance <= bat.range * 1.2


def test_player_loses_when_touching_bat(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    bat = view.bat_list[0]
    view.player.center_x = bat.center_x
    view.player.center_y = bat.center_y

    old_view = view
    view.on_update(1 / 60)

    assert window.current_view is not old_view

def test_sword_removes_bat(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    initial_count = len(view.bat_list)
    bat = view.bat_list[0]

    view.player.center_x = bat.center_x
    view.player.center_y = bat.center_y

    view.sword.use(view.player)
    view.on_update(1 / 60)

    assert len(view.bat_list) == initial_count - 1
