"""module de création du plateau"""
import pygame

from modules.overlays import StaticTexture
from modules.outils import extend_mask, forme_mask

pygame.init()

def initialisation():
    """initialise le plateau"""
    surface = pygame.image.load('ressources/textures/map.png')
    pos = pygame.Vector3(0, 0, 0) # pygame.Vector3(-16, -16, 0) #
    mask = forme_mask(surface, 8)
    mask = extend_mask(mask)
    return StaticTexture(surface, pos, mask, 'plateau')
