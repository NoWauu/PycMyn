"""module de définition des classes principales"""
from typing import List, Any, Tuple, Dict
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
    interfaces: Dict[str, 'Interface'] = {}

    def __init__(self, nom: str | None = None) -> None:
        self.elements: List['Element'] = []

        if nom is not None:
            Interface.interfaces[nom] = self

    def add_element(self, element: 'Element'):
        """ajoute un élément à la liste"""
        index: int = outils.dichotomie(
            [elm.pos.z for elm in self.elements], element.pos.z)
        self.elements.insert(index, element)
        element.interface = self

    def remove_element(self, element: 'Element'):
        """retire un élément de la liste"""
        self.elements.remove(element)

    def on_keypress(self, event: pygame.event.Event):
        """gère les touches appuyées"""
        for elm in self.elements:
            if hasattr(elm.objet, 'on_keypress'):
                elm.objet.on_keypress(event)

    def update(self):
        for elm in self.elements:
            if hasattr(elm, 'update'):
                elm.update()
            if hasattr(elm, 'objet') and hasattr(elm.objet, 'update'):
                elm.objet.update()

    def render(self):
        """méthode d'affichage"""
        return (elm.render() for elm in self.elements)

    @classmethod
    def add_element_to(cls, element: 'Element', interface_nom: str):
        """ajoute un élément à l'interface donnée"""
        if interface_nom in cls.interfaces:
            cls.interfaces[interface_nom].add_element(element)


class Element:
    """
    classe de représentation
    d'un élément graphique
    """

    def __init__(self, objet: Any, surface: pygame.Surface, rectangle: pygame.Rect, interface_nom: str | None = None) -> None:
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface, threshold=1)
        self.rect = rectangle
        self.objet = objet
        self.backup_rotation = 0
        self.pos: pygame.Vector3 = self.objet.pos
        self.interface: Interface

        if interface_nom is None:
            Interface.current_interface.add_element(self)
        else:
            Interface.add_element_to(self, interface_nom)

    def delink(self):
        """délie l'élément"""
        self.interface.remove_element(self)

    def ancre(self, ancre: str = 'topleft'):
        """ancre le rectangle à la bonne position"""
        # cas où l'élément n'est pas encore binder
        if not hasattr(self, 'objet'):
            return

        self.pos: pygame.Vector3 = self.objet.pos
        match ancre:
            case 'centre':
                self.rect.center = vect2_to_tuple(self.pos.xy)
            case _:
                self.rect.topleft = vect2_to_tuple(self.pos.xy)

    def update(self):
        """methode de mise à jour"""
        self.ancre()

        if hasattr(self, 'objet') and hasattr(self.objet, 'rotation'):
            # en degrés
            self.surface = pygame.transform.rotate(
                self.surface, self.objet.rotation - self.backup_rotation)
            self.backup_rotation = self.objet.rotation
        self.mask = pygame.mask.from_surface(self.surface, threshold=1)

    def render(self):
        """méthode d'affichage"""
        return self.surface, self.rect


class Frame:
    """
    classe de représentation d'un groupement
    d'élément dans un cadre
    """

    frames: Dict[str, 'Frame'] = {}

    def __init__(self, nom: str, interface: Interface, surface: pygame.Surface, pos: pygame.Vector3, interface_nom: str | None = None) -> None:
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.pos = pos
        self.interface = interface
        self.element = Element(self, surface, self.rect, interface_nom)

        if nom not in Frame.frames:
            Frame.frames[nom] = self

    def on_keypress(self, event: pygame.event.Event):
        """gestion des touches"""
        self.interface.on_keypress(event)

    def update(self):
        """méthode de mise à jour"""
        # clear
        self.surface.fill('#000000')
        self.interface.update()
        self.surface.blits(list(self.interface.render()))


class RelativePos:
    """
    classe de représentation
    des positions variables
    """
    window: pygame.Surface

    def __init__(self, relx: float, rely: float) -> None:
        self.relx, self.rely = relx, rely
        self.x: float
        self.y: float

    def update(self):
        """méthode de mise à jour"""
        self.x = self.relx * RelativePos.window.get_width()
        self.y = self.rely * RelativePos.window.get_height()


class StaticElement(Element):
    """création d'un modèle immuable"""

    def __init__(self, objet: Any, surface: pygame.Surface, mask: pygame.Mask | None = None, interface_nom: str | None = None) -> None:
        super().__init__(objet, surface, surface.get_rect(), interface_nom)
        self.ancre()
        if mask is not None:
            self.mask = mask

    def update(self):
        """surécrit la méthode pour la désactiver"""
        ...


class AnimElement(Element):
    """classe de gestion des animations"""

    def __init__(self, objet: Any, default_texture: pygame.Surface,
                 textures: Dict[str, List[pygame.Surface]],
                 times: Dict[str, List[float]], interface_nom: str | None = None) -> None:
        """infos: temps en millisecondes"""
        self.default_texture = default_texture
        self.textures = textures
        self.times = times
        self.valide_start = True
        self.current_anim_nom: str

        self.anim_index: int
        self.is_in_animation = False
        self.start_anim_time: int = 0

        super().__init__(objet, self.default_texture,
                         self.default_texture.get_rect(), interface_nom)

    def reset_anim(self):
        """reset les animations"""
        self.is_in_animation = False
        self.anim_index = 0
        self.valide_start = False

    def start_anim(self, nom: str):
        """déclenche une animation"""
        self.is_in_animation = True
        self.anim_index = 0
        self.current_anim_nom = nom
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
        if self.is_in_animation and time - self.start_anim_time >= self.times[self.current_anim_nom][self.anim_index]:
            self.anim_index += 1
            self.start_anim_time = time
            change = True

        if self.is_in_animation and self.anim_index >= len(self.textures[self.current_anim_nom]):
            self.is_in_animation = False
            return self.default_texture, True

        if not self.is_in_animation:
            return self.default_texture, change

        return self.textures[self.current_anim_nom][self.anim_index], change

    def update(self):
        """méthode de mise à jour"""
        texture, change = self.check_next_anim()
        if change:
            self.surface = texture
            self.backup_rotation = 0
            self.rect = texture.get_rect()

        super().update()
