import pygame
from circleshape import CircleShape
from constants import *
from sound_manager import SoundManager
import random

class Asteroid(CircleShape):
    enemy_images = [
        pygame.image.load('assets/images/enemy4.png'),
        pygame.image.load('assets/images/enemy3.png'),
        pygame.image.load('assets/images/enemy2.png'),
        pygame.image.load('assets/images/enemy.png') 
    ]
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
        self.velocity = pygame.Vector2(1,1)
        self.sound_manager = SoundManager()
        self.sound_manager.load_sound('pop', 'assets/sounds/asteroid_pop.wav')
        
        self.random_image = random.choice(self.enemy_images)
        self.enemy_image = pygame.transform.scale(self.random_image, (int(radius * 2), int(radius * 2)))
        self.rect = self.enemy_image.get_rect()
        self.rect.center = (x,y)
    
    def draw(self, screen):
        #pygame.draw.circle(screen, "white", self.position, self.radius,2)
        #pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.radius, 2)
        screen.blit(self.enemy_image, self.rect)
        
    def update(self, dt):
        self.position += self.velocity * dt
        
        self.rect.center = self.position
    
    def split(self):
        self.kill()
        self.sound_manager.play_sound('pop')
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        split_angle = random.uniform(20,50)
        
        velocity1 = self.velocity.rotate(split_angle)
        velocity2 = self.velocity.rotate(-split_angle)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        
        new_asteroid1.velocity = velocity1*1.2
        new_asteroid2.velocity = velocity2*1.2
        
        