import arcade


class Monster(arcade.TextureAnimationSprite):
    def kill(self) -> None:
        self.remove_from_sprite_lists()

    def touches_player(self, player: arcade.Sprite) -> bool:
        return arcade.check_for_collision(self, player)
