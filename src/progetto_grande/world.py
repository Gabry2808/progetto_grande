import arcade
from typing import Callable

from progetto_grande.constants import SCALE
from progetto_grande.map import GridCell, Map
from progetto_grande.textures import (
    ANIMATION_CRYSTAL,
    TEXTURE_BUSH,
    TEXTURE_GRASS,
    TEXTURE_HOLE,
)

SpriteList = arcade.SpriteList[arcade.Sprite]
AnimatedSpriteList = arcade.SpriteList[arcade.TextureAnimationSprite]


def create_world_sprites(
    game_map: Map,
    grid_to_pixels: Callable[[int], int],
) -> tuple[SpriteList, SpriteList, AnimatedSpriteList, SpriteList]:

    grounds, walls, holes = (
        arcade.SpriteList(use_spatial_hash=True),
        arcade.SpriteList(use_spatial_hash=True),
        arcade.SpriteList(use_spatial_hash=True),
    )
    crystals = arcade.SpriteList(use_spatial_hash=True)

    for y in range(game_map.height):
        for x in range(game_map.width):
            grounds.append(
                arcade.Sprite(
                    TEXTURE_GRASS,
                    scale=SCALE,
                    center_x=grid_to_pixels(x),
                    center_y=grid_to_pixels(y),
                )
            )

            cell = game_map.get(x, y)

            if cell == GridCell.BUSH:
                walls.append(
                    arcade.Sprite(
                        TEXTURE_BUSH,
                        scale=SCALE,
                        center_x=grid_to_pixels(x),
                        center_y=grid_to_pixels(y),
                    )
                )
            elif cell == GridCell.CRYSTAL:
                crystal = arcade.TextureAnimationSprite(
                    animation=ANIMATION_CRYSTAL,
                    scale=SCALE,
                    center_x=grid_to_pixels(x),
                    center_y=grid_to_pixels(y),
                )
                crystals.append(crystal)
            elif cell == GridCell.HOLE:
                holes.append(
                    arcade.Sprite(
                        TEXTURE_HOLE,
                        scale=SCALE,
                        center_x=grid_to_pixels(x),
                        center_y=grid_to_pixels(y),
                    )
                )

    return grounds, walls, crystals, holes
