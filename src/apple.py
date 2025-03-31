import pygame
import random

from src.screen import Screen


class Apple:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.position = self.random_position()

    def random_position(self):
        x_min = 0
        x_max = (self.screen.width // self.screen.block_size) - 1
        x = random.randint(x_min, x_max) * self.screen.block_size

        y_min = 0
        y_max = (self.screen.height // self.screen.block_size) - 1
        y = random.randint(y_min, y_max) * self.screen.block_size

        return (x, y)

    def draw(self):
        pygame.draw.rect(
            self.screen.surface,
            (255, 0, 0),
            (*self.position, self.screen.block_size, self.screen.block_size),
        )
