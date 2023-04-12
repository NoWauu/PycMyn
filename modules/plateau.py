"""module de création du plateau"""
import pygame

from modules.graphics import StaticElement
from modules.outils import extend_mask, forme_mask


class Plateau:
    """classe de gestion du plateau"""

    def __init__(self) -> None:
        surface = pygame.image.load('ressources/textures/map.png')
        self.pos = pygame.Vector3(0, 0, 0) #pygame.Vector3(-16, -16, 0)
        mask = forme_mask(surface, 8)
        mask = extend_mask(mask)
        self.element = StaticElement(self, surface, mask, 'plateau')
