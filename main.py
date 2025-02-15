import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from boss import Boss
from asteroidfield import AsteroidField
from shot import Shot
from sound_manager import SoundManager
from gameover import game_over_screen


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    time_elapsed = 0 #start internal clock to have boss timer start
    boss_spawned = False
    
    sound_manager = SoundManager()
    sound_manager.load_sound('die','assets/sounds/die_sound.wav')
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
            if isinstance(obj, Boss):
                obj.update(dt, player) # boss needs player to update so they can move towards it
            else:
                obj.update(dt)
        
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sound_manager.play_sound('die')
                if game_over_screen(screen):  # If they choose to try again
                    main()
                else:
                    running = False  # Exit the game if they don't restart
        
        # Handle bullet-asteroid (and boss) collisions
        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.collides_with(bullet):
                    if isinstance(asteroid, Boss):  # If the asteroid is a boss
                        asteroid.take_damage()  # The boss takes damage
                        bullet.kill()  # Destroy the bullet after hitting the boss
                        if asteroid.health <= 0:  # If the boss has no health left
                            print("The boss is defeated!")
                            asteroid.kill()  # Remove the boss from the game
                            sound_manager.play_normal_music()
                    else:  # Normal asteroids
                        asteroid.split()  # Split the asteroid
                        bullet.kill()  # Destroy the bullet

                    
        if time_elapsed >= 10 and not boss_spawned:
            for asteroid in asteroids:
                asteroid.kill()
            asteroid_field.spawn_boss(updatable, drawable) # Spawn at a custom location
            boss_spawned = True 
            sound_manager.play_boss_music()
            
            
        
        screen.fill('black')
        
        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()
        
        clock.tick(60)
        
        dt = clock.get_time() / 1000
        
        time_elapsed += dt


        


if __name__ == "__main__":
    main()