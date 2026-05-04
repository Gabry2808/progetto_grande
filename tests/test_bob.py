import arcade

from progetto_grande.Monsters.blob import Blob
from progetto_grande.map import GridCell, Map
from progetto_grande.textures import ANIMATION_BLOB
from progetto_grande.constants import SCALE, TILE_SIZE
from progetto_grande.player import Player
from progetto_grande.textures import ANIMATION_PLAYER_IDLE_DOWN
from progetto_grande.navmesh import build_navmesh, node_to_cell

player = Player(
    animation=ANIMATION_PLAYER_IDLE_DOWN,
    scale=SCALE,
    center_x=0,
    center_y=0,
)

def make_test_map() -> Map:
    game_map = Map(
        width=5,
        height=5,
        grid=(
            (
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
            ),
            (
                GridCell.GRASS,
                GridCell.BUSH,
                GridCell.GRASS,
                GridCell.HOLE,
                GridCell.GRASS,
            ),
            (
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
            ),
            (
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
            ),
            (
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
                GridCell.GRASS,
            ),
        ),
        player_start_x=0,
        player_start_y=0,
        spinners=[],
        bats=(),
        blobs=(),
    )
    game_map.navmesh = build_navmesh(game_map)
    return game_map


def make_blob() -> Blob:
    game_map = make_test_map()
    player = Player(
        animation=ANIMATION_PLAYER_IDLE_DOWN,
        scale=SCALE,
        center_x=0,
        center_y=0,
    )
    walls: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
    return Blob(
        animation=ANIMATION_BLOB,
        scale=SCALE,
        center_x=2 * TILE_SIZE + TILE_SIZE // 2,
        center_y=2 * TILE_SIZE + TILE_SIZE // 2,
        game_map = game_map,
        player=player,
        walls=walls,
    )

def test_blob_cell_to_pixel() -> None:
    blob = make_blob()

    assert blob.cell_to_pixel((0, 0)) == arcade.Vec2(16, 16)
    assert blob.cell_to_pixel((2, 3)) == arcade.Vec2(80, 112)

def test_blob_compute_valid_destinations() -> None:
    blob = make_blob()

    destinations = blob.compute_valid_destinations()

    assert arcade.Vec2(1 * TILE_SIZE + TILE_SIZE // 2, 1 * TILE_SIZE + TILE_SIZE // 2) not in destinations
    assert arcade.Vec2(3 * TILE_SIZE + TILE_SIZE // 2, 1 * TILE_SIZE + TILE_SIZE // 2) not in destinations
    assert arcade.Vec2(2 * TILE_SIZE + TILE_SIZE // 2, 2 * TILE_SIZE + TILE_SIZE // 2) in destinations

def test_blob_choose_random_destination_computes_path() -> None:
    blob = make_blob()
    blob.choose_random_destination()

    assert blob.destination in blob.valid_destinations
    assert blob.path
    assert node_to_cell(blob.path[-1]) == blob.position_to_cell(blob.destination)

# pathfinding
def test_blob_compute_path() -> None:
    blob = make_blob()
    blob.compute_path((4, 4))

    assert node_to_cell(blob.path[0]) == blob.position_to_cell(blob.current_position())
    assert node_to_cell(blob.path[-1]) == (4, 4)
    assert blob.path_index == 1

# visibility
def test_blob_cannot_see_player_too_far() -> None:
    blob = make_blob()

    blob.player.center_x = 1000
    blob.player.center_y = 1000

    assert not blob.can_see_player()

def test_blob_can_see_player_when_close() -> None:
    blob = make_blob()

    blob.player.center_x = blob.center_x + TILE_SIZE
    blob.player.center_y = blob.center_y

    assert blob.can_see_player()

def test_blob_cannot_see_player_behind_wall() -> None:
    blob = make_blob()

    wall = arcade.Sprite(
        center_x=blob.center_x + TILE_SIZE,
        center_y=blob.center_y,
        scale=SCALE,
    )
    blob.walls.append(wall)
    blob.player.center_x = blob.center_x + 2 * TILE_SIZE
    blob.player.center_y = blob.center_y

    assert not blob.can_see_player()

# update behaviour
def test_blob_update_computes_path_to_player_when_visible() -> None:
    blob = make_blob()

    blob.player.center_x = blob.center_x + TILE_SIZE
    blob.player.center_y = blob.center_y

    blob.update_monster(lambda i: i * TILE_SIZE + TILE_SIZE // 2)
    player_cell = blob.position_to_cell(
        arcade.Vec2(blob.player.center_x, blob.player.center_y)
    )

    assert blob.path
    assert node_to_cell(blob.path[-1]) == player_cell

def test_blob_update_stops_chasing_when_player_not_visible() -> None:
    blob = make_blob()
    blob.chasing_player = True

    blob.player.center_x = 1000
    blob.player.center_y = 1000
    blob.update_monster(lambda i: i * TILE_SIZE + TILE_SIZE // 2)

    assert not blob.chasing_player
    assert blob.path
