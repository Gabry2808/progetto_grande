from typing import Final
import arcade
from progetto_grande.map import Map, GridCell, SpinnerMove, limites_spinner

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
    ANIMATION_SPINNER,
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

    spinner_list: Final[arcade.SpriteList[arcade.TextureAnimationSprite]]
    spinner_info: list[tuple[arcade.TextureAnimationSprite, int, int, int, SpinnerMove]]


    def __init__(self, game_map: Map) -> None:
        super().__init__()
        self.map = game_map

        # Background + world size
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.world_width = self.map.width * TILE_SIZE
        self.world_height = self.map.height * TILE_SIZE

        # Player sprite
        self.player = arcade.TextureAnimationSprite(
            animation=ANIMATION_PLAYER_IDLE_DOWN,
            scale=SCALE,
            center_x=grid_to_pixels(self.map.player_start_x),
            center_y=grid_to_pixels(self.map.player_start_y),
        )

        # Player list (for efficient drawing)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # actual directions required for the joueur
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False
        # Last direction requested on each axis
        self.last_horizontal = 0   # 1 = right, -1 = left, 0 = none
        self.last_vertical = 0     # 1 = up, -1 = down, 0 = none

        # World sprite lists
        self.grounds = arcade.SpriteList(use_spatial_hash=True)
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.crystals = arcade.SpriteList(use_spatial_hash=True)

        self.spinner_list = arcade.SpriteList()
        self.spinner_info = []

        for y in range(self.map.height):
            for x in range(self.map.width):
                self.grounds.append(
                    arcade.Sprite(
                        TEXTURE_GRASS,
                        scale=SCALE,
                        center_x=grid_to_pixels(x),
                        center_y=grid_to_pixels(y),
                    )
                )

                cell = self.map.get(x, y)

                if cell == GridCell.BUSH:
                    self.walls.append(
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
                    self.crystals.append(crystal)

        for spinner in self.map.spinners:
            sprite =arcade.TextureAnimationSprite(animation=ANIMATION_SPINNER,
            scale= SCALE,
            center_x= grid_to_pixels(spinner.x),
            center_y= grid_to_pixels(spinner.y)
            )
            min_limit, max_limit = limites_spinner(self.map, spinner)
            self.spinner_list.append(sprite)
            self.spinner_info.append(
                (sprite, 1, min_limit, max_limit, spinner.move)
            )


        # Physics engine (player collides with walls)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.walls)
        self.camera = arcade.camera.Camera2D()

        # Load sound once
        self.collect_sound = arcade.load_sound(":resources:sounds/coin5.wav")

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

            self.spinner_list.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
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

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.go_right = False
            case arcade.key.LEFT:
                self.go_left = False
            case arcade.key.UP:
                self.go_up = False
            case arcade.key.DOWN:
                self.go_down = False
            case arcade.key.ESCAPE:
                new_view = GameView(self.map)
                self.window.show_view(new_view)

    def on_update(self, delta_time: float) -> None:
        # Horizontal movement
        self.player.change_x = (
            self.last_horizontal * PLAYER_MOVEMENT_SPEED
            if self.go_right and self.go_left
            else (PLAYER_MOVEMENT_SPEED if self.go_right else (-PLAYER_MOVEMENT_SPEED if self.go_left else 0))
        )

        # Vertical movement
        self.player.change_y = (
            self.last_vertical * PLAYER_MOVEMENT_SPEED
            if self.go_up and self.go_down
            else (PLAYER_MOVEMENT_SPEED if self.go_up else (-PLAYER_MOVEMENT_SPEED if self.go_down else 0))
        )
        # Physics
        self.physics_engine.update()

        # Update animations
        self.player.update_animation()
        self.crystals.update_animation()

        # Camera follow
        target_x, target_y = self.player.position
        camera_x, camera_y = self.camera.position

        MARGIN = 100
        if abs(target_x - camera_x) > MARGIN:
            camera_x = target_x - MARGIN if target_x > camera_x else target_x + MARGIN
        if abs(target_y - camera_y) > MARGIN:
            camera_y = target_y - MARGIN if target_y > camera_y else target_y + MARGIN

        half_camera_width = self.window.width / 2
        half_camera_height  = self.window.height / 2

        camera_x = max(half_camera_width, min(camera_x, self.world_width - half_camera_width))
        camera_y = max(half_camera_height, min(camera_y, self.world_height - half_camera_height))

        self.camera.position = (camera_x, camera_y)

        # Crystal collision
        hit_crystals = arcade.check_for_collision_with_list(self.player, self.crystals)
        for c in hit_crystals:
            c.remove_from_sprite_lists()
            arcade.play_sound(self.collect_sound)

        #mouvement des spinners
        new_spinner_info = []
        for sprite, move, min_limit, max_limit,spinner_move in self.spinner_info :
            if spinner_move == SpinnerMove.HORIZONTAL:
                sprite.center_x += 3 * move
                left_px = grid_to_pixels(min_limit)
                right_px = grid_to_pixels(max_limit)

                if sprite.center_x >= right_px:
                    sprite.center_x = right_px
                    move = -1
                elif sprite.center_x <= left_px:
                    sprite.center_x = left_px
                    move = 1
            else:
                sprite.center_y += 3 * move

                bottom_px= grid_to_pixels(min_limit)
                top_px = grid_to_pixels(max_limit)

                if sprite.center_y >= top_px :
                    sprite.center_y = top_px
                    move = -1
                elif sprite.center_y <= bottom_px :
                    sprite.center_y = bottom_px
                    move = 1

            new_spinner_info.append(
                (sprite, move, min_limit, max_limit, spinner_move)
            )
        self.spinner_info =new_spinner_info
        self.spinner_list.update_animation()

        #contact entre joueur

        if arcade.check_for_collision_with_list(self.player, self.spinner_list):
            restart = GameView(self.map)
            self.window.show_view(restart)
