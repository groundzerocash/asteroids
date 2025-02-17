import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid, Explosion
from boss import Boss
from asteroidfield import AsteroidField
from shot import Shot
from sound_manager import SoundManager
from gameover import game_over_screen, win_screen, title_screen


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    title_screen(screen)
    
    time_elapsed = 0  # Start internal clock to have boss timer start
    boss_spawned = False
    sound_manager = SoundManager()
    sound_manager.load_sound('die', 'assets/sounds/die_sound.wav')
    sound_manager.load_sound('win', 'assets/sounds/win.wav')
    sound_manager.load_music('assets/sounds/scifi.mp3')
    sound_manager.play_music()
    
    # Setup sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField()
    
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Spawn player in the center
    
    dt = 0
    explosion_complete = False  # Flag to track if the explosion animation is complete
    explosion_start_time = None
    boss_defeated = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # Update the objects
        for obj in updatable:
            if isinstance(obj, Boss):
                obj.update(dt, player)  # Boss needs player to update
            else:
                obj.update(dt)
                
        # Handle collisions (Player and Asteroids)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                sound_manager.stop_music()
                sound_manager.play_sound('die')
                if game_over_screen(screen):  # If they choose to try again
                    main()
                else:
                    return  # Exit the game if they don't restart
                
        
        # Handle bullet-asteroid (and boss) collisions
        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.collides_with(bullet):
                    if isinstance(asteroid, Boss):  # If it's the boss
                        asteroid.take_damage()
                        bullet.kill()
                        if asteroid.health <= 0:  # Boss defeated
                            sound_manager.stop_music()
                            boss_defeated = True
                            # Trigger explosion animation
                            explosion = Explosion(asteroid.rect.centerx, asteroid.rect.centery)  # Position the explosion where the asteroid is
                            updatable.add(explosion)  # Add explosion to the group to be updated
                            drawable.add(explosion)   # Add explosion to the group to be drawn
                            
                            for asteroid in asteroids:
                                asteroid.kill()


                            asteroid.kill()  # Remove the boss after the explosion starts
                            explosion_start_time = pygame.time.get_ticks()  # Record time when explosion started
                    else:  # Normal asteroids
                        asteroid.split()
                        bullet.kill()


        # Spawn the boss after 15 seconds
        if time_elapsed >= 5 and not boss_spawned:
            asteroid_field.spawn_boss(updatable, drawable)  # Spawn boss at custom location
            boss_spawned = True
            sound_manager.play_boss_music()
        
        # Prevent new asteroids from spawning if the boss is defeated
        if not boss_defeated:
            # Logic to spawn regular asteroids (if needed)
            #asteroid_field.spawn_asteroids(updatable, drawable)
            pass

        # Update the screen
        screen.fill('black')

        # Draw all objects
        for obj in drawable:
            obj.draw(screen)

        # Check if the explosion has finished by counting the explosions still in the game
        if len([obj for obj in updatable if isinstance(obj, Explosion)]) == 0 and explosion_start_time:
            for asteroid in asteroids:
                asteroid.kill()
            # If explosion is finished, check if enough time has passed to show win screen
            if pygame.time.get_ticks() - explosion_start_time >= 3000:  # Wait for 1 second after explosion
                if not explosion_complete:
                    sound_manager.play_sound('win')  # Play win sound
                    explosion_complete = True  # Set the flag to true to avoid triggering the win screen repeatedly
                
                if win_screen(screen):  # Show win screen after explosion finishes
                    main()  # Restart game
                else:
                    return  # Exit game if player doesn't restart

        pygame.display.flip()
        
        clock.tick(60)
        
        dt = clock.get_time() / 1000
        time_elapsed += dt


if __name__ == "__main__":
    main()
