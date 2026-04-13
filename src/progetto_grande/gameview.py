from typing import Final
import arcade
from arcade.camera import Camera2D
from progetto_grande.map import Map, limites_spinner

from progetto_grande.player import Player, Direction

from progetto_grande.Weapons.boomerang import Boomerang, BoomerangState
from progetto_grande.Weapons.weapon import Weapon
from progetto_grande.Weapons.sword import Sword
from progetto_grande.Monsters.bat import Bat
from progetto_grande.Monsters.spinner import Spinner
from progetto_grande.world import create_world_sprites
from progetto_grande.ui import (
    create_weapon_icon,
    create_weapon_icon_list,
    create_weapon_icon_textures,
)
from progetto_grande.factory import (
    create_bat_list,
    create_boomerang,
    create_boomerang_list,
    create_player,
    create_player_list,
    create_spinner_list,
    create_sword,
    create_sword_list,
)

from progetto_grande.constants import (
    MAX_WINDOW_WIDTH,
    MAX_WINDOW_HEIGHT,
    TILE_SIZE,
    SCALE,
)
from progetto_grande.textures import (
    ANIMATION_PLAYER_IDLE_DOWN,
    ANIMATION_PLAYER_IDLE_UP,
    ANIMATION_PLAYER_IDLE_LEFT,
    ANIMATION_PLAYER_IDLE_RIGHT,
    ANIMATION_BAT
)
SpinnerList = arcade.SpriteList[Spinner]
SpriteList = arcade.SpriteList[arcade.Sprite]
AnimatedSpriteList = arcade.SpriteList[arcade.TextureAnimationSprite]
BatList = arcade.SpriteList[Bat]

def grid_to_pixels(i: int) -> int:
    return i * TILE_SIZE + (TILE_SIZE // 2)


class GameView(arcade.View):
    """Main in-game view."""

    world_width: Final[int]
    world_height: Final[int]

    player: Final[Player]
    player_list: Final[SpriteList]

    boomerang: Boomerang
    boomerang_list: Final[SpriteList]

    spinner_list: Final[SpinnerList]

    active_weapon: Weapon
    sword: Sword
    sword_list: Final[SpriteList]

    grounds: Final[SpriteList]
    walls: Final[SpriteList]
    crystals: Final[AnimatedSpriteList]
    physics_engine: Final[arcade.PhysicsEngineSimple]
    camera: Final[arcade.Camera2D]
    ui_camera: Camera2D

    bat_list: BatList
    holes: Final[SpriteList]

    def __init__(self, game_map: Map) -> None:
        super().__init__()
        self.map = game_map

        # Background + world size
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.world_width = self.map.width * TILE_SIZE
        self.world_height = self.map.height * TILE_SIZE

        # Player sprite
        self.player = create_player(self.map, grid_to_pixels)

        # Player list (for efficient drawing)
        self.player_list = create_player_list(self.player)

        #------------Weapons------------
        #Boomerang
        self.boomerang = create_boomerang()
        self.boomerang_list = create_boomerang_list(self.boomerang)

        # Weapon icons
        self.boomerang_icon_texture, self.sword_icon_texture = create_weapon_icon_textures()
        self.weapon_icon = create_weapon_icon(self.boomerang_icon_texture)
        self.weapon_icon_list = create_weapon_icon_list(self.weapon_icon)
        self.active_weapon = self.boomerang
        #Sword
        self.sword = create_sword()
        self.sword_list = create_sword_list(self.sword)

        # World sprite lists
        self.grounds, self.walls, self.crystals, self.holes = create_world_sprites(
            self.map,
            grid_to_pixels,
        )
        self.spinner_list = create_spinner_list(self.map, grid_to_pixels)
        self.bat_list = create_bat_list(self.map, grid_to_pixels)

        # Physics engine (player collides with walls)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.walls)
        self.camera = Camera2D()

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

    def create_spinner_list(self) -> arcade.SpriteList[Spinner]:
        spinner_list: arcade.SpriteList[Spinner] = arcade.SpriteList()

        for spinner in self.map.spinners:
            min_limit, max_limit = limites_spinner(self.map, spinner)
            spinner_sprite = Spinner(
                center_x=grid_to_pixels(spinner.x),
                center_y=grid_to_pixels(spinner.y),
                min_limit=min_limit,
                max_limit=max_limit,
                spinner_move=spinner.move,
            )
            spinner_list.append(spinner_sprite)

        return spinner_list

    def create_bat_list(self) -> BatList:
        bat_list: BatList = arcade.SpriteList()

        for x, y in self.map.bats:
            bat = Bat(
                animation=ANIMATION_BAT,
                scale=SCALE,
                center_x=grid_to_pixels(x),
                center_y=grid_to_pixels(y),
            )
            bat_list.append(bat)

        return bat_list

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

            weapon_name = self.active_weapon.name
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
        animations = {
            Direction.SOUTH: ANIMATION_PLAYER_IDLE_DOWN,
            Direction.NORTH: ANIMATION_PLAYER_IDLE_UP,
            Direction.WEST: ANIMATION_PLAYER_IDLE_LEFT,
            Direction.EAST: ANIMATION_PLAYER_IDLE_RIGHT,
        }
        self.player.animation = animations[self.player.direction]

    def near_enough_to_fall(self) -> bool:
        for hole in self.holes:
            if arcade.get_distance_between_sprites(self.player, hole) <= 16:
                return True
        return False

    def remove_hit_spinners(self, hit_spinners: list[Spinner]) -> None:
        if not hit_spinners:
            return

        for spinner in hit_spinners:
            spinner.kill()

    def remove_hit_bats(self, hit_bats: list[Bat]) -> None:
        if not hit_bats:
            return
        for bat in hit_bats:
            bat.kill()

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

    def update_player_state(self) -> None:
        self.player.update_movement()
        self.update_player_animation()
        self.physics_engine.update()

    def update_weapons_state(self) -> None:
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

    def update_animations(self) -> None:
        self.player.update_animation()
        self.crystals.update_animation()

    def update_camera_position(self) -> None:
        camera_x, camera_y = self.player.position

        half_camera_width = self.window.width / 2
        half_camera_height = self.window.height / 2

        camera_x = max(half_camera_width, min(camera_x, self.world_width - half_camera_width))
        camera_y = max(half_camera_height, min(camera_y, self.world_height - half_camera_height))

        self.camera.position = (camera_x, camera_y)

    def collect_player_crystals(self) -> None:
        hit_crystals = arcade.check_for_collision_with_list(self.player, self.crystals)
        for crystal in hit_crystals:
            crystal.remove_from_sprite_lists()
            arcade.play_sound(self.collect_sound)
            self.score += 1

        self.score_text.text = f"SCORE : {self.score}"

    def update_spinners(self) -> None:
        for spinner in self.spinner_list:
            spinner.update_spinner(grid_to_pixels)
        self.spinner_list.update_animation()


    def update_bats(self) -> None:
        for bat in self.bat_list:
            bat.update_bat()

    def update_monsters_state(self) -> None:
        self.update_spinners()
        self.update_bats()

    def reset_game(self) -> None:
        self.window.show_view(GameView(self.map))

    def player_touches_monster(self) -> bool:
        for spinner in self.spinner_list:
            if spinner.touches_player(self.player):
                return True

        for bat in self.bat_list:
            if bat.touches_player(self.player):
                return True

        return False

    def check_player_death(self) -> None:
        #contact entre joueur et monstres
        if self.player_touches_monster():
            self.reset_game()

        #tomber dans un trou
        if self.near_enough_to_fall():
            self.reset_game()

    def on_update(self, delta_time: float) -> None:
        self.update_player_state()
        self.update_weapons_state()
        self.update_animations()
        self.update_camera_position()
        self.collect_player_crystals()
        self.update_monsters_state()
        self.check_player_death()
