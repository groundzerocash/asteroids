# game_over.py

import pygame

def game_over_screen(screen):
    font = pygame.font.SysFont("Arial", 48)
    
    # Text for Game Over and try again prompt
    game_over_text = font.render("Game Over, Get Back to Work!", True, (255, 0, 0))
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
