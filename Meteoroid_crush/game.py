import pygame

from pygame import Color
from util import load_sprite, get_random_position, print_text, load_sound, draw_text
from models import Spaceship, Meteroid

class Meteoroids:

    MIN_METEROID_DIS = 300
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        self.score = 0
        self._init_pygame()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = load_sprite("space1", False)
        self.background_game_music = load_sound("game_play_music")
        self.game_over_music = load_sound("game_over_music")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.meteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        
        for _ in range(4):
            while True:
                pos = get_random_position(self.screen)
                if pos.distance_to(self.spaceship.position) > self.MIN_METEROID_DIS:
                    break
            self.meteroids.append(Meteroid(pos, self.meteroids.append))
        

    def _get_game_objects(self):
        game_objs = [*self.meteroids, *self.bullets]

        if self.spaceship:
            game_objs.append(self.spaceship)

        return game_objs

    def _welcome_screen(self):
        welcome_message = """ PIZZA DOG """
        intro_music = load_sound("welcome_screen_music")
        intro_music.play()
        self.screen.blit(self.background, (0, 0))
        draw_text(self.screen, welcome_message, self.font,  self.WIDTH/2, self.HEIGHT/3)
        draw_text(self.screen, "Press [ENTER] To Begin", self.font,  self.WIDTH/2, (self.HEIGHT/2)+40)
            
        intro = True
        while intro:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    intro_music.stop()
                    intro = False
            pygame.display.flip()


    def game_loop(self):

        #intro_loop
        self._welcome_screen()

        self.background_game_music.play()
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
                elif is_key_pressed[pygame.K_DOWN]:
                    self.spaceship.reverse()

    def _process_game_logic(self):

        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for meteroid in self.meteroids:
                if meteroid.collides_with(self.spaceship):
                    self.spaceship.explosion_sound.play()
                    self.background_game_music.stop()
                    self.game_over_music.play()
                    self.spaceship = None
                    self.message = "Game Over... Final Score: " + str(self.score)
                    break

        for bullet in self.bullets[:]:
            for meteroid in self.meteroids[:]:
                if meteroid.collides_with(bullet):
                    meteroid_size = meteroid.size
                    if meteroid_size == 3:
                        self.score += 3 
                    elif meteroid_size == 2:
                        self.score += 2
                    else:
                        self.score += 1 
                    meteroid.explosion_sound.play()   
                    self.meteroids.remove(meteroid)
                    self.bullets.remove(bullet)
                    meteroid.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        
        if not self.meteroids and self.spaceship:
            self.message = "You Won!"
        
    def _display_score(self):
        current_score = self.font.render("Score: " + str(self.score), 1, Color("white"))
        self.screen.blit(current_score, (self.WIDTH - 10 - current_score.get_width(), 10))

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self._display_score()

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)
            
        pygame.display.flip()
        self.clock.tick(60)