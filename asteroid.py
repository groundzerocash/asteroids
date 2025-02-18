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
        

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Load a sequence of images representing the explosion animation.
        self.frames = [
            pygame.image.load('assets/images/explosion.png'),
            pygame.image.load('assets/images/explosion2.png'),
            pygame.image.load('assets/images/explosion3.png'),
            #pygame.image.load('assets/images/explosion4.png'),
            # Add more frames if necessary
        ]

        # Set the initial image to the first frame
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Time tracking
        self.last_update_time = pygame.time.get_ticks()  # Tracks the last frame update time
        self.frame_delay = 500  # Delay in milliseconds (500 ms = 0.5 seconds)
        self.current_frame = 0
        self.max_lifetime = len(self.frames)  # Total number of frames in the explosion sequence

        # Play the explosion sound initially
        self.explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.wav')

    def update(self, dt):
        """Update the explosion animation (change frames every 0.5 seconds)."""
        # Check if enough time has passed (500ms)
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - self.last_update_time >= self.frame_delay:  # If 0.5s has passed
            self.last_update_time = current_time  # Reset the last update time to the current time
            self.current_frame += 1  # Move to the next frame

            self.explosion_sound.play()

            if self.current_frame >= self.max_lifetime:  # If all frames have been shown
                self.kill()  # Remove the explosion sprite from the game
            else:
                self.image = pygame.transform.scale(self.frames[self.current_frame], self.rect.center) # Update the image to the next frame

    def draw(self, screen):
        screen.blit(self.image, self.rect)



