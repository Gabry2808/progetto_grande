from enum import Enum
from typing import Final

class GridCell(Enum):
    GRASS = 0
    BUSH = 1
    CRYSTAL = 2


class Map:
    def __init__(
    self,
    width: int,
    height: int,
    grid: list[list[GridCell]],
    player_start_x: int,
    player_start_y: int,
) -> None:
        self.width: Final[int] = width
        self.height: Final[int] = height
        self.player_start_x: Final[int] = player_start_x
        self.player_start_y: Final[int] = player_start_y
        self._grid: Final[list[list[GridCell]]] = grid

    def get(self, x: int, y: int) -> GridCell:
        if x < 0 or x >= self.width:
            raise IndexError("x out of bounds")
        if y < 0 or y >= self.height:
            raise IndexError("y out of bounds")

        return self._grid[y][x]

# Création d'une grille remplie d'herbe
grid_decouverte = [
    [GridCell.GRASS for _ in range(40)]
    for _ in range(20)
]

# Bords de la carte
for x in range(40):
    grid_decouverte[0][x] = GridCell.BUSH # Ligne du bas (y = 0)
    grid_decouverte[19][x] = GridCell.BUSH # Ligne du haut (y = 19)

for y in range(20):
    grid_decouverte[y][0] = GridCell.BUSH # Colonne de gauche (x = 0)
    grid_decouverte[y][39] = GridCell.BUSH # Colonne de droite (x = 39)

# Buissons à l'intérieur de la carte
for x, y in [(3, 6), (7, 2), (2, 10), (3, 8)]:
    grid_decouverte[y][x] = GridCell.BUSH

# Cristaux
for x, y in [(5, 2), (6, 5), (3, 5)]:
    grid_decouverte[y][x] = GridCell.CRYSTAL


MAP_DECOUVERTE = Map(
    width=40,
    height=20,
    grid=grid_decouverte,
    player_start_x=2,
    player_start_y=2,
)
