"""Module de gestion des Entités"""
from typing import List, Tuple, Dict, Any

import pygame

from modules.graphics import AnimElement, Frame, vect2_to_tuple
from modules.overlays import StaticTexture
import modules.outils as utl

pygame.init()

# fonctions de déplacement


def haut(pos: pygame.Vector2, speed: float, deltat: float):
    """déplacement vers le haut"""
    return pygame.Vector2(pos.x,
                          round(utl.reste_etendu(
                              (pos.y - speed * deltat / 1000),
                              Frame.get_surface_by_name('plateau').get_height())))


def bas(pos: pygame.Vector2, speed: float, deltat: float):
    """déplacement vers le bas"""
    return pygame.Vector2(pos.x,
                          round(utl.reste_etendu(
                              (pos.y + speed * deltat / 1000),
                              Frame.get_surface_by_name('plateau').get_height())))


def gauche(pos: pygame.Vector2, speed: float, deltat: float):
    """déplacement vers la gauche"""
    return pygame.Vector2(round(utl.reste_etendu((pos.x - speed * deltat / 1000),
                                                 Frame.get_surface_by_name('plateau').get_width())),
                          pos.y)


def droite(pos: pygame.Vector2, speed: float, deltat: float):
    """déplacement vers la droite"""
    return pygame.Vector2(round(utl.reste_etendu((pos.x + speed * deltat / 1000),
                                                 Frame.get_surface_by_name('plateau').get_width())),
                          pos.y)


def immobile(pos: pygame.Vector2, *_: Any):
    """reste immobile"""
    return pos


CASE = {1: haut,
        3: bas,
        2: gauche,
        0: droite,
        -1: immobile}


class Entity:
    """Classe racine des entités"""
    plateau: StaticTexture
    group: List['Entity'] = []

    niveau = utl.SAVE['niveau_sauvegarde']

    def __init__(self, pos: pygame.Vector3,
                 anim_infos: Tuple[pygame.Surface,
                                   Dict[str, List[Tuple[pygame.Surface, float]]]]) -> None:
        self.pos = pos
        self.hard_collide = False

        # rendereur
        self.animation = AnimElement(
            self, anim_infos[0], anim_infos[1], 'plateau')
        self.idt = 0

        Entity.group.append(self)

    def collide_with(self, point: pygame.Vector2 | None = None) -> List['Entity']:
        """return a list containing the sprites colliding with this one"""
        Entity.group.remove(self)
        lis: List['Entity'] = []

        save_pos = self.animation.rect.topleft
        if point is not None:
            self.animation.rect.topleft = vect2_to_tuple(point)
        for enit in Entity.group:
            if enit.animation.rect.colliderect(self.animation.rect):
                lis.append(enit)
        if point is not None:
            self.animation.rect.topleft = save_pos

        Entity.group.append(self)
        return lis

    def collide_wall(self, pos: pygame.Vector2):
        """Check if the entity collide with walls"""
        # on utilise (-pos.x, -pos.y) car le coin supérieur gauche du masque
        # est considéré comme étant (0, 0). Le masque des murs est par conséquent décalé.
        # on doit donc le recentré
        return Entity.plateau.element.mask.overlap(self.animation.mask,
                                                   (pos.x + utl.UNIT_SIZE,
                                                    pos.y + utl.UNIT_SIZE)) is not None

    def destroy(self) -> None:
        """détruit l'entité"""
        self.animation.delie()
        Entity.group.remove(self)
        del self.animation
        del self

    @classmethod
    def set_niveau(cls, niveau: int):
        """change le niveau"""
        cls.niveau = niveau


def clear():
    """réinitialise tous les éléments du jeux"""
    while len(Entity.group) > 0:
        Entity.group[0].destroy()
    utl.clear(['init_entities', 'powerup'])
    utl.call('vide_point', {})
    utl.call('set_vie', {'nombre': 3})
