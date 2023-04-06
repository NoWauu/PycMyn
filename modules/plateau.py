"""module de création du plateau"""
import pygame

from modules.classes import StaticElement
from modules.outils import extend_mask, forme_mask


class Plateau:
    """classe de gestion du plateau"""

    def __init__(self) -> None:
        surface = pygame.image.load('ressources/map.png')
        print(surface.get_size())
        self.pos = pygame.Vector3(0, 0, 0) #pygame.Vector3(-16, -16, 0)
        mask = extend_mask(forme_mask(surface))
        self.element = StaticElement(self, surface, mask, 'jeux')
