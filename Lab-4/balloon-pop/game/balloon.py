"""
Balloon: falls from the top of the screen.
"""

import pygame


class Balloon:
    def __init__(self, x, y, radius, speed, color=(220, 90, 120),
                 balloon_type="normal", points=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.balloon_type = balloon_type
        self.points = points

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )