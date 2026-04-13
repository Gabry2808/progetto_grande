from abc import ABC, abstractmethod
import arcade

from progetto_grande.player import Player


class Weapon(arcade.TextureAnimationSprite, ABC):
    name: str

    @abstractmethod
    def use(self, player: Player) -> None:
        pass

    @abstractmethod
    def is_active(self) -> bool:
        pass
