import pygame
import random

from src.screen import Screen


class Apple:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.position = self.random_position(occupied_positions=[])

    def random_position(self, occupied_positions: list):
        # Calcula o número de células horizontal e verticalmente
        x_cells = self.screen.width // self.screen.block_size
        y_cells = self.screen.height // self.screen.block_size

        # Cria uma lista com todas as posições possíveis no grid
        all_positions = [
            (x * self.screen.block_size, y * self.screen.block_size) for x in range(x_cells) for y in range(y_cells)
        ]

        # Filtra as posições que não estão ocupadas
        free_positions = [pos for pos in all_positions if pos not in occupied_positions]

        if not free_positions:
            return None

        return random.choice(free_positions)

    def draw(self):
        if self.position is not None:
            rect = (*self.position, self.screen.block_size, self.screen.block_size)
            pygame.draw.rect(self.screen.surface, (255, 0, 0), rect)
