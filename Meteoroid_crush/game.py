import pygame

from util import load_sprite
from models import GameObject

class Meteoroids:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space1", False)
        self.spaceship = GameObject((400, 300), load_sprite("spaceship1"), (0, 0))
        self.meteroid = GameObject((400, 300), load_sprite("AsteroidLarge"), (1, 0))


    def game_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Meteriods")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_q
            ):
                quit()

    def _process_game_logic(self):
        self.spaceship.move()
        self.meteroid.move()

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.spaceship.draw(self.screen)
        self.meteroid.draw(self.screen)
        pygame.display.flip()
        print("Collides:", self.spaceship.collides_with(self.meteroid))
    