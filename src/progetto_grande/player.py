from enum import Enum

import arcade

from progetto_grande.constants import PLAYER_MOVEMENT_SPEED


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


class Player(arcade.TextureAnimationSprite):

    def __init__(self, animation: arcade.TextureAnimation , scale: float, center_x: float, center_y: float) -> None:
        super().__init__(
            animation=animation,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
        )
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False

        # direction debut
        self.direction = Direction.SOUTH
        self.last_horizontal = 0   # right = 1, left = -1
        self.last_vertical = 0     # up = 1, down = -1

    def press_key(self, symbol: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.go_right = True
                self.last_horizontal = 1
            case arcade.key.LEFT:
                self.go_left = True
                self.last_horizontal = -1
            case arcade.key.UP:
                self.go_up = True
                self.last_vertical = 1
            case arcade.key.DOWN:
                self.go_down = True
                self.last_vertical = -1
        self.update_direction()

    def release_key(self, symbol: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.go_right = False
            case arcade.key.LEFT:
                self.go_left = False
            case arcade.key.UP:
                self.go_up = False
            case arcade.key.DOWN:
                self.go_down = False

        self.update_direction()

    def update_direction(self) -> None:
        """
        orientation selon les regles de la consigne
        """
        if self.go_down:
            self.direction = Direction.SOUTH
        elif self.go_up:
            self.direction = Direction.NORTH
        elif self.go_left:
            self.direction = Direction.WEST
        elif self.go_right:
            self.direction = Direction.EAST

    def update_movement(self) -> None:
        # horizontal movement
        if self.go_right and self.go_left:
            self.change_x = self.last_horizontal * PLAYER_MOVEMENT_SPEED
        elif self.go_right:
            self.change_x = PLAYER_MOVEMENT_SPEED
        elif self.go_left:
            self.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.change_x = 0

        # vertical movement
        if self.go_up and self.go_down:
            self.change_y = self.last_vertical * PLAYER_MOVEMENT_SPEED
        elif self.go_up:
            self.change_y = PLAYER_MOVEMENT_SPEED
        elif self.go_down:
            self.change_y = -PLAYER_MOVEMENT_SPEED
        else:
            self.change_y = 0
