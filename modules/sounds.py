"""modules de gestion du son"""

import pygame

pygame.mixer.init()

with open('ressources/sounds/pacman_death.wav', 'r') as file:
    DEATH_SOUND = pygame.mixer.Sound(file)
with open('ressources/sounds/pacman_eat.wav', 'r') as file:
    EAT_SOUND = pygame.mixer.Sound(file)
with open('ressources/sounds/pacman_eatfruit.wav', 'r') as file:
    FRUIT_SOUND = pygame.mixer.Sound(file)
with open('ressources/sounds/pacman_eatghost.wav', 'r') as file:
    GHOST_SOUND = pygame.mixer.Sound(file)
with open('ressources/sounds/pacman_extra.wav', 'r') as file:
    EXTRA_SOUND = pygame.mixer.Sound(file)