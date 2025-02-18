import pygame
from circleshape import CircleShape
from constants import *
from sound_manager import SoundManager
from asteroid import Asteroid, Explosion
from math import atan2, degrees

class Boss(Asteroid):
    def __init__(self, x, y):
        super().__init__(x, y, ASTEROID_MAX_RADIUS * 1.5)
        self.velocity = pygame.Vector2(0, 0)
        self.sound_manager = SoundManager()
        
        # Load the original boss image (without rotation)
        self.original_boss_image = pygame.image.load('assets/images/boss.png')
        self.original_boss_image = pygame.transform.scale(self.original_boss_image, (int(ASTEROID_MAX_RADIUS * 1.5 * 2), int(ASTEROID_MAX_RADIUS * 1.5 * 2)))
        self.boss_image = self.original_boss_image
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
        """Update boss position, handle fade-out, and rotation towards the player."""
        if self.health <= 0:  # If the boss is defeated
            self.alpha -= 5  # Fade out (decrease alpha)
            if self.alpha < 0:
                self.alpha = 0  # Ensure alpha doesn't go below 0
            self.boss_image.set_alpha(self.alpha)

        # Normal movement and update code for the boss
        if player:
            # Calculate direction towards the player
            self.direction = pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
            
            # If there is movement, normalize direction
            if self.direction.length() > 1:
                self.direction = self.direction.normalize()
                self.velocity = self.direction * 50

            # Update boss position
            self.position += self.velocity * dt
            self.rect.center = self.position

            # Calculate the angle to rotate the boss towards the player
            angle = atan2(self.direction.y, self.direction.x)
            rotated_image = pygame.transform.rotate(self.original_boss_image, -degrees(angle))  # Rotate in the correct direction
            self.rect = rotated_image.get_rect(center=self.rect.center)  # Keep the boss centered after rotation
            self.boss_image = rotated_image

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





    