import pygame


class Screen:
    def __init__(self, title: str, width: int, height: int, block_size: int = 20):
        self.title = title
        self.width = width
        self.height = height
        self.block_size = block_size

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def clear(self):
        self.surface.fill((0, 0, 0))

    def update(self):
        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, self.width, self.block_size):
            pygame.draw.line(self.surface, (40, 40, 40), (x, 0), (x, self.height))

        for y in range(0, self.height, self.block_size):
            pygame.draw.line(self.surface, (40, 40, 40), (0, y), (self.width, y))
