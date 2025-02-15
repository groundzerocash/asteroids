import pygame
from circleshape import CircleShape
from constants import *
from sound_manager import SoundManager
from asteroid import Asteroid

class Boss(Asteroid):
    boss_image = pygame.image.load('assets/images/boss.png')
    def __init__(self, x, y):
        super().__init__(x, y, ASTEROID_MAX_RADIUS * 1.5)
        self.velocity = pygame.Vector2(0,0)
        self.sound_manager = SoundManager()

        self.boss_image = pygame.transform.scale(self.boss_image, (int(ASTEROID_MAX_RADIUS *1.5*2), int(ASTEROID_MAX_RADIUS *1.5*2)))
        self.rect = self.boss_image.get_rect()
        self.rect.center = (x,y)
        self.health = BOSS_HEALTH
        
    def draw(self,screen):
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, ASTEROID_MAX_RADIUS *1.5, 2)
        screen.blit(self.boss_image,self.rect)
    
    def update(self, dt, player):
        self.direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        if self.direction.length() > 1:
            self.direction = self.direction.normalize()
            self.velocity = self.direction * 50

        self.position += self.velocity * dt
        self.rect.center = self.position
        
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
        
    
    