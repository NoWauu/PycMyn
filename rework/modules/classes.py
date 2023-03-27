"""module de définition des classes principales"""
from typing import List, Any, Tuple
import pygame

from modules import outils

pygame.init()

# fonctions


def vect2_to_tuple(vecteur: pygame.Vector2):
    """convertie un vecteur2 en tuple d'entier"""
    return round(vecteur.x), round(vecteur.y)

# classes


class Interface:
    """classe de représentation des Interfaces"""
    current_interface: 'Interface'

    def __init__(self) -> None:
        self.elements: List['Element'] = []

    def add_element(self, element: 'Element'):
        """ajoute un élément à la liste"""
        index = outils.dichotomie(
            [elm.pos.z for elm in self.elements], element.pos.z)
        self.elements.insert(index, element)

    def remove_element(self, element: 'Element'):
        """retire un élément de la liste"""
        self.elements.remove(element)

    def update(self):
        for elm in self.elements:
            if hasattr(elm.objet, 'update'):
                elm.objet.update()

    def render(self):
        """méthode d'affichage"""
        return (elm.render() for elm in self.elements)


class Element:
    """
    classe de représentation
    d'un élément graphique
    """

    def __init__(self, objet: Any, pos: pygame.Vector3, surface: pygame.Surface, rectangle: pygame.Rect) -> None:
        self.pos = pos
        self.surface = surface
        self.rect = rectangle
        self.objet = objet

    def ancre(self, ancre: str = 'topleft'):
        """ancre le rectangle à la bonne position"""
        match ancre:
            case 'centre':
                self.rect.center = vect2_to_tuple(self.pos.xy)
            case _:
                self.rect.topleft = vect2_to_tuple(self.pos.xy)

    def render(self):
        """méthode d'affichage"""
        return self.surface, self.rect


class Text:
    """
    classe de représentation du texte
    """
    POLICE = pygame.font.SysFont('Arial', 20)

    def __init__(self, texte: str, pos: tuple[int, int], priority: int,
                 couleur: str = '#FFFFFF', interface: Interface | None = None) -> None:
        model = Text.POLICE.render(texte, True, couleur)
        self.element = Element(self, pygame.Vector3(
            pos[0], pos[1], priority), model, model.get_rect())

        if interface is None:
            Interface.current_interface.add_element(self.element)

    def update(self):
        """méthode de mis à jour"""
        self.element.ancre()


class AnimElement:
    """classe de gestion des animations"""

    def __init__(self, objet, default_texture: pygame.Surface,
                 textures: List[pygame.Surface], times: List[float],
                 interface: Interface | None=None) -> None:
        """infos: temps en millisecondes"""
        self.default_texture = default_texture
        self.textures = textures
        self.times = times
        self.valide_start = True

        if len(self.textures) != len(self.times):
            raise ValueError

        self.anim_index: int
        self.is_in_animation = False

        # objet à proxy
        self.objet = objet

        # renderer
        self.element = Element(
            self, self.objet.pos, self.default_texture, self.default_texture.get_rect())

        if interface is None:
            Interface.current_interface.add_element(self.element)

    def reset_anim(self):
        """reset les animations"""
        self.is_in_animation = False
        self.anim_index = 0
        self.valide_start = False

    def start_anim(self):
        """déclenche une animation"""
        self.is_in_animation = True
        self.anim_index = 0
        self.valide_start = False
        self.start_anim_time = pygame.time.get_ticks()

    def check_next_anim(self) -> Tuple[pygame.Surface, bool]:
        """si le temps lié à l'animation est écoulé,
        passe à la texture suivante"""
        time = pygame.time.get_ticks()
        change = False
        if not self.valide_start:
            self.valide_start = True
            change = True

        if self.is_in_animation and time - self.start_anim_time >= self.times[self.anim_index]:
            self.anim_index += 1
            self.start_anim_time = time
            change = True

        if self.is_in_animation and self.anim_index >= len(self.textures):
            # self.anim_index = -1
            self.is_in_animation = False
            return self.default_texture, True

        if not self.is_in_animation:
            return self.default_texture, change

        return self.textures[self.anim_index], change

    def update(self):
        """méthode de mise à jour"""
        if hasattr(self.objet, 'update'):
            self.objet.update()
            self.element.pos = self.objet.pos

        texture, change = self.check_next_anim()
        if change:
            self.element.surface = texture
            self.element.rect = texture.get_rect()
