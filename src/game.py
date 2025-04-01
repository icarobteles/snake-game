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

        # Inicializa os componentes do jogo via injeção de dependência
        self.screen = Screen(title="Snake Game", width=800, height=600, block_size=50)
        self.player = Player(name="Jogador")
        self.snake = Snake(screen=self.screen, initial_direction=pygame.K_RIGHT, initial_speed=5)
        self.apple = Apple(screen=self.screen)
        self.is_running = False

    def reset(self):
        self.player = Player(name="Jogador")
        self.snake = Snake(screen=self.screen, initial_direction=pygame.K_RIGHT, initial_speed=5)
        self.apple = Apple(screen=self.screen)
        self.is_running = False
        self.run(show_start_screen=False)

    def run(self, show_start_screen: bool = True):
        if show_start_screen:
            self.show_start_screen()

        self.is_running = True

        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()

            if self.snake.check_collision():
                self.show_collision()
                time.sleep(0.5)
                self.show_message_screen("Você Perdeu!", (255, 0, 0))
            if self.player.level == 10:
                self.show_message_screen("Você Ganhou!", (0, 255, 0))

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

        # Verifica se a cabeça da cobra colidiu com a maçã
        if self.snake.body[0] == self.apple.position:
            self.snake.grow_snake()

            new_position = self.apple.random_position(occupied_positions=self.snake.body)
            if new_position is None:
                self.show_message_screen("Você ganhou! Todos os quadrados preenchidos!", (0, 255, 0))
                self.quit()  # Encerra o jogo
            else:
                self.apple.position = new_position

        # A cada 5 segmentos adicionados, o nível aumenta e a velocidade da cobra aumenta
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

    def show_message_screen(self, message: str, color: tuple):
        self.screen.clear()

        font = pygame.font.Font(None, self.screen.width // 30)
        text = font.render(message, True, color)

        # Centraliza o texto na tela
        text_rect = text.get_rect(center=(self.screen.width // 2, self.screen.height // 2 - 50))
        self.screen.surface.blit(text, text_rect)

        instruction = "Pressione R para jogar novamente ou Q para encerrar o jogo"
        text2 = font.render(instruction, True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(self.screen.width // 2, self.screen.height // 2 + 50))
        self.screen.surface.blit(text2, text2_rect)

        self.screen.update()

        is_waiting = True
        while is_waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                        is_waiting = False
                    elif event.key == pygame.K_q:
                        self.quit()

    def show_start_screen(self):
        self.screen.clear()

        font = pygame.font.Font(None, self.screen.width // 30)
        text = font.render("Pressione SPACE para iniciar", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.width // 2, self.screen.height // 2))
        self.screen.surface.blit(text, text_rect)
        self.screen.update()

        is_waiting = True
        while is_waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_waiting = False

    def show_game_over_screen(self):
        self.screen.clear()
        font = pygame.font.Font(None, self.screen.width // 15)
        text = font.render("Você Perdeu!", True, (255, 0, 0))
        self.screen.surface.blit(text, (self.screen.width // 3, self.screen.height // 2 - 50))
        text = font.render(
            "Pressione R para jogar novamente ou Q para encerrar o jogo",
            True,
            (255, 255, 255),
        )
        self.screen.surface.blit(text, (self.screen.width // 6, self.screen.height // 2 + 50))
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
        self.screen.surface.blit(text, (self.screen.width // 3, self.screen.height // 2 - 50))
        text = font.render(
            "Pressione R para jogar novamente ou Q para encerrar o jogo",
            True,
            (255, 255, 255),
        )
        self.screen.surface.blit(text, (self.screen.width // 6, self.screen.height // 2 + 50))
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
