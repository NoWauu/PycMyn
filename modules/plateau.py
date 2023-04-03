"""module de création du plateau"""
import pygame

from modules.classes import StaticElement
from modules.outils import extend_mask


class Plateau:
    """classe de gestion du plateau"""
    window: pygame.Surface

    def __init__(self) -> None:
        surface = pygame.image.load('ressources/plateau.png')
        self.pos = pygame.Vector3(0, 0, 0)
        self.element = StaticElement(self, surface, extend_mask(pygame.mask.from_surface(surface)), 'jeux')
