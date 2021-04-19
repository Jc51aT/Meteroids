from pygame.math import  Vector2
from pygame.transform import rotozoom

from util import load_sprite, wrap_position, get_random_velocity, load_sound

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_pos = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_pos)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Spaceship(GameObject):
    MANEUVERABILITY = 10
    ACCELERATION = 0.33
    BULLET_SPEED = 3

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound('laser')
        self.explosion_sound = load_sound("crush")
        self.direction = Vector2(UP)
        super().__init__(position, rotozoom(load_sprite("spaceship"), 0, 0.5), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        if self.velocity.y > -1.5:
            self.velocity += self.direction * self.ACCELERATION
        print(self.velocity.y)

    def reverse(self):
        if self.velocity.y < 1:
            self.velocity -= self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class Meteroid(GameObject):

    def __init__(self, position, create_meteroid_callback, size=3):
        self.size = size
        self.create_meteroid_callback = create_meteroid_callback
        self.explosion_sound = load_sound("meteriod_explo")
        self.explosion_sound.set_volume(100)

        size_to_scale = {
            3:.66,
            2:0.44,
            1:0.25
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("meteroid"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1,3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                meteroid = Meteroid(self.position, self.create_meteroid_callback, self.size - 1)
                self.create_meteroid_callback(meteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, rotozoom(load_sprite("pizza"), 0, 0.5), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity