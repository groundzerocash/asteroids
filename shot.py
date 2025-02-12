from circleshape import CircleShape
import pygame
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.original_image = pygame.image.load('assets/images/arrow.png')
        self.arrow_image = self.original_image
        self.rect = self.arrow_image.get_rect()
        self.rect.center = (x,y)

    def draw(self, screen):
        #pygame.draw.circle(screen, "white", self.position, self.radius,2)
        screen.blit(self.arrow_image, self.rect)
    
    def update(self, dt):
        self.position += self.velocity * dt
        
        self.rect.center = self.position