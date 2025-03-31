import pygame
import sys
import time

from src.apple import Apple
from src.player import Player
from src.screen import Screen
from src.snake import Snake


class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.screen = Screen(title="Snake Game", width=800, height=600, block_size=50)
        self.player = Player(name="Jogador")
        self.snake = Snake(
            screen=self.screen, initial_direction=pygame.K_RIGHT, initial_speed=5
        )
        self.apple = Apple(screen=self.screen)
        self.is_running = True

    def run(self):
        self.show_start_screen()

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            if self.snake.check_collision():
                self.is_running = False
                self.show_collision()
                time.sleep(0.5)  # Aguardar 0.5 segundos para mostrar a colisão
                self.show_game_over_screen()
            if self.player.level == 10:  # Supondo que o nível 10 é o objetivo
                self.is_running = False
                self.show_success_screen()
            self.clock.tick(self.snake.speed)

    def quit(self):
        self.is_running = False
        pygame.quit()
        sys.exit()

    def handle_keydown(self, key: int):
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            self.snake.change_direction(new_direction=key)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(key=event.key)

    def update(self):
        self.snake.move()

        if self.snake.body[0] == self.apple.position:
            self.snake.grow_snake()
            self.apple.position = self.apple.random_position()

        if self.snake.length % 5 == 0 and self.snake.length // 5 == self.player.level:
            self.player.increase_level()
            self.snake.increase_speed()

    def draw(self):
        self.screen.clear()
        self.screen.draw_grid()
        self.apple.draw()
        self.snake.draw()
        self.screen.update()
        
    def show_collision(self):
        self.draw()
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.clear()
        font = pygame.font.Font(None, self.screen.width // 15)
        text = font.render("Pressione SPACE para iniciar", True, (255, 255, 255))
        self.screen.surface.blit(
            text, (self.screen.width // 4, self.screen.height // 2)
        )
        self.screen.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def show_game_over_screen(self):
        self.screen.clear()
        font = pygame.font.Font(None, self.screen.width // 15)
        text = font.render("Você Perdeu!", True, (255, 0, 0))
        self.screen.surface.blit(
            text, (self.screen.width // 3, self.screen.height // 2 - 50)
        )
        text = font.render(
            "Pressione R para jogar novamente ou Q para encerrar o jogo",
            True,
            (255, 255, 255),
        )
        self.screen.surface.blit(
            text, (self.screen.width // 6, self.screen.height // 2 + 50)
        )
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()  # Reinicia o jogo
                        self.run()
                    if event.key == pygame.K_q:
                        self.quit()
                        exit()

    def show_success_screen(self):
        self.screen.clear()
        font = pygame.font.Font(None, self.screen.width // 15)
        text = font.render("Você ganhou!", True, (0, 255, 0))
        self.screen.surface.blit(
            text, (self.screen.width // 3, self.screen.height // 2 - 50)
        )
        text = font.render(
            "Pressione R para jogar novamente ou Q para encerrar o jogo",
            True,
            (255, 255, 255),
        )
        self.screen.surface.blit(
            text, (self.screen.width // 6, self.screen.height // 2 + 50)
        )
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()  # Reinicia o jogo
                        self.run()
                    if event.key == pygame.K_q:
                        self.quit()
                        exit()


if __name__ == "__main__":
    game = Game()
    game.run()
