from typing import Final
import arcade

ORIG_TILE_SIZE = (16, 16)


def _load_grid(
    file: str,
    columns: int,
    rows: int,
    tile_size: tuple[int, int] = ORIG_TILE_SIZE,
) -> list[arcade.Texture]:
    spritesheet = arcade.load_spritesheet(file)
    return spritesheet.get_texture_grid(tile_size, columns, columns * rows)

def _load_animation_strip(
    file: str,
    frame_count: int,
    frame_duration: int = 100,
    tile_size: tuple[int, int] = ORIG_TILE_SIZE,
) -> arcade.TextureAnimation:
    grid = _load_grid(file, columns=frame_count, rows=1, tile_size=tile_size)
    keyframes = [arcade.TextureKeyframe(frame, frame_duration) for frame in grid]
    return arcade.TextureAnimation(keyframes)

_overworld_grid = _load_grid(
    "assets/Top_Down_Adventure_Pack_v.1.0/Overworld_Tileset.png", 18, 13
)

TEXTURE_GRASS: Final[arcade.Texture] = _overworld_grid[18 * 1 + 6]
TEXTURE_BUSH: Final[arcade.Texture] = _overworld_grid[18 * 3 + 5]

TEXTURE_HOLE: Final[arcade.Texture] = _overworld_grid[18 * 4 + 8]

ANIMATION_PLAYER_IDLE_DOWN: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_idle_down_anim_strip_6.png",
    6,
)
ANIMATION_PLAYER_IDLE_UP: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_idle_up_anim_strip_6.png",
    6,
)
ANIMATION_PLAYER_IDLE_LEFT: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_idle_left_anim_strip_6.png",
    6,
)
ANIMATION_PLAYER_IDLE_RIGHT: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_idle_right_anim_strip_6.png",
    6,
)
ANIMATION_CRYSTAL: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Props_Items_(animated)/crystal_item_anim_strip_6.png",
    6,
)

ANIMATION_SPINNER: Final[arcade. TextureAnimation]= _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Spinner_Sprites/spinner_run_attack_anim_all_dir_strip_8.png",
    3,
)

ANIMATION_BAT: Final[arcade. TextureAnimation]= _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Pinkbat_Sprites/pinkbat_idle_left_anim_strip_5.png" ,
    5,
)

ANIMATION_BOOMERANG= _load_animation_strip(
    "assets/provided/boomerang-sheet.png",
    8,
    25,
)

ANIMATION_SWORD_DOWN: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_attack48_down_anim_strip_6.png",
    6,
    50,
    tile_size=(48, 48),
)

ANIMATION_SWORD_UP: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_attack48_up_anim_strip_6.png",
    6,
    50,
    tile_size=(48, 48),
)

ANIMATION_SWORD_LEFT: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_attack48_left_anim_strip_6.png",
    6,
    50,
    tile_size=(48, 48),
)

ANIMATION_SWORD_RIGHT: Final[arcade.TextureAnimation] = _load_animation_strip(
    "assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_attack48_right_anim_strip_6.png",
    6,
    50,
    tile_size=(48, 48),
)
