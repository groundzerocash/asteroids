import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from sound_manager import SoundManager

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    sound_manager = SoundManager()
    sound_manager.load_music('assets/sounds/scifi.mp3')
    sound_manager.play_music()
    
    
    #Groups can be used to minimize code, we are covering the drawing of two classes (asteroids (which there are many), player) every instance, such as one press forward or backward
    #And the updating of all the classes
    #And we even have a group just for asteroids, that way we can loop through a tuple of asteroid vectors to see if they are in collision with the player class
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()
    
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)#spawns player in the center, if this is placed before - it does not show up  for some reason
    
    dt = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        for obj in updatable:
            obj.update(dt)
        
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()
        
        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.collides_with(bullet):
                    asteroid.split()
                    bullet.kill()
        
        screen.fill('black')
        
        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()
        
        clock.tick(60)
        
        dt = clock.get_time() / 1000
        


if __name__ == "__main__":
    main()