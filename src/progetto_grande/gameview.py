from typing import Final
import arcade

from progetto_grande.constants import (
    MAX_WINDOW_WIDTH,
    MAX_WINDOW_HEIGHT,
    TILE_SIZE,
    SCALE,
    PLAYER_MOVEMENT_SPEED,
)
from progetto_grande.textures import (
    TEXTURE_GRASS,
    TEXTURE_BUSH,
    ANIMATION_PLAYER_IDLE_DOWN,
    ANIMATION_CRYSTAL,
)

def grid_to_pixels(i: int) -> int:
    return i * TILE_SIZE + (TILE_SIZE // 2)


class GameView(arcade.View):
    """Main in-game view."""

    world_width: Final[int]
    world_height: Final[int]

    player: Final[arcade.Sprite]
    player_list: Final[arcade.SpriteList[arcade.Sprite]]

    grounds: Final[arcade.SpriteList[arcade.Sprite]]
    walls: Final[arcade.SpriteList[arcade.Sprite]]
    crystals: Final[arcade.SpriteList[arcade.TextureAnimationSprite]]
    physics_engine: Final[arcade.PhysicsEngineSimple]
    camera: Final[arcade.Camera2D]

    def __init__(self) -> None:
        super().__init__()

        # Background + world size
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.world_width = 40 * TILE_SIZE
        self.world_height = 20 * TILE_SIZE

        # Player sprite
        self.player = arcade.TextureAnimationSprite(
            animation=ANIMATION_PLAYER_IDLE_DOWN,
            scale=SCALE,
            center_x=grid_to_pixels(2),
            center_y=grid_to_pixels(2),
        )

        # Player list (for efficient drawing)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # World sprite lists
        self.grounds = arcade.SpriteList(use_spatial_hash=True)
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.crystals = arcade.SpriteList(use_spatial_hash=True)

        for (x, y) in [(5, 2), (6, 5), (3, 5)]:
            crystal = arcade.TextureAnimationSprite(
                animation=ANIMATION_CRYSTAL,
                scale=SCALE,
                center_x=grid_to_pixels(x),
                center_y=grid_to_pixels(y),
            )
            self.crystals.append(crystal)

        # Fill with grass (40 x 20 tiles)
        for x in range(40):
            for y in range(20):
                self.grounds.append(
                    arcade.Sprite(
                        TEXTURE_GRASS,
                        scale=SCALE,
                        center_x=grid_to_pixels(x),
                        center_y=grid_to_pixels(y),
                    )
                )

        # Add bushes (walls)
        for (x, y) in [(3, 6), (7, 2), (2, 10), (3, 8)]:
            self.walls.append(
                arcade.Sprite(
                    TEXTURE_BUSH,
                    scale=SCALE,
                    center_x=grid_to_pixels(x),
                    center_y=grid_to_pixels(y),
                )
            )

        # Bush border (world limits)
        for x in range(40):
            for y in (0, 19):
                self.walls.append(
                    arcade.Sprite(
                        TEXTURE_BUSH,
                        scale=SCALE,
                        center_x=grid_to_pixels(x),
                        center_y=grid_to_pixels(y),
                    )
                )

        for y in range(20):
            for x in (0, 39):
                self.walls.append(
                    arcade.Sprite(
                        TEXTURE_BUSH,
                        scale=SCALE,
                        center_x=grid_to_pixels(x),
                        center_y=grid_to_pixels(y),
                    )
                )

        # Physics engine (player collides with walls)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.walls)
        self.camera = arcade.camera.Camera2D()

    def on_show_view(self) -> None:
        self.window.width = min(MAX_WINDOW_WIDTH, self.world_width)
        self.window.height = min(MAX_WINDOW_HEIGHT, self.world_height)

    def on_draw(self) -> None:
        self.clear()

        with self.camera.activate():
            self.grounds.draw()
            self.walls.draw()
            self.crystals.draw()
            self.player_list.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.player.change_x = +PLAYER_MOVEMENT_SPEED
            case arcade.key.LEFT:
                self.player.change_x = -PLAYER_MOVEMENT_SPEED
            case arcade.key.UP:
                self.player.change_y = +PLAYER_MOVEMENT_SPEED
            case arcade.key.DOWN:
                self.player.change_y = -PLAYER_MOVEMENT_SPEED

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.RIGHT | arcade.key.LEFT:
                self.player.change_x = 0
            case arcade.key.UP | arcade.key.DOWN:
                self.player.change_y = 0
            case arcade.key.ESCAPE:
                new_view = GameView()
                self.window.show_view(new_view)

    def on_update(self, delta_time: float) -> None:
        # Physics
        self.physics_engine.update()

        # Update animations
        self.player.update_animation()
        self.crystals.update_animation()

        # Camera follow
        target_x, target_y = self.player.position

        half_width = self.window.width / 2
        half_height = self.window.height / 2

        min_x = half_width
        max_x = self.world_width - half_width
        min_y = half_height
        max_y = self.world_height - half_height

        clamped_x = max(min_x, min(target_x, max_x))
        clamped_y = max(min_y, min(target_y, max_y))

        self.camera.position = (clamped_x, clamped_y)

        # Crystal collision
        hit_crystals = arcade.check_for_collision_with_list(self.player, self.crystals)
        for c in hit_crystals:
            c.remove_from_sprite_lists()
