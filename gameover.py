# game_over.py

import pygame
import sys

def title_screen(screen):
    font = pygame.font.SysFont(None, 48)
    title_text = font.render("GOAL: Defeat Enemy", True, (0, 0, 255))
    start_text = font.render("Press ENTER to Start", True, (0, 255, 0))

    while True:
        screen.fill((0, 0, 0))  # Black background

        # Draw the title text
        screen.blit(title_text, (250, 200))
        screen.blit(start_text, (250, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game on pressing ENTER
                    return

        pygame.display.update()


def game_over_screen(screen):
    font = pygame.font.SysFont("Arial", 48)
    
    # Text for Game Over and try again prompt
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    try_again_text = font.render("Press 'R' to Try Again or 'Q' to Quit", True, (255, 255, 255))
    
    # Get the size of the texts
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    try_again_rect = try_again_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Fill the screen with a black color
    screen.fill((0, 0, 0))
    
    # Blit the text onto the screen
    screen.blit(game_over_text, game_over_rect)
    screen.blit(try_again_text, try_again_rect)
    
    pygame.display.flip()

    # Wait for player input
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()  # Quit the game if 'Q' is pressed
                if event.key == pygame.K_r:
                    return True  # Return True to indicate a restart

    return False  # If no input, stay in the game over screen

def win_screen(screen):
    font = pygame.font.SysFont("Arial", 48)
    
    # Text for Game Over and try again prompt
    game_over_text = font.render("You Win!", True, (255, 0, 0))
    try_again_text = font.render("Press 'R' to Play Again or 'Q' to Quit", True, (255, 255, 255))
    
    # Get the size of the texts
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    try_again_rect = try_again_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    # Fill the screen with a black color
    screen.fill((0, 0, 0))
    
    # Blit the text onto the screen
    screen.blit(game_over_text, game_over_rect)
    screen.blit(try_again_text, try_again_rect)
    
    pygame.display.flip()

    # Wait for player input
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()  # Quit the game if 'Q' is pressed
                if event.key == pygame.K_r:
                    return True  # Return True to indicate a restart

    return False  # If no input, stay in the game over screen

