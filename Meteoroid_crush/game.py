import pygame

from util import load_sprite, get_random_position
from models import Spaceship, Meteroid

class Meteoroids:

    MIN_METEROID_DIS = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space1", False)
        self.clock = pygame.time.Clock()
        self.meteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        
        for _ in range(3):
            while True:
                pos = get_random_position(self.screen)
                if pos.distance_to(self.spaceship.position) > self.MIN_METEROID_DIS:
                    break
            self.meteroids.append(Meteroid(pos))
        

    def _get_game_objects(self):
        game_objs = [*self.meteroids, *self.bullets]

        if self.spaceship:
            game_objs.append(self.spaceship)

        return game_objs

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
            elif(
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key  == pygame.K_SPACE
            ):
                self.spaceship.shoot()

            is_key_pressed = pygame.key.get_pressed()
            
            if self.spaceship:
                if is_key_pressed[pygame.K_RIGHT]:
                    self.spaceship.rotate(clockwise=True)
                elif is_key_pressed[pygame.K_LEFT]:
                    self.spaceship.rotate(clockwise=False)

                if is_key_pressed[pygame.K_UP]:
                    self.spaceship.accelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for meteroid in self.meteroids:
                if meteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    break

        for bullet in self.bullets[:]:
            for meteroid in self.meteroids[:]:
                if meteroid.collides_with(bullet):
                    self.meteroids.remove(meteroid)
                    self.bullets.remove(bullet)
                    break
                
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        
        

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)