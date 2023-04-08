"""module de création du plateau"""
from typing import List
import pygame

from modules.outils import UNIT_SIZE
from modules.mask_tools import extend_mask


class Plateau:
    """classe de gestion du plateau"""

    def __init__(self, width: int, height: int) -> None:
        self.ecran: pygame.surface.Surface = pygame.Surface(
            (width * UNIT_SIZE, height * UNIT_SIZE))
        self.texture = pygame.image.load('ressources/textures/plateau.jpg')
        self.mask = extend_mask(pygame.mask.from_threshold(
            self.texture, pygame.Color('blue'), (1, 1, 1, 255)))

    def update_texture(self):
        self.texture = pygame.transform.scale(
            self.texture, self.ecran.get_size())

        self.rect: pygame.Rect = self.ecran.get_rect()

        self.mask = extend_mask(pygame.mask.from_threshold(
            self.texture, pygame.Color('blue'), (200, 200, 200, 255)))
        
    def update(self, Entites: pygame.sprite.Group, events: List[pygame.event.Event]):
        """met à jour les entités"""
        if len(Entites) > 0:
            for enit in Entites:
                enit.update(events)

    def render(self, Entites: pygame.sprite.Group):
        """Affiche tous les sprites en les ayant mis à jour"""

        self.update_texture()
        self.ecran.blit(self.texture, (0, 0))
        if len(Entites) > 0:
            Entites.draw(self.ecran)

        return self.ecran, self.rect
