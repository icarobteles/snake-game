import pygame

from src.screen import Screen


class Snake:
    def __init__(self, screen: Screen, initial_direction: int, initial_speed: int):
        self.screen = screen
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = initial_direction
        self.speed = initial_speed
        self.grow = False

    @property
    def length(self) -> int:
        return len(self.body)

    def move(self):
        head_x, head_y = self.body[0]

        if self.direction == pygame.K_UP:
            new_head = (head_x, head_y - self.screen.block_size)
        elif self.direction == pygame.K_DOWN:
            new_head = (head_x, head_y + self.screen.block_size)
        elif self.direction == pygame.K_LEFT:
            new_head = (head_x - self.screen.block_size, head_y)
        elif self.direction == pygame.K_RIGHT:
            new_head = (head_x + self.screen.block_size, head_y)
        else:
            new_head = (head_x, head_y)

        # Atualiza o corpo da cobra: a nova cabeça é adicionada e a cauda é removida
        self.body = [new_head] + self.body[:-1]

        # Se a cobra deve crescer, adiciona um segmento extra
        if self.grow:
            self.body.append(self.body[-1])
            self.grow = False

    def change_direction(self, new_direction: int):
        opposite_directions = {
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT,
        }

        if new_direction in opposite_directions and new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def draw(self):
        head_color = (0, 200, 0)
        body_color = (0, 255, 0)
        for index, segment in enumerate(self.body):
            color = head_color if index == 0 else body_color
            rect = (*segment, self.screen.block_size, self.screen.block_size)
            pygame.draw.rect(self.screen.surface, color, rect)

    # Sinaliza que a cobra deve crescer na próxima atualização.
    def grow_snake(self):
        self.grow = True

    # Incrementa a velocidade da cobra.
    def increase_speed(self):
        self.speed += 1

    # Verifica se a cobra colidiu com as bordas ou com ela mesma.
    def check_collision(self):
        head_x, head_y = self.body[0]
        
        # Verificar colisão com as bordas
        if head_x < 0 or head_x >= self.screen.width or head_y < 0 or head_y >= self.screen.height:
            return True
        
        # Verificar colisão com o próprio corpo
        if (head_x, head_y) in self.body[1:]:
            return True
        return False
