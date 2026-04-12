import arcade
from progetto_grande.gameview import GameView
from progetto_grande.map import MAP_DECOUVERTE

def test_collect_crystals(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    initial_crystal_count = len(view.crystals)
    assert initial_crystal_count == 12

    crystal = view.crystals[0]
    view.player.center_x = crystal.center_x
    view.player.center_y = crystal.center_y

    view.on_update(1 / 60)


    assert len(view.crystals) == initial_crystal_count - 1
