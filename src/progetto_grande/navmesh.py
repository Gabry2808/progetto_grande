import networkx as nx
import math
from progetto_grande.map import GridCell, Map
from progetto_grande.constants import TILE_SIZE

NODES_PER_CELL = 3

Cell = tuple[int, int]
Node = tuple[int, int]
Position = tuple[float, float]

# ============= Cell Helpers =============
def all_cells(game_map: Map) -> list[Cell]:
    return [
        (x, y)
        for x in range(game_map.width)
        for y in range(game_map.height)
    ]

def walkable_cells(game_map: Map) -> list[Cell]:
    return [
        cell for cell in all_cells(game_map)
        if game_map.is_walkable(cell)
    ]

def bush_centers(game_map: Map) -> list[Position]:
    return [
        (
            x * TILE_SIZE + TILE_SIZE / 2,
            y * TILE_SIZE + TILE_SIZE / 2,
        )
        for (x, y) in all_cells(game_map)
        if game_map.get(x, y) == GridCell.BUSH
    ]

# ============= Node creation / filtering =============
def nodes_in_cell(cell: Cell) -> list[Node]:
    cell_x, cell_y = cell
    return [
        (
            cell_x * NODES_PER_CELL + i,
            cell_y * NODES_PER_CELL + j,
        )
        for i in range(NODES_PER_CELL)
        for j in range(NODES_PER_CELL)
    ]

def node_too_close_to_bush(node: Node, bushes: list[Position]) -> bool:
    node_x, node_y = node_to_position(node)

    return any(
        math.sqrt((node_x - bx) ** 2 + (node_y - by) ** 2) < TILE_SIZE
        for bx, by in bushes
    )

def all_nodes(game_map: Map) -> list[Node]:
    bushes = bush_centers(game_map)

    return [
        node
        for cell in walkable_cells(game_map)
        for node in nodes_in_cell(cell)
        if not node_too_close_to_bush(node, bushes)
    ]


# ============= Node Convertion =============
def node_to_cell(node: Node) -> Cell:
    return (
        node[0] // NODES_PER_CELL,
        node[1] // NODES_PER_CELL,
    )

def node_to_position(node: Node) -> Position:
    step = TILE_SIZE / NODES_PER_CELL

    cell_coords = tuple(n // NODES_PER_CELL for n in node)
    local_coords = tuple(n % NODES_PER_CELL for n in node)

    # - cell_coord * TILE_SIZE → position de l'origine de la cellule
    # - local_coord * step     → déplacement à l'intérieur de la cellule
    # - + step / 2             → centre du petit carré, pas son bord
    #
    # Donc : position = cell_coord * TILE_SIZE + (local_coord + 0.5) * step
    return tuple(
        cell_coord * TILE_SIZE + step * (local_coord + 0.5)
        for cell_coord, local_coord in zip(cell_coords, local_coords)
    )


# ============= Distance Helpers =============
def distance(p1: Position, p2: Position) -> float:
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def distance_between_nodes(node1: Node, node2: Node) -> float:
    return distance(node_to_position(node1), node_to_position(node2))

def distance_position_to_node(position: Position, node: Node) -> float:
    return distance(position, node_to_position(node))

def closest_node(graph: nx.Graph[Node], position: Position) -> Node:
    return min(
        graph.nodes,
        key=lambda node: distance_position_to_node(position, node),
    )

# ============= Graph =============
def forward_neighbor_nodes(node: Node) -> list[Node]:
    x, y = node
    return [
        (x + 1, y),
        (x, y + 1),
        (x + 1, y + 1),
        (x + 1, y - 1),
    ]

def is_diagonal_between_cells(cell: Cell, neighbor_cell: Cell) -> bool:
    return cell[0] != neighbor_cell[0] and cell[1] != neighbor_cell[1]

def adjacent_cells_for_diagonal(cell: Cell, neighbor_cell: Cell) -> tuple[Cell, Cell]:
    dx = neighbor_cell[0] - cell[0]
    dy = neighbor_cell[1] - cell[1]

    return (
        (cell[0] + dx, cell[1]),
        (cell[0], cell[1] + dy),
    )

def can_connect(game_map: Map, node: Node, neighbor: Node) -> bool:
    cell = node_to_cell(node)
    neighbor_cell = node_to_cell(neighbor)

    # Pas une diagonale entre cellule -> Pas de problem
    if not is_diagonal_between_cells(cell, neighbor_cell): return True

    cell1, cell2 = adjacent_cells_for_diagonal(cell, neighbor_cell)

    # On empêche les diagonales qui coupent les coins
    return game_map.is_walkable(cell1) and game_map.is_walkable(cell2)


# ============= Others Functions =============
def valid_neighbors(
    game_map: Map,
    node: Node,
    nodes: set[Node],
) -> list[Node]:
    return [
        neighbor
        for neighbor in forward_neighbor_nodes(node)
        if neighbor in nodes and can_connect(game_map, node, neighbor)
    ]

def build_navmesh(game_map: Map) -> nx.Graph[Node]:
    graph: nx.Graph[Node] = nx.Graph()
    nodes = set(all_nodes(game_map))

    for node in nodes:
        for neighbor in valid_neighbors(game_map, node, nodes):
            graph.add_edge(
                node,
                neighbor,
                weight=distance_between_nodes(node, neighbor),
            )
    return graph

def shortest_path(graph: nx.Graph[Node], start: Node, target: Node) -> list[Node]:
    return nx.shortest_path(graph, source=start, target=target, weight="weight")
