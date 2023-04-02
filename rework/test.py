import pygame

pygame.init()

img = pygame.image.load('ressources/plateau.png')

WINDOW = pygame.display.set_mode((600, 600))

while True:
    WINDOW.blit(pygame.mask.from_surface(img).to_surface(), (0, 0))
    pygame.display.flip()