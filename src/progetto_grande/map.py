from tkinter import HORIZONTAL
from arcade.examples.happy_face import height
import signal
from enum import Enum
from typing import Final

class GridCell(Enum):
    GRASS = 0
    BUSH = 1
    CRYSTAL = 2

class SpinnerMove(Enum):
    HORIZONTAL = 3
    VERTICAL = 4


class Spinner:
    def __init__(self, x: int, y: int , move : SpinnerMove) -> None :
        self.x : Final[int]=x
        self.y :Final[int]=y
        self.move :Final[SpinnerMove] = move

class Map:
    def __init__(
    self,
    width: int,
    height: int,
    grid: list[list[GridCell]],
    player_start_x: int,
    player_start_y: int,

    spinners : list[Spinner],

) -> None:
        self.width: Final[int] = width
        self.height: Final[int] = height
        self.player_start_x: Final[int] = player_start_x
        self.player_start_y: Final[int] = player_start_y
        self._grid: Final[list[list[GridCell]]] = grid

        self.spinners: Final[list[Spinner]]= spinners

    def get(self, x: int, y: int) -> GridCell:
        if x < 0 or x >= self.width:
            raise IndexError("x out of bounds")
        if y < 0 or y >= self.height:
            raise IndexError("y out of bounds")

        return self._grid[y][x]

# Exception utilisée lorsque le fichier de la carte contient une erreur
class InvalidMapFileException(Exception):
    pass

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

# Buissons
for x, y in [(3, 6), (7, 2), (2, 10), (3, 8)]:
    grid_decouverte[y][x] = GridCell.BUSH

# Cristaux
for x, y in [(5, 2), (6, 5), (3, 5)]:
    grid_decouverte[y][x] = GridCell.CRYSTAL

"""
MAP_DECOUVERTE = Map(
    width=40,
    height=20,
    grid=grid_decouverte,
    player_start_x=2,
    player_start_y=2,
)
"""

# Correspondance entre les caractères du fichier de carte et les types de cellule
# ' ' -> GRASS
# 'x' -> BUSH
# '*' -> CRYSTAL
# 's' -> spinner horizontal (géré plus tard)
# 'S' -> spinner vertical (géré plus tard)
# 'P' -> position de départ du joueur



def ligne_taille_en_entier (l: str, key_attendu: str) -> int:
     "tranforme les lignes de longeur/largeur(key) en entier(val) et leve les exceptions"
     new_l = l.split(":", 1)
     if len(new_l) != 2:
        raise InvalidMapFileException(f"la ligne {l} est invalide pour les tailles")
     key =new_l[0].strip()
     val_entiere = new_l[1].strip()

     if key != key_attendu:
        raise InvalidMapFileException(f"cle attendue : {key_attendu} differente de cle recu : {key} ")
     try:
        val = int(val_entiere)
     except ValueError as VE :
        raise InvalidMapFileException(f"mauvaise valeur entiere pour {key_attendu}: {val_entiere}") from VE

     if val <= 0:
        raise InvalidMapFileException(f"valeur {key_attendu} negative c'est une erreur ")

     return val


def caract_en_cell (c: str) -> GridCell :
     "transforme un caractere du fichier en grid et leve les exceptions"
     if (c == " " ) or (c== "P") or (c=="s") or (c== "S") :
        return GridCell.GRASS
     if c == "x":
        return GridCell.BUSH
     if c == "*":
        return GridCell.CRYSTAL

     raise InvalidMapFileException (f"Le caractere {c} n'est pas valide")

def charger_map (lignes: list[str]) -> Map:
     "charger la map a partir des LIGNES d'un fichier et lever les exeptions"
     if len(lignes)< 5:
        raise InvalidMapFileException("Mauvais format : pas assez de lignes")

     lignes= [ ligne.rstrip("\n")for ligne in lignes  ]

     new_width= ligne_taille_en_entier(lignes[0],"width")
     new_height= ligne_taille_en_entier(lignes[1], "height")

     if lignes[2] != "---" :
        raise InvalidMapFileException("On attend '---' apres les tailles")

     map_lignes = lignes[3:3 + new_height]   #on coupe la liste lignes pour pouvoir compter le nombre de ligne
     if len(map_lignes) != new_height:
        raise InvalidMapFileException("Le nombre de lignes de la carte est incorrect")

     derniere_ligne = 3 + new_height

     if derniere_ligne >= len(lignes) or lignes[derniere_ligne] != "---":
        raise InvalidMapFileException("Il manque la derniere ligne : '---' ")

     new_grid : list[list[GridCell]]
     new_grid=[]
     new_player_start_x= -1
     new_player_start_y= -1

     new_spinners: list[Spinner]
     new_spinners = []

     for num_ligne_fichier, ligne in enumerate(map_lignes):
        if len(ligne)>new_width:
            raise InvalidMapFileException("La ligne est trop longue")

        ligne_complete = ligne.ljust(new_width)
        row: list[GridCell]
        row = []
        for x, char in enumerate(ligne_complete) :
            y= new_height - 1 - num_ligne_fichier

            if char == "P":
                if new_player_start_x != - 1:
                    raise InvalidMapFileException("Trop de joueurs sur votre map")
                new_player_start_x = x
                new_player_start_y = y
            if char == "s":
                new_spinners.append(Spinner(x,y, SpinnerMove.HORIZONTAL))
            if char == "S":
                new_spinners.append(Spinner(x,y, SpinnerMove.VERTICAL))

            row.append(caract_en_cell(char))

        new_grid.append(row)
     new_grid.reverse()

     if new_player_start_x == -1 :
        raise InvalidMapFileException("Joueur hors map")

     return Map( new_width, new_height , new_grid, new_player_start_x, new_player_start_y , new_spinners )

def charger_map_dun_fichier( nom_fichier: str) -> Map :
    try:
        with open(nom_fichier,"r", encoding="utf-8" ) as f:
            lignes = f.readlines()
    except OSError as e :
        raise InvalidMapFileException(f"Fichier {nom_fichier} impossible a lire") from e
    return charger_map(lignes)

def limites_spinner (map: Map, spinner: Spinner) -> tuple :
    x=spinner.x
    y=spinner.y

    if spinner.move == SpinnerMove.HORIZONTAL:
        left=x
        while left - 1 >= 0 and map.get(left - 1, y) !=GridCell.BUSH:
            left = left -1

        right= x
        while right + 1 < map.width and map.get(right +1, y) != GridCell.BUSH:
            right = right + 1
        return (left, right)

    bottom = y
    while bottom - 1 >= 0 and map.get(x, bottom -1) != GridCell.BUSH:
        bottom = bottom -1

    top = y
    while top + 1 < map.height and map.get(x, top +1) != GridCell.BUSH :
        top = top +1
    return (bottom, top)

MAP_DECOUVERTE = charger_map_dun_fichier("maps/map1.txt")
