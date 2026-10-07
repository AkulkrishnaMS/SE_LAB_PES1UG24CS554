"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom. Balloons vary in size - this matters for
how click detection should work.
"""

import pygame
import random

# Define the properties for each balloon type (Color as RGB tuples)
BALLOON_TYPES = {
    "Normal": {"color": (220, 90, 120), "points": 10},      # Default red/pink
    "Bonus": {"color": (255, 215, 0), "points": 50},        # Gold
    "Penalty": {"color": (0, 0, 0), "points": -20}          # Black
}

class Balloon:
    def __init__(self, x, y, radius, speed, balloon_type=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        
        # Randomly select a type if one isn't provided
        if balloon_type is None:
            self.balloon_type = random.choices(
                ["Normal", "Bonus", "Penalty"], 
                weights=[70, 15, 15], 
                k=1
            )[0]
        else:
            self.balloon_type = balloon_type
            
        # Apply the correct color and point value based on the type
        properties = BALLOON_TYPES[self.balloon_type]
        self.color = properties["color"]
        self.points = properties["points"]

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )