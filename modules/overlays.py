"""modules de définition des overlays"""
import pygame

from modules.graphics import Texte, RelativePos, Element, StaticElement
from modules.outils import extend_mask, forme_mask


pygame.init()


class Compteur:
    """classe compteur"""

    def __init__(self, pos: pygame.Vector3 | RelativePos, interface_nom: str) -> None:
        self.texte = Texte(pos, interface_nom = interface_nom)
        self.points = 0

    def incremente(self, point: int = 1):
        """incrémente le compteur de points"""
        self.points += point
        self.texte.texte = f'Points: {self.points}'

    def vide(self):
        """incrémente le compteur de points"""
        self.points = 0
        self.texte.texte = f'Points: {self.points}'

class HealthBar:
    """représentation de la barre de vie"""

    def __init__(self, pos: RelativePos | pygame.Vector3, unit_texture: pygame.Surface, repetition: int = 1, interface_nom: str | None = None) -> None:
        self.pos = pos
        self.width = unit_texture.get_width()
        self.unit_texture = unit_texture

        surface = pygame.Surface((self.width * repetition, unit_texture.get_height()))
        self.repetition = repetition
        for posx in range(repetition):
            surface.blit(unit_texture, (posx * self.width, 0))

        self.element = Element(self, surface, surface.get_rect(), interface_nom, False)

    def set_repetition(self, nombre: int):
        """change le nombre de répétition"""
        self.repetition = nombre

    def update(self):
        """mise à jour"""
        surface = pygame.Surface((self.width * self.repetition, self.unit_texture.get_height()))
        for posx in range(self.repetition):
            surface.blit(self.unit_texture, (posx * self.width, 0))

        self.element.surface = surface
        self.element.rect = self.element.surface.get_rect()

<<<<<<< Updated upstream

class DtRenderer:

    def __init__(self, pos: RelativePos | pygame.Vector3, interface_nom: str | None = None) -> None:
        self.pos = pos
        self.texte = Texte(pos, interface_nom = interface_nom)
        self.element = Element(self, pygame.Surface((0, 0)), pygame.Rect(0, 0, 0, 0), interface_nom)
        self.dt = 0
        self.time = pygame.time.get_ticks()

    def update(self):
        self.dt = pygame.time.get_ticks() - self.time
        self.time = pygame.time.get_ticks()
        self.texte.texte = str(self.dt)
=======
class Background:
    def __init__(self) -> None:
        surface = pygame.image.load('ressources/textures/image.png')
        self.pos = pygame.Vector3(0, 0, 0)

        self.element = StaticElement(self, surface, pygame.Mask(), 'background')
>>>>>>> Stashed changes
