from typing import Callable
import arcade

from progetto_grande.constants import SCALE
from progetto_grande.map import Map, limites_spinner
from progetto_grande.Monsters.bat import Bat
from progetto_grande.Monsters.spinner import Spinner
from progetto_grande.player import Player
from progetto_grande.textures import (
    ANIMATION_BAT,
    ANIMATION_BOOMERANG,
    ANIMATION_PLAYER_IDLE_DOWN,
)
from progetto_grande.Weapons.boomerang import Boomerang
from progetto_grande.Weapons.sword import Sword

SpriteList = arcade.SpriteList[arcade.Sprite]
BatList = arcade.SpriteList[Bat]
SpinnerList = arcade.SpriteList[Spinner]


def create_player(
    game_map: Map,
    grid_to_pixels: Callable[[int], int],
) -> Player:
    return Player(
        animation=ANIMATION_PLAYER_IDLE_DOWN,
        scale=SCALE,
        center_x=grid_to_pixels(game_map.player_start_x),
        center_y=grid_to_pixels(game_map.player_start_y),
    )

def create_player_list(player: Player) -> SpriteList:
    player_list: SpriteList = arcade.SpriteList()
    player_list.append(player)
    return player_list


def create_boomerang() -> Boomerang:
    return Boomerang(
        animation=ANIMATION_BOOMERANG,
        scale=SCALE,
    )

def create_sword() -> Sword:
    return Sword(scale=SCALE)

def create_boomerang_list(boomerang: Boomerang) -> SpriteList:
    boomerang_list: SpriteList = arcade.SpriteList()
    boomerang_list.append(boomerang)
    return boomerang_list

def create_sword_list(sword: Sword) -> SpriteList:
    sword_list: SpriteList = arcade.SpriteList()
    sword_list.append(sword)
    return sword_list

def create_spinner_list(
    game_map: Map,
    grid_to_pixels: Callable[[int], int],
) -> SpinnerList:
    spinner_list: SpinnerList = arcade.SpriteList()

    for spinner in game_map.spinners:
        min_limit, max_limit = limites_spinner(game_map, spinner)
        spinner_sprite = Spinner(
            center_x=grid_to_pixels(spinner.x),
            center_y=grid_to_pixels(spinner.y),
            min_limit=min_limit,
            max_limit=max_limit,
            spinner_move=spinner.move,
        )
        spinner_list.append(spinner_sprite)

    return spinner_list

def create_bat_list(
    game_map: Map,
    grid_to_pixels: Callable[[int], int],
) -> BatList:
    bat_list: BatList = arcade.SpriteList()

    for x, y in game_map.bats:
        bat = Bat(
            animation=ANIMATION_BAT,
            scale=SCALE,
            center_x=grid_to_pixels(x),
            center_y=grid_to_pixels(y),
        )
        bat_list.append(bat)

    return bat_list
