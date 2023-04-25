"""modules de définition des overlays"""
import pygame

from modules.graphics import Texte, RelativePos, Element, StaticElement, Sequence
import modules.outils as utl

pygame.init()


class Compteur:
    """classe compteur"""

    def __init__(self, pos: pygame.Vector3 | RelativePos,
                 interface_nom: str, base: str = '') -> None:
        self.points = 0
        self.base = base
        self.texte = Texte(pos, interface_nom=interface_nom)
        self.update_texte()

    def incremente(self, point: int = 1):
        """incrémente le compteur de points"""
        self.points += point
        self.update_texte()

    def vide(self):
        """réinitialise le compteur de points"""
        self.points = 0
        self.update_texte()

    def update_texte(self):
        """met à jour le texte du compteur"""
        self.texte.texte = self.base.format(value=self.points)


class HealthBar:
    """représentation de la barre de vie"""

    def __init__(self, pos: RelativePos | pygame.Vector3, unit_texture: pygame.Surface,
                 repetition: int = 1, interface_nom: str | None = None) -> None:
        self.pos = pos
        self.width = unit_texture.get_width()
        self.unit_texture = unit_texture

        surface = pygame.Surface(
            (self.width * repetition, unit_texture.get_height()))
        self.repetition = repetition
        for posx in range(repetition):
            surface.blit(unit_texture, (posx * self.width, 0))

        self.element = Element(
            self, surface, surface.get_rect(), interface_nom, False)

    def set_repetition(self, nombre: int):
        """change le nombre de répétition"""
        self.repetition = nombre

    def update(self):
        """mise à jour"""
        surface = pygame.Surface(
            (self.width * self.repetition, self.unit_texture.get_height()))
        for posx in range(self.repetition):
            surface.blit(self.unit_texture, (posx * self.width, 0))

        self.element.info_dct['surface'] = surface
        self.element.info_dct['rect'] = self.element.info_dct['surface'].get_rect()


class DtRenderer:
    """représentation du compteur de ms"""

    def __init__(self, pos: RelativePos | pygame.Vector3,
                 interface_nom: str | None = None) -> None:
        self.pos = pos
        self.texte = Texte(pos, interface_nom=interface_nom)
        self.element = Element(self, pygame.Surface(
            (0, 0)), pygame.Rect(0, 0, 0, 0), interface_nom)
        self.deltat = 0
        self.time = pygame.time.get_ticks()

    def update(self):
        """mise à jour"""
        self.deltat = pygame.time.get_ticks() - self.time
        self.time = pygame.time.get_ticks()
        self.texte.texte = str(self.deltat)


class Timer:
    """représentation d'un timer"""

    def __init__(self, pos: pygame.Vector3 | RelativePos, interface_nom: str) -> None:
        self.compteur = Compteur(pos, interface_nom, base='{value} s')
        self.temps = 0

        self.time_seq = Sequence(
            [((self.compteur.incremente, [1]), 1000)], loop=True, local=True)

    def start(self):
        """lance le timer"""
        self.reset()
        self.time_seq.start()

    def stop(self):
        """arrête le timer"""
        self.time_seq.stop()

    def reset(self):
        """réinitialise le compteur"""
        self.compteur.vide()

    def get_temps(self):
        """renvoie le temps chronométré en secondes"""
        return self.compteur.points


class StaticTexture:
    """classe de représentation de fond"""

    def __init__(self, texture: pygame.Surface,
                 pos: pygame.Vector3 | RelativePos = pygame.Vector3(0, 0, 0),
                 mask: pygame.Mask = pygame.Mask((0, 0)),
                 interface_nom: str | None = None) -> None:
        self.pos = pos

        self.element = StaticElement(
            self, texture, mask, interface_nom)

    def on_video_resize(self):
        """ajuste la texture à la fenêtre"""
        self.element.info_dct['rect'] = pygame.transform.scale_by(self.element.info_dct['surface'],
                                                         (max(utl.WINDOW.get_width()/
                                                              self.element.info_dct['surface'].get_width(),
                                                              utl.WINDOW.get_height() /
                                                              self.element.info_dct['surface'].get_height())))
        self.element.info_dct['rect'] = self.element.info_dct['surface'].get_rect()
