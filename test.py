import pygame

pygame.init()

WINDOW = pygame.display.set_mode((600, 600))

surface = pygame.transform.scale(pygame.image.load('ressources/textures/map.png'), (224, 248))
#surface.fill('#FFFFA0')

pygame.draw.circle(surface, '#FFA0FF', (8, 8), 8)

mask = pygame.mask.from_surface(surface)
rects = pygame.mask.from_surface(surface).get_bounding_rects()

WINDOW.blit(surface, (400, 300))


for rect in rects:
    pygame.draw.rect(WINDOW, '#FFFFFF', rect)

WINDOW.blit(mask.to_surface(), (0, 248))

while True:
    pygame.display.flip()