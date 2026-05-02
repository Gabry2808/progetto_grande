from typing import Callable
import arcade
from abc import abstractmethod

class Monster(arcade.TextureAnimationSprite):
    def kill(self) -> None:
        self.remove_from_sprite_lists()

    def touches_player(self, player: arcade.Sprite) -> bool:
        return arcade.check_for_collision(self, player)

    @abstractmethod
    def update_monster(self, grid_to_pixels: Callable[[int], int]) -> None:
        pass
