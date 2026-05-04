import math
from progetto_grande.map import charger_map
from progetto_grande.navmesh import (
    build_navmesh,
    closest_node,
    distance_between_nodes,
    nodes_in_cell,
    shortest_path,
)

def test_navmesh_contains_nodes_for_walkable_cells() -> None:
    game_map = charger_map([
        "width: 3",
        "height: 3",
        "---",
        "   ",
        " P ",
        "   ",
        "---",
    ])
    graph = build_navmesh(game_map)

    for node in nodes_in_cell((1, 1)):
        assert node in graph.nodes

def test_navmesh_connects_neighbor_nodes() -> None:
    game_map = charger_map([
        "width: 3",
        "height: 3",
        "---",
        "   ",
        " P ",
        "   ",
        "---",
    ])
    graph = build_navmesh(game_map)
    nodes = nodes_in_cell((1, 1))

    assert graph.has_edge(nodes[0], nodes[1])

def test_closest_node() -> None:
    lines = [
        "width: 3",
        "height: 3",
        "---",
        "   ",
        " P ",
        "   ",
        "---",
    ]

    game_map = charger_map(lines)
    graph = build_navmesh(game_map)

    node = closest_node(graph, (48.0, 48.0))

    assert node in graph.nodes

def test_shortest_path_between_nodes() -> None:
    game_map = charger_map([
        "width: 3",
        "height: 3",
        "---",
        "   ",
        " P ",
        "   ",
        "---",
    ])

    graph = build_navmesh(game_map)

    start = nodes_in_cell((0, 0))[0]
    target = nodes_in_cell((2, 2))[-1]

    path = shortest_path(graph, start, target)

    assert path[0] == start
    assert path[-1] == target

def test_navmesh_avoids_obstacles() -> None:
    game_map = charger_map([
        "width: 3",
        "height: 3",
        "---",
        "   ",
        "Px ",
        "   ",
        "---",
    ])
    graph = build_navmesh(game_map)

    start = closest_node(graph, (16.0, 48.0))
    target = closest_node(graph, (80.0, 48.0))

    path = shortest_path(graph, start, target)

    for node in nodes_in_cell((1, 1)):
        assert node not in path

def test_navmesh_connects_diagonal_nodes() -> None:
    lines = [
        "width: 3",
        "height: 3",
        "---",
        "   ",
        " P ",
        "   ",
        "---",
    ]
    game_map = charger_map(lines)
    graph = build_navmesh(game_map)
    center_node = nodes_in_cell((1, 1))[4]
    diagonal_node = nodes_in_cell((1, 1))[8]

    assert graph.has_edge(center_node, diagonal_node)

def test_navmesh_diagonal_weight() -> None:
    lines = [
        "width: 3",
        "height: 3",
        "---",
        "   ",
        " P ",
        "   ",
        "---",
    ]
    game_map = charger_map(lines)
    graph = build_navmesh(game_map)

    node = nodes_in_cell((1, 1))[4]
    diagonal = nodes_in_cell((1, 1))[8]
    horizontal = nodes_in_cell((1, 1))[5]

    assert abs(graph[node][diagonal]["weight"] - distance_between_nodes(node, diagonal)) < 1e-6
    assert abs(graph[node][horizontal]["weight"] - distance_between_nodes(node, horizontal)) < 1e-6

def test_shortest_path_uses_diagonal_when_shorter() -> None:
    lines = [
        "width: 3",
        "height: 3",
        "---",
        "   ",
        " P ",
        "   ",
        "---",
    ]
    game_map = charger_map(lines)
    graph = build_navmesh(game_map)
    start = closest_node(graph, (16.0, 16.0))
    target = closest_node(graph, (80.0, 80.0))

    path = shortest_path(graph, start, target)

    assert path[0] == start
    assert path[-1] == target
    assert len(path) < 10

def test_shortest_path_avoids_obstacle_with_diagonals() -> None:
    lines = [
        "width: 3",
        "height: 3",
        "---",
        "   ",
        "Px ",
        "   ",
        "---",
    ]
    game_map = charger_map(lines)
    graph = build_navmesh(game_map)

    start = closest_node(graph, (16.0, 48.0))
    target = closest_node(graph, (80.0, 48.0))
    path = shortest_path(graph, start, target)

    for node in nodes_in_cell((1, 1)):
        assert node not in path

    assert path[0] == start
    assert path[-1] == target

def test_navmesh_blocks_diagonal_through_corner() -> None:
    game_map = charger_map([
        "width: 3",
        "height: 3",
        "---",
        "x x",
        " P ",
        "   ",
        "---",
    ])
    graph = build_navmesh(game_map)

    center = nodes_in_cell((1, 1))[4]
    diag = nodes_in_cell((0, 2))[4]

    assert not graph.has_edge(center, diag)
