from constants import *#PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED
from circleshape import CircleShape
from shot import Shot
from sound_manager import SoundManager
import pygame

class Player(CircleShape):
    def __init__(self, x, y):
        player_image = pygame.image.load('assets/images/bow.png')
        super().__init__(x, y, PLAYER_RADIUS)

        self.rotation = 0
        self.timer = 0 # shot cooldown timer
        
        self.sound_manager = SoundManager()
        
        self.sound_manager.load_sound("shoot", "assets/sounds/laser.flac") 
        self.original_image = pygame.transform.scale(player_image, (int(PLAYER_RADIUS*2), int(PLAYER_RADIUS*2)))
        self.player_image = self.original_image
        self.rect = self.player_image.get_rect()
        self.rect.center = (x,y)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        #pygame.draw.polygon(screen, 'white', self.triangle(), 2)
        pygame.draw.circle(screen, (255, 0, 0), self.rect.center, self.radius, 2)  # Debug circle
        screen.blit(self.player_image, self.rect)  # Draw the player sprite
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt*-1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt*-1)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        if self.timer > 0:
            self.timer -= dt
            
        self.update_image()
            
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        self.rect.center = self.position
    
    def shoot(self):
        if self.check_timer():
            shot = Shot(self.position.x, self.position.y)
            self.sound_manager.play_sound('shoot')
            shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.timer += PLAYER_SHOOT_COOLDOWN
    
    def check_timer(self):
        return self.timer <= 0 
    
    def update_image(self):
        # Rotate the image to match the current rotation
        self.player_image = pygame.transform.rotate(self.original_image, -self.rotation)
        # Update the rect to fit the rotated image
        self.rect = self.player_image.get_rect(center=self.rect.center)
    