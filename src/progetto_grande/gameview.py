from typing import Final
from collections.abc import Sequence, Iterator
import arcade
from arcade.camera import Camera2D
from progetto_grande.map import Map

from progetto_grande.player import Player

from progetto_grande.Weapons.boomerang import Boomerang, BoomerangState
from progetto_grande.Weapons.weapon import Weapon
from progetto_grande.Weapons.sword import Sword
from progetto_grande.Monsters.bat import Bat
from progetto_grande.Monsters.blob import Blob
from progetto_grande.Monsters.spinner import Spinner
from progetto_grande.Monsters.monster import Monster
from progetto_grande.world import create_world_sprites
from progetto_grande.display import (
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
    create_blob_list
)

from progetto_grande.constants import (
    MAX_WINDOW_WIDTH,
    MAX_WINDOW_HEIGHT,
    TILE_SIZE,
)

SpinnerList = arcade.SpriteList[Spinner]
SpriteList = arcade.SpriteList[arcade.Sprite]
AnimatedSpriteList = arcade.SpriteList[arcade.TextureAnimationSprite]
BatList = arcade.SpriteList[Bat]
BlobList = arcade.SpriteList[Blob]

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
    blob_list: BlobList
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
        self.blob_list = create_blob_list(
            self.map,
            grid_to_pixels,
            self.player,
            self.walls,
        )

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
            self.blob_list.draw()

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


    def near_enough_to_fall(self) -> bool:
        # Grâce à la function check_for_collision_with_list:
        # -> Complexité : O(k), où k est le nombre de trous proches du joueur.
        hit_holes = arcade.check_for_collision_with_list(self.player, self.holes)

        for hole in hit_holes:
            if arcade.get_distance_between_sprites(self.player, hole) <= 16:
                return True
        return False

    def remove_hit_monsters(self, hit_monsters: Sequence[Monster]) -> None:
        for monster in hit_monsters:
            monster.kill()

    def update_boomerang(self) -> None:
        if self.boomerang.state == BoomerangState.INACTIVE:
            return

        if self.boomerang.state == BoomerangState.LAUNCHING:
            self.boomerang.update_launching()

            if arcade.check_for_collision_with_list(self.boomerang, self.walls):
                self.boomerang.start_return()

            hit_spinners = arcade.check_for_collision_with_list(self.boomerang, self.spinner_list)
            self.remove_hit_monsters(hit_spinners)

            if hit_spinners:
                self.boomerang.start_return()

            hit_bats = arcade.check_for_collision_with_list(self.boomerang, self.bat_list)
            self.remove_hit_monsters(hit_bats)

            if hit_bats:
                self.boomerang.start_return()

            if self.boomerang.too_far():
                self.boomerang.start_return()

        elif self.boomerang.state == BoomerangState.RETURNING:
            hit_spinners = arcade.check_for_collision_with_list(self.boomerang, self.spinner_list)
            self.remove_hit_monsters(hit_spinners)

            hit_bats = arcade.check_for_collision_with_list(self.boomerang, self.bat_list)
            self.remove_hit_monsters(hit_bats)

            self.boomerang.update_returning(
                self.player.center_x,
                self.player.center_y,
                )

        self.boomerang.update_animation()

    def update_player_state(self) -> None:
        # Mis à jour du mouvement et animation du joueur
        self.player.update_movement()
        self.player.update_animation_state()
        self.physics_engine.update()

    def update_weapons_state(self) -> None:
        self.update_boomerang()
        self.sword.update_sword()

        if self.sword.active:
            hit_bats = arcade.check_for_collision_with_list(self.sword, self.bat_list)
            self.remove_hit_monsters(hit_bats)

            hit_crystals = arcade.check_for_collision_with_list(self.sword, self.crystals)
            for crystal in hit_crystals:
                crystal.remove_from_sprite_lists()
                arcade.play_sound(self.collect_sound)
                self.score += 1

    def update_animations(self) -> None:
        self.player.update_animation()
        self.crystals.update_animation()

    def update_camera_position(self) -> None:
        #Position de la caméra = Position actuelle du joueur
        camera_x, camera_y = self.player.position

         # On calcule la moitié de la taille visible de la fenêtre
        half_camera_width = self.window.width / 2
        half_camera_height = self.window.height / 2

        # On limite la position de la caméra:
        # la caméera reste entre les bords du monde
        camera_x = max(
            half_camera_width,
            min(camera_x, self.world_width - half_camera_width)
        )
        camera_y = max(
            half_camera_height,
            min(camera_y, self.world_height - half_camera_height)
        )
        self.camera.position = (camera_x, camera_y)

    def collect_player_crystals(self) -> None:
        hit_crystals = arcade.check_for_collision_with_list(self.player, self.crystals)
        for crystal in hit_crystals:
            crystal.remove_from_sprite_lists()
            arcade.play_sound(self.collect_sound)
            self.score += 1

        self.score_text.text = f"SCORE : {self.score}"


    def update_monsters_state(self) -> None:
        for monster in self.all_monsters():
            monster.update_monster(grid_to_pixels)
        self.spinner_list.update_animation()

    def reset_game(self) -> None:
        self.window.show_view(GameView(self.map))

    #Itérateur regroupant tous les monstres
    def all_monsters(self) -> Iterator[Monster]:
        yield from self.spinner_list
        yield from self.bat_list
        yield from self.blob_list

    def player_touches_monster(self) -> bool:
        #On vérifie si le joueur est en contact avec un monstre
        for monster in self.all_monsters():
            if monster.touches_player(self.player):
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
