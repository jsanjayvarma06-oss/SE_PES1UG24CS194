
"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Normal movement speed
        self.speed = speed

        # Speed boost support
        self.boosted_frames = 0
        self.normal_speed = speed
        self.boost_speed = speed

    def get_rect(self):
        """
        Return the pygame rectangle representing the basket.

        self.x and self.y represent the CENTER of the basket.
        """
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )
