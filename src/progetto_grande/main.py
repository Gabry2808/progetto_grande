import arcade

from progetto_grande.constants import MAX_WINDOW_HEIGHT, MAX_WINDOW_WIDTH, WINDOW_TITLE
from progetto_grande.gameview import GameView


def main() -> None:
    window = arcade.Window(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT, WINDOW_TITLE)
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()
