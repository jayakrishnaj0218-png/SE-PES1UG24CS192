
"""
GameEngine: manages balloons, scoring, lives and timer.
"""

import random
import pygame

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
STARTING_LIVES = 3
GAME_DURATION = 30


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES
        self.time_left = GAME_DURATION
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)

        balloon_type = random.choices(
            ["normal", "bonus", "penalty"],
            weights=[60, 20, 20]
        )[0]

        if balloon_type == "normal":
            color, points = (220, 90, 120), 10
        elif balloon_type == "bonus":
            color, points = (255, 215, 0), 30
        else:
            color, points = (50, 150, 255), -20

        self.balloons.append(
            Balloon(
                x=x, y=-radius, radius=radius, speed=speed,
                color=color, balloon_type=balloon_type, points=points
            )
        )

    def handle_click(self, pos):
        if self.game_over:
            return

        popped = check_pop(self.balloons, pos)

        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        if self.game_over:
            return

        elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.time_left = max(0, GAME_DURATION - elapsed)

        if self.time_left <= 0:
            self.game_over = True
            self.balloons.clear()
            return

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for balloon in self.balloons:
            balloon.update()

        remaining_balloons = []

        for balloon in self.balloons:
            if balloon.is_past_bottom(HEIGHT):
                self.lives -= 1
            else:
                remaining_balloons.append(balloon)

        self.balloons = remaining_balloons

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True
            self.balloons.clear()

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.balloons)

        renderer.draw_text(
            surface, font, f"Score: {self.score}", (10, 10)
        )
        renderer.draw_text(
            surface, font, f"Lives: {self.lives}", (10, 40)
        )
        renderer.draw_text(
            surface, font, f"Time: {self.time_left}", (10, 70)
        )

        if self.game_over:
            renderer.draw_banner(
                surface, font,
                f"GAME OVER! Final Score: {self.score} - Press R to Restart"
            )
