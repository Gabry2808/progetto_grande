from typing import Final
import arcade
from arcade.camera import Camera2D
from progetto_grande.map import Map, GridCell, SpinnerMove, limites_spinner

from progetto_grande.player import Player, Direction

from progetto_grande.Weapons.boomerang import Boomerang, BoomerangState
from progetto_grande.Weapons.sword import Sword
from progetto_grande.Monsters.bat import Bat

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
    ANIMATION_PLAYER_IDLE_UP,
    ANIMATION_PLAYER_IDLE_LEFT,
    ANIMATION_PLAYER_IDLE_RIGHT,
    ANIMATION_CRYSTAL,
    ANIMATION_SPINNER,
    TEXTURE_HOLE,
    ANIMATION_BOOMERANG,
    ANIMATION_BAT
)

def grid_to_pixels(i: int) -> int:
    return i * TILE_SIZE + (TILE_SIZE // 2)


class GameView(arcade.View):
    """Main in-game view."""

    world_width: Final[int]
    world_height: Final[int]

    player: Final[Player]
    player_list: Final[arcade.SpriteList[arcade.Sprite]]

    grounds: Final[arcade.SpriteList[arcade.Sprite]]
    walls: Final[arcade.SpriteList[arcade.Sprite]]
    crystals: Final[arcade.SpriteList[arcade.TextureAnimationSprite]]
    physics_engine: Final[arcade.PhysicsEngineSimple]
    camera: Final[arcade.Camera2D]

    spinner_list: Final[arcade.SpriteList[arcade.TextureAnimationSprite]]
    spinner_info: list[tuple[arcade.TextureAnimationSprite, int, int, int, SpinnerMove]]

    score: int
    score_text: arcade.Text

    holes: Final[arcade.SpriteList[arcade.Sprite]]

    def __init__(self, game_map: Map) -> None:
        super().__init__()
        self.map = game_map

        # Background + world size
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.world_width = self.map.width * TILE_SIZE
        self.world_height = self.map.height * TILE_SIZE

        # Player sprite
        self.player = Player(
            animation=ANIMATION_PLAYER_IDLE_DOWN,
            scale=SCALE,
            center_x=grid_to_pixels(self.map.player_start_x),
            center_y=grid_to_pixels(self.map.player_start_y),
        )

        # Player list (for efficient drawing)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        #------------Weapons------------
        #Boomerang
        self.boomerang = Boomerang(
            animation=ANIMATION_BOOMERANG,
            scale=SCALE,
            )
        self.boomerang_list = arcade.SpriteList()
        self.boomerang_list.append(self.boomerang)
        self.active_weapon = self.boomerang
        # Weapon icons
        self.boomerang_icon_texture = arcade.load_texture("assets/provided/boomerang-sheet.png")
        self.sword_icon_texture = arcade.load_texture("assets/provided/boomerang-sheet.png")
        self.weapon_icon_list = arcade.SpriteList()
        self.weapon_icon: arcade.Sprite = arcade.Sprite(
            self.boomerang_icon_texture,
            scale=0.8,
        )
        self.weapon_icon_list.append(self.weapon_icon)
        #Sword
        self.sword = Sword(scale=SCALE)
        self.sword_list = arcade.SpriteList()
        self.sword_list.append(self.sword)

        # World sprite lists
        self.grounds = arcade.SpriteList(use_spatial_hash=True)
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.crystals = arcade.SpriteList(use_spatial_hash=True)

        self.spinner_list = arcade.SpriteList()
        self.spinner_info = []

        self.holes= arcade.SpriteList(use_spatial_hash=True)

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
                elif cell == GridCell.HOLE:
                    self.holes.append(
                        arcade.Sprite(
                        TEXTURE_HOLE,
                        scale=SCALE,
                        center_x=grid_to_pixels(x),
                        center_y=grid_to_pixels(y),
                        )
                    )

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
        #---------bats---------
        self.bat_list = arcade.SpriteList()
        for x, y in self.map.bats:
            bat = Bat(
                animation=ANIMATION_BAT,
                scale=SCALE,
                center_x=grid_to_pixels(x),
                center_y=grid_to_pixels(y),
            )
            self.bat_list.append(bat)



        # Physics engine (player collides with walls)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.walls)
        self.camera = arcade.camera.Camera2D()

        # camera ui
        self.ui_camera = Camera2D()

        # Load sound once
        self.collect_sound = arcade.load_sound(":resources:sounds/coin5.wav")

        #score
        self.score = 0
        self.score_text = arcade.Text(text=f"SCORE : {self.score}",
        x=20,y=self.window.height - 40 if self.window is not None else 20,
        font_size=18,)

    def on_show_view(self) -> None:
        self.window.width = min(MAX_WINDOW_WIDTH, self.world_width)
        self.window.height = min(MAX_WINDOW_HEIGHT, self.world_height)

        self.weapon_icon.center_x = 30
        self.weapon_icon.center_y = self.window.height - 30
        self.score_text.y = self.window.height - 40

    def on_draw(self) -> None:
        self.clear()

        with self.camera.activate():
            self.grounds.draw()
            self.holes.draw()
            self.walls.draw()
            self.crystals.draw()
            self.player_list.draw()

            self.spinner_list.draw()
            self.bat_list.draw()

            self.boomerang_list.draw()
            self.sword_list.draw()

        with self.ui_camera.activate():
            self.score_text.draw()
            self.weapon_icon_list.draw()

            weapon_name = "boomerang" if self.active_weapon == self.boomerang else "sword"
            arcade.draw_text(
                f"Weapon: {weapon_name}",
                20,
                self.window.height - 80,
                arcade.color.WHITE,
                12,
            )

    def update_weapon_icon(self) -> None:
        if self.active_weapon == self.boomerang:
            self.weapon_icon.texture = self.boomerang_icon_texture
        else:
            self.weapon_icon.texture = self.sword_icon_texture

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.D:
            self.active_weapon.use(self.player)
        elif symbol == arcade.key.R:
            if self.active_weapon == self.boomerang:
                    self.active_weapon = self.sword
            else:
                self.active_weapon = self.boomerang
            self.update_weapon_icon()
        else:
            self.player.press_key(symbol)


    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE :
            new_view = GameView(self.map)
            self.window.show_view(new_view)
        else :
            self.player.release_key(symbol)

    def update_player_animation(self) -> None:
        if self.player.direction == Direction.SOUTH:
            self.player.animation = ANIMATION_PLAYER_IDLE_DOWN
        elif self.player.direction == Direction.NORTH:
            self.player.animation = ANIMATION_PLAYER_IDLE_UP
        elif self.player.direction == Direction.WEST:
            self.player.animation = ANIMATION_PLAYER_IDLE_LEFT
        elif self.player.direction == Direction.EAST:
            self.player.animation = ANIMATION_PLAYER_IDLE_RIGHT

    def near_enough_to_fall(self) -> bool:
        for hole in self.holes:
            if arcade.get_distance_between_sprites(self.player, hole) <= 16:
                return True
        return False

    def remove_hit_spinners(self, hit_spinners) -> None:
        if not hit_spinners:
            return

        for spinner in hit_spinners:
            spinner.remove_from_sprite_lists()

        new_spinner_info = []
        for sprite, move, min_limit, max_limit, spinner_move in self.spinner_info:
            if sprite not in hit_spinners:
                new_spinner_info.append((sprite, move, min_limit, max_limit, spinner_move))

        self.spinner_info = new_spinner_info

    def remove_hit_bats(self, hit_bats: list[arcade.Sprite]) -> None:
        if not hit_bats:
            return
        for bat in hit_bats:
            bat.remove_from_sprite_lists()

    def update_boomerang(self) -> None:
        if self.boomerang.state == BoomerangState.INACTIVE:
            return

        if self.boomerang.state == BoomerangState.LAUNCHING:
            self.boomerang.update_launching()

            if arcade.check_for_collision_with_list(self.boomerang, self.walls):
                self.boomerang.start_return()

            hit_spinners = arcade.check_for_collision_with_list(self.boomerang, self.spinner_list)
            self.remove_hit_spinners(hit_spinners)

            if hit_spinners:
                self.boomerang.start_return()

            hit_bats = arcade.check_for_collision_with_list(self.boomerang, self.bat_list)
            self.remove_hit_bats(hit_bats)

            if hit_bats:
                self.boomerang.start_return()

            if self.boomerang.too_far():
                self.boomerang.start_return()

        elif self.boomerang.state == BoomerangState.RETURNING:
            hit_spinners = arcade.check_for_collision_with_list(self.boomerang, self.spinner_list)
            self.remove_hit_spinners(hit_spinners)

            hit_bats = arcade.check_for_collision_with_list(self.boomerang, self.bat_list)
            self.remove_hit_bats(hit_bats)

            self.boomerang.update_returning(
                self.player.center_x,
                self.player.center_y,
                )

        self.boomerang.update_animation()



    def on_update(self, delta_time: float) -> None:
        self.player.update_movement()
        self.update_player_animation()
        # Physics
        self.physics_engine.update()
        # Weapon
        self.update_boomerang()
        self.sword.update_sword()
        if self.sword.active:
            hit_bats = arcade.check_for_collision_with_list(self.sword, self.bat_list)
            self.remove_hit_bats(hit_bats)
            hit_crystals = arcade.check_for_collision_with_list(self.sword, self.crystals)
            for crystal in hit_crystals:
                crystal.remove_from_sprite_lists()
                arcade.play_sound(self.collect_sound)
                self.score += 1
        # Update animations
        self.player.update_animation()
        self.crystals.update_animation()

        # Camera followfor spin
        """target_x, target_y = self.player.position
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

        self.camera.position = self.player.position """

        camera_x, camera_y = self.player.position

        half_camera_width = self.window.width / 2
        half_camera_height = self.window.height / 2

        camera_x = max(half_camera_width, min(camera_x, self.world_width - half_camera_width))
        camera_y = max(half_camera_height, min(camera_y, self.world_height - half_camera_height))

        self.camera.position = (camera_x, camera_y)

        # Crystal collision
        hit_crystals = arcade.check_for_collision_with_list(self.player, self.crystals)
        for c in hit_crystals:
            c.remove_from_sprite_lists()
            arcade.play_sound(self.collect_sound)
            self.score += 1
        self.score_text.text = f"SCORE : {self.score}"

        #------------Monsters------------
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
        #bats
        for bat in self.bat_list:
            bat.update_bat()
        #contact entre joueur et monstres
        if (
            arcade.check_for_collision_with_list(self.player, self.bat_list)
            or arcade.check_for_collision_with_list(self.player, self.spinner_list)
        ):
            game_over = GameView(self.map)
            self.window.show_view(game_over)

        #tomber dans un trou
        if self.near_enough_to_fall():
            game_over = GameView(self.map)
            self.window.show_view(game_over)
