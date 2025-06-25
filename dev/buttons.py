import pygame
def intro(screen):
    #play the game
    play_surf = pygame.Surface((200, 100)).convert()
    play_surf.fill((150, 0, 255))
    play_rect = play_surf.get_rect(center = (400, 200))
    screen.blit(play_surf, play_rect)

    #help button
    help_surf = pygame.Surface((200, 100)).convert()
    help_surf.fill((200, 0, 200))
    help_rect = help_surf.get_rect(center = (400, 400))
    screen.blit(help_surf, help_rect)