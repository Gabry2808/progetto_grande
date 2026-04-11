import arcade
from progetto_grande.player import Direction
from progetto_grande.textures import (
    ANIMATION_SWORD_DOWN,
    ANIMATION_SWORD_UP,
    ANIMATION_SWORD_LEFT,
    ANIMATION_SWORD_RIGHT,
)

class Sword(arcade.TextureAnimationSprite):
    def __init__(self, scale: float) -> None:
        super().__init__(animation=ANIMATION_SWORD_DOWN, scale=scale)
        self.active = False
        self.visible = False
        self.frame_count = 0

    def start(self, x: float, y: float, direction: Direction) -> None:
        self.center_x = x
        self.center_y = y

        if direction == Direction.SOUTH:
            self.animation = ANIMATION_SWORD_DOWN
        elif direction == Direction.NORTH:
            self.animation = ANIMATION_SWORD_UP
        elif direction == Direction.WEST:
            self.animation = ANIMATION_SWORD_LEFT
        elif direction == Direction.EAST:
            self.animation = ANIMATION_SWORD_RIGHT

        self.active = True
        self.visible = True
        self.frame_count = 0
        self.cur_frame_idx = 0 #reset animation

    def update_sword(self) -> None:
        if not self.active:
            return

        self.update_animation()
        self.frame_count += 1

        if self.frame_count > 18:
            self.active = False
            self.visible = False

    def use(self, player):
        if not self.active:
            self.start(
                player.center_x,
                player.center_y,
                player.direction,
            )
