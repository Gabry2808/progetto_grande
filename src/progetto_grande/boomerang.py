from enum import Enum

import arcade

from progetto_grande.constants import TILE_SIZE
from progetto_grande.player import Direction


class BoomerangState(Enum):
    INACTIVE = 1
    LAUNCHING = 2
    RETURNING = 3


class Boomerang(arcade.TextureAnimationSprite):

    def __init__(self, animation, scale: float) -> None:
        super().__init__(
            animation=animation,
            scale=scale,
            center_x=0,
            center_y=0,
        )

        self.state = BoomerangState.INACTIVE
        self.direction = Direction.SOUTH
        self.start_x = 0
        self.start_y = 0
        self.visible = False

    def launch(self, player_x: float, player_y: float, direction: Direction) -> None:
        if self.state != BoomerangState.INACTIVE:
            return

        self.center_x = player_x
        self.center_y = player_y
        self.start_x = player_x
        self.start_y = player_y
        self.direction = direction
        self.state = BoomerangState.LAUNCHING
        self.visible = True

    def update_launching(self) -> None:
        if self.direction == Direction.NORTH:
            self.center_y += 8
        elif self.direction == Direction.SOUTH:
            self.center_y -= 8
        elif self.direction == Direction.EAST:
            self.center_x += 8
        elif self.direction == Direction.WEST:
            self.center_x -= 8

    def too_far(self) -> bool:
        distance = ((self.center_x - self.start_x) ** 2 + (self.center_y - self.start_y) ** 2) ** 0.5
        return distance >= 8 * TILE_SIZE

    def start_return(self) -> None:
        self.state = BoomerangState.RETURNING

    def update_returning(self, player_x: float, player_y: float) -> None:
        dx = player_x - self.center_x
        dy = player_y - self.center_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance <= 8:
            self.state = BoomerangState.INACTIVE
            self.visible = False
            return

        self.center_x += 8 * dx / distance
        self.center_y += 8 * dy / distance
