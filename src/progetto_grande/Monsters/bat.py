import arcade
import math
import random


class Bat(arcade.TextureAnimationSprite):
    def __init__(self, animation, scale: float, center_x: float, center_y: float) -> None:
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
        #random change of direction
        self.angle += random.uniform(-0.2, 0.2)

        dx_from_center = self.center_x - self.start_x
        dy_from_center = self.center_y - self.start_y
        distance = (dx_from_center**2 + dy_from_center**2) ** 0.5

        if distance > self.range:
            # angle pointing back toward the center
            # (negative because we want the vector from current position to the center)
            angle_to_center = math.atan2(-dy_from_center, -dx_from_center)
            diff_angle = angle_to_center - self.angle
            #2*pi turn angles are avoided
            diff_angle = (diff_angle + math.pi) % (2 * math.pi) - math.pi
            self.angle += diff_angle *0.3 * (distance / self.range)

        # constant speed
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

        self.center_x += self.dx
        self.center_y += self.dy

        self.update_animation()
