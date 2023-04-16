"""modules de définition des overlays"""
import pygame

from modules.graphics import Texte, RelativePos

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
