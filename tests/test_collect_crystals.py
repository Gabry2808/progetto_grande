import arcade
from progetto_grande.gameview import GameView
from progetto_grande.map import MAP_DECOUVERTE

def test_collect_crystals(window: arcade.Window) -> None:
    view = GameView(MAP_DECOUVERTE)
    window.show_view(view)

    INITIAL_CRYSTAL_COUNT = 12
    assert len(view.crystals) == INITIAL_CRYSTAL_COUNT

    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)

    # Let the game run for 1 second (60 frames)
    window.test(60)

    # We should have collected the first crystal
    assert len(view.crystals) == INITIAL_CRYSTAL_COUNT - 1
