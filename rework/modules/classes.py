"""module de définition des classes principales"""
from typing import List, Any
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
        index = outils.dichotomie([elm.pos.z for elm in self.elements], element.pos.z)
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

    def ancre(self, ancre: str='topleft'):
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

    def __init__(self, texte: str, pos: tuple[int, int], priority: int, couleur: str='#FFFFFF', interface: Interface | None=None) -> None:
        model = pygame.Surface((20, 20)) #Text.POLICE.render(texte, True, couleur)
        model.fill(couleur)
        self.element = Element(self, pygame.Vector3(pos[0], pos[1], priority), model, model.get_rect())

        if interface is None:
            Interface.current_interface.add_element(self.element)
    
    def update(self):
        """méthode de mis à jour"""
        self.element.ancre()
