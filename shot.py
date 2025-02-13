from circleshape import CircleShape
import pygame
from constants import SHOT_RADIUS

class Shot(CircleShape):
    shot_image = pygame.image.load('assets/images/arrow.png')
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        
        self.shot_image = pygame.transform.scale(self.shot_image, (int(SHOT_RADIUS*2), int(SHOT_RADIUS*2)))
        self.rect = self.shot_image.get_rect()
        self.rect.center = (x,y)

    def draw(self, screen):
        #pygame.draw.circle(screen, "white", self.position, self.radius,2)
        screen.blit(self.shot_image, self.rect)
    
    def update(self, dt):
        self.position += self.velocity * dt
        
        self.rect.center = self.position