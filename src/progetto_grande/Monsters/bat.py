from collections.abc import Callable
import arcade
import math
import random
from progetto_grande.Monsters.monster import Monster
from progetto_grande.map import Map
from progetto_grande.constants import SCALE
from progetto_grande.textures import ANIMATION_BAT

BatList = arcade.SpriteList["Bat"]

class Bat(Monster):
    def __init__(self, animation: arcade.TextureAnimation, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(
            animation=animation,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
        )
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed, self.range = 2.5, 100
        self.start_x, self.start_y = center_x, center_y

    def update_bat(self) -> None:
        # Le mouvement est basé sur des coordonnées polaires:
        # le centre de référence est la position initiale sur la carte

        # Le mouvement est semi-aléatoire:
        # à chaque frame, on modifie l'angle pour créer une trajectoire irrégulière
        self.angle += random.uniform(-0.2, 0.2)

        # On calcule la distance actuelle par rapport au point de départ
        dx_from_center = self.center_x - self.start_x
        dy_from_center = self.center_y - self.start_y
        distance = (dx_from_center**2 + dy_from_center**2) ** 0.5

        # Si la chauve-souris dépasse son rayon de déplacement,
        # on la réoriente vers son point d'origine
        if distance > self.range:

            # Angle vers le centre (vecteur opposé à la position actuelle)
            angle_to_center = math.atan2(-dy_from_center, -dx_from_center)

            # Différence entre l’angle actuel et la direction vers le centre
            # On évite des rotations inutiles de 2π
            diff_angle = angle_to_center - self.angle
            diff_angle = (diff_angle + math.pi) % (2 * math.pi) - math.pi

            #On ajouste la direction
            self.angle += diff_angle *0.3 * (distance / self.range)

        # Mouvement avec vitesse constante
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

        self.center_x += self.dx
        self.center_y += self.dy

        self.update_animation()

    def update_monster(self, grid_to_pixels: Callable[[int], int]) -> None:
        self.update_bat()
