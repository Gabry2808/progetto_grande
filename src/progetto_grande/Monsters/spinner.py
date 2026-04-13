from typing import Callable
import arcade

from progetto_grande.Monsters.monster import Monster
from progetto_grande.map import SpinnerMove
from progetto_grande.textures import ANIMATION_SPINNER
from progetto_grande.constants import SCALE


class Spinner(Monster):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        min_limit: int,
        max_limit: int,
        spinner_move: SpinnerMove,
    ) -> None:
        super().__init__(
            animation=ANIMATION_SPINNER,
            scale=SCALE,
            center_x=center_x,
            center_y=center_y,
        )
        self.move = 1
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.spinner_move = spinner_move

    def update_spinner(self, grid_to_pixels: Callable[[int], int]) -> None:
        if self.spinner_move == SpinnerMove.HORIZONTAL:
            self.center_x += 3 * self.move
            left_px = grid_to_pixels(self.min_limit)
            right_px = grid_to_pixels(self.max_limit)

            if self.center_x >= right_px:
                self.center_x = right_px
                self.move = -1
            elif self.center_x <= left_px:
                self.center_x = left_px
                self.move = 1
        else:
            self.center_y += 3 * self.move

            bottom_px = grid_to_pixels(self.min_limit)
            top_px = grid_to_pixels(self.max_limit)

            if self.center_y >= top_px:
                self.center_y = top_px
                self.move = -1
            elif self.center_y <= bottom_px:
                self.center_y = bottom_px
                self.move = 1
