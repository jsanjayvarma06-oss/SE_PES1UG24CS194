
"""
GameEngine: owns the basket and all falling objects.

Improved spawning:
- Random spawn interval
- Random X position within screen boundaries
- Minimum horizontal distance between consecutive objects
- Maximum number of objects on screen
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT


# ============================================================
# GAME SETTINGS
# ============================================================

# Minimum and maximum number of frames between spawns.
MIN_SPAWN_INTERVAL_FRAMES = 30
MAX_SPAWN_INTERVAL_FRAMES = 70

# Maximum number of falling objects allowed on screen.
MAX_OBJECTS = 5

# Radius of a falling object.
# Change this if your FallingObject uses a different radius.
OBJECT_RADIUS = 14

# Minimum horizontal distance between consecutive objects.
MIN_SPAWN_DISTANCE = 60

# Falling object speed.
OBJECT_SPEED = 3

# Maximum number of misses before game over.
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(
            x=WIDTH / 2,
            y=HEIGHT - 30
        )

        self.objects = []

        # Start with a random spawn delay.
        self.frames_until_spawn = random.randint(
            MIN_SPAWN_INTERVAL_FRAMES,
            MAX_SPAWN_INTERVAL_FRAMES
        )

        self.score = 0
        self.misses = 0
        self.game_over = False

    def _get_spawn_x(self):
        """
        Generate a valid X position for a new object.

        The position:
        1. Stays inside the screen.
        2. Is at least MIN_SPAWN_DISTANCE away from
           the previous object's X position.
        """

        # Object center must stay at least OBJECT_RADIUS
        # away from either edge of the screen.
        min_x = OBJECT_RADIUS
        max_x = WIDTH - OBJECT_RADIUS

        # If there are no existing objects, any valid X is okay.
        if not self.objects:
            return random.randint(min_x, max_x)

        # Get the X position of the most recently spawned object.
        previous_x = self.objects[-1].x

        # Try several random positions until we find one
        # sufficiently far away.
        for _ in range(20):
            x = random.randint(min_x, max_x)

            if abs(x - previous_x) >= MIN_SPAWN_DISTANCE:
                return x

        # Fallback:
        # If we couldn't find a suitable random position,
        # choose the side of the screen farther from the
        # previous object.
        left_distance = abs(previous_x - min_x)
        right_distance = abs(max_x - previous_x)

        if left_distance >= right_distance:
            return min_x
        else:
            return max_x

    def _spawn_object(self):
        """
        Spawn a new falling object if the screen isn't full.
        """

        # Don't spawn if the maximum number of objects
        # is already on screen.
        if len(self.objects) >= MAX_OBJECTS:
            return

        x = self._get_spawn_x()

        self.objects.append(
            FallingObject(
                x=x,
                y=-OBJECT_RADIUS,
                speed=OBJECT_SPEED
            )
        )

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        # Move basket continuously while the key is held.
        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed

        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        # Keep the entire basket inside the screen.
        half_width = self.basket.width / 2

        self.basket.x = max(
            half_width,
            min(WIDTH - half_width, self.basket.x)
        )

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()

    def update(self):
        if self.game_over:
            return

        # ====================================================
        # SPAWNING
        # ====================================================

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:

            # Only spawn if we haven't reached the limit.
            if len(self.objects) < MAX_OBJECTS:
                self._spawn_object()

            # Pick a NEW random interval for the next spawn.
            self.frames_until_spawn = random.randint(
                MIN_SPAWN_INTERVAL_FRAMES,
                MAX_SPAWN_INTERVAL_FRAMES
            )

        # ====================================================
        # UPDATE OBJECTS
        # ====================================================

        for obj in self.objects:
            obj.update()

        # ====================================================
        # CATCH DETECTION
        # ====================================================

        basket_rect = self.basket.get_rect()

        # Iterate over a copy so removing an object doesn't
        # cause the next object to be skipped.
        for obj in self.objects[:]:
            if is_caught(basket_rect, obj):
                self.score += 1
                self.objects.remove(obj)

        # ====================================================
        # MISSED OBJECTS
        # ====================================================

        missed = [
            obj
            for obj in self.objects
            if obj.is_past_bottom(HEIGHT)
        ]

        if missed:
            self.objects = [
                obj
                for obj in self.objects
                if not obj.is_past_bottom(HEIGHT)
            ]

            self.misses += len(missed)

            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.basket,
            self.objects
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Misses: {self.misses}/{MAX_MISSES}",
            (10, 36)
        )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart."
            )
