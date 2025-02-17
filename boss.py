import pygame
from circleshape import CircleShape
from constants import *
from sound_manager import SoundManager
from asteroid import Asteroid, Explosion

# In your Boss class:

class Boss(Asteroid):
    def __init__(self, x, y):
        super().__init__(x, y, ASTEROID_MAX_RADIUS * 1.5)
        self.velocity = pygame.Vector2(0, 0)
        self.sound_manager = SoundManager()
        
        self.boss_image = pygame.image.load('assets/images/boss.png')
        self.boss_image = pygame.transform.scale(self.boss_image, (int(ASTEROID_MAX_RADIUS * 1.5 * 2), int(ASTEROID_MAX_RADIUS * 1.5 * 2)))
        self.rect = self.boss_image.get_rect()
        self.rect.center = (x, y)
        self.health = BOSS_HEALTH
        
        self.alpha = 255  # Initial opacity

    def take_damage(self):
        """Handle damage to the boss."""
        self.health -= 1
        if self.health <= 0:
            self.alpha = 255  # Reset alpha if boss is defeated
            self.kill()  # Remove the boss from the game

    def update(self, dt, player=None):
        """Update boss position and handle fade-out."""
        if self.health <= 0:  # If the boss is defeated
            self.alpha -= 5  # Fade out (decrease alpha)
            if self.alpha < 0:
                self.alpha = 0  # Ensure alpha doesn't go below 0
            self.boss_image.set_alpha(self.alpha)

        # Normal movement and update code for the boss
        if player:
            self.direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
            if self.direction.length() > 1:
                self.direction = self.direction.normalize()
                self.velocity = self.direction * 50

            self.position += self.velocity * dt
            self.rect.center = self.position

    def draw(self, screen):
        """Draw the boss on the screen."""
        screen.blit(self.boss_image, self.rect)
    
    def self_destruct(self, updatable, drawable):
        """Trigger explosion and remove the asteroid."""
        # Create the explosion at the asteroid's current position
        explosion = Explosion(self.rect.centerx, self.rect.centery)
        updatable.add(explosion)
        drawable.add(explosion)
        explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')
        explosion_sound.play()  # Play the explosion sound
        
        self.kill()  # Remove the asteroid from the game



    