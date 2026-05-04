from typing import Callable
import arcade
import random
import networkx as nx
from progetto_grande.Monsters.monster import Monster
from progetto_grande.map import Map, GridCell
from progetto_grande.constants import TILE_SIZE
from progetto_grande.player import Player
from progetto_grande.navmesh import (
    Node,
    closest_node,
    node_to_position,
    shortest_path,
    node_to_cell,
)

MAX_OFFSET = 3

Cell = tuple[int, int]
Position = arcade.Vec2

def pixels_to_grid(value: float) -> int:
    return int(value // TILE_SIZE)

class Blob(Monster):
    def __init__(
        self,
        animation: arcade.TextureAnimation,
        scale: float,
        center_x: float,
        center_y: float,
        game_map: Map,
        player: Player,
        walls: arcade.SpriteList[arcade.Sprite],
    ) -> None:
        super().__init__(
            animation = animation,
            scale= scale,
            center_x=center_x,
            center_y=center_y,
        )
        self.start_position: Position = Position(center_x, center_y)
        self.game_map = game_map
        self.player = player
        self.chasing_player = False
        self.walls = walls

        self.speed = 1.0
        self.valid_destinations = self.compute_valid_destinations()
        self.destination: Position = Position(center_x, center_y)
        self.path: list[Node] = []
        self.path_index = 0
        self.choose_random_destination()

    def current_position(self) -> Position:
        return Position(self.center_x, self.center_y)

    def position_to_cell(self, position: Position) -> Cell:
        return (
            pixels_to_grid(position.x),
            pixels_to_grid(position.y),
        )

    def cell_to_pixel(self, cell: Cell) -> Position:
        x, y = cell
        return Position(
            x * TILE_SIZE + TILE_SIZE // 2,
            y * TILE_SIZE + TILE_SIZE // 2,
        )

    #On calcune le destination possibles dans la zone de patrouille
    def compute_valid_destinations(self) -> list[Position]:
        destinations: list[Position] = []

        start_cell = self.position_to_cell(self.start_position)

        for dx in range(-MAX_OFFSET, MAX_OFFSET+ 1):
            for dy in range(-MAX_OFFSET, MAX_OFFSET + 1):
                cell: Cell = (start_cell[0] + dx, start_cell[1] + dy)

                # On garde seulement les cellules accessibles
                if self.game_map.is_walkable(cell):
                    destinations.append(self.cell_to_pixel(cell))

        return destinations

    def choose_random_destination(self) -> None:
        destination = random.choice(self.valid_destinations)
        self.destination = destination

        destination_cell = self.position_to_cell(destination)
        self.compute_path(destination_cell)

    def can_see_player(self) -> bool:
        distance = arcade.get_distance_between_sprites(self, self.player)
        if distance > 5 * TILE_SIZE: #distance limitée
            return False
        return arcade.has_line_of_sight(
            self.position,
            self.player.position,
            self.walls,
        )

    # On calcule le plus court chemin entre la position
    # actuelle du blob et une cellule cible
    def compute_path(self, target: Cell) -> None:
        navmesh = self.game_map.navmesh
        if navmesh is None: return

        if not self.game_map.is_walkable(target):
            self.path = []
            return

        start_position = (self.center_x, self.center_y)
        target_position_vec = self.cell_to_pixel(target)
        target_position = (target_position_vec.x, target_position_vec.y)

        start_node = closest_node(navmesh, start_position)
        target_node = closest_node(navmesh, target_position)

        try:
            self.path = shortest_path(navmesh, start_node, target_node)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            self.path = []  # S'il n'y a pas de chemin possible, liste vide

        # On commence au deuxième point du chemin pour éviter
        # de rester bloqué sur la cellule actuelle
        self.path_index = 1 if len(self.path) > 1 else 0

    # Le blob suit le chemin calculé.
    def move_along_path(self) -> None:
        if not self.path: return

        # cellule cible actuelle dans le chemin
        target_node = self.path[self.path_index]
        target_x, target_y = node_to_position(target_node)
        target_pos = Position(target_x, target_y)

        position = Position(self.center_x, self.center_y)
        direction = target_pos - position
        distance = direction.length()

        # assez proche du point cible -> on passe au point suivant du chemin
        if distance < 2:
            self.path_index += 1

            #fin du chemin
            if self.path_index >= len(self.path):
                self.choose_random_destination() #nouvelle destination aléatoire
                return
        else:
            # On avance dans la direction de la cible
            movement = direction.normalize() * self.speed
            position += movement
            self.center_x = position.x
            self.center_y = position.y

    def update_monster(self, grid_to_pixels: Callable[[int], int]) -> None:
        if self.can_see_player():
            self.chasing_player = True

            player_cell = self.position_to_cell(
                Position(self.player.center_x, self.player.center_y)
            )
            # Si le joueur n'a pas changé de cellule, on évite de recalculer le chemin
            if not self.path or node_to_cell(self.path[-1]) != player_cell:
                self.compute_path(player_cell)
        else:
            if self.chasing_player:
                self.chasing_player = False
                self.choose_random_destination()

        self.move_along_path()
        self.update_animation()
