
"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


# Boost configuration
BOOST_DURATION_FRAMES = 180   # 3 seconds at 60 FPS
BOOST_COOLDOWN_FRAMES = 300   # 5 seconds at 60 FPS


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Normal movement speed
        self.speed = speed

        # Speed boost settings
        self.boosted_frames = 0
        self.normal_speed = speed
        self.boost_speed = speed * 2

        # Cooldown prevents the boost from being spammed
        self.boost_cooldown_frames = 0

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

    def activate_boost(self):
        """
        Activate the speed boost if it isn't already active
        and the cooldown has expired.
        """
        if self.boosted_frames > 0:
            return False

        if self.boost_cooldown_frames > 0:
            return False

        self.boosted_frames = BOOST_DURATION_FRAMES
        self.speed = self.boost_speed

        return True

    def update_boost(self):
        """
        Update the boost timer and automatically restore
        normal speed when the boost expires.
        """

        # Update boost
        if self.boosted_frames > 0:
            self.boosted_frames -= 1

            if self.boosted_frames <= 0:
                self.boosted_frames = 0
                self.speed = self.normal_speed

                # Start cooldown when boost expires
                self.boost_cooldown_frames = BOOST_COOLDOWN_FRAMES

        # Update cooldown
        if self.boost_cooldown_frames > 0:
            self.boost_cooldown_frames -= 1

    def is_boost_active(self):
        """Return True while the speed boost is active."""
        return self.boosted_frames > 0

    def get_boost_seconds(self):
        """Return remaining boost time in seconds."""
        return self.boosted_frames / 60
