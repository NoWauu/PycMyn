"""module de gestion des pièces et des super-pouvoirs"""
from typing import Tuple, List, Set
import random

import pygame

from modules.entite import Entity
from modules.outils import UNIT_SIZE


class Collectable(Entity):
    """classe de gestion des collectables"""
    texture = pygame.Surface((32, 32))  # texture par défaut

    def __init__(self, position: pygame.Vector3) -> None:
        super().__init__(
            position, (self.texture, {}, {}))

    @classmethod
    def settexture(cls, texture: pygame.Surface) -> pygame.Surface:
        """remplace la texture unique de l'objet
        et renvoie l'ancienne texture"""
        pre_texture = cls.texture
        cls.texture = texture

        return pre_texture


class Piece(Collectable):
    """classe de gestion des pièces"""

    def __init__(self, position: pygame.Vector3) -> None:
        super().__init__(position)


class Pomme(Collectable):
    """classe de gestion des Pommes"""

    def __init__(self, position: pygame.Vector3) -> None:
        super().__init__(position)


class Super(Collectable):
    """classe de gestion des Pommes"""

    def __init__(self, position: pygame.Vector3) -> None:
        super().__init__(position)


def choose_pos(k: int, positions: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """choisi k positions parmis la liste donnée"""
    temp: List[Tuple[int, int]] = []

    for _ in range(k):
        pos = random.choice(list(positions))
        positions.remove(pos)  # effets de bords volontaires
        temp.append(pos)

    return temp


def get_empty_placement(scheme: pygame.mask.Mask) -> Set[Tuple[int, int]]:
    """renvoie un dictionnaire constitué des positions libres du mask"""
    width, height = scheme.get_size()

    return {(x, y) for y in range(height // UNIT_SIZE - 2)
            for x in range(width // UNIT_SIZE - 2)
            if not scheme.get_at(((x + 1) * UNIT_SIZE + 16,
                                  (y + 1) * UNIT_SIZE + 16))}


def populate():
    """place les pièces sur le plateaux"""
    scheme: pygame.mask.Mask = Entity.plateau.element.mask

    empty_placement = get_empty_placement(scheme)

    empty_placement.remove((3, 3))  # à retirer
    empty_placement.remove((4, 3))
    empty_placement.remove((5, 3))
    empty_placement.remove((6, 3))

    empty_placement.remove((3, 2))
    empty_placement.remove((6, 2))

    pommes_pos = choose_pos(4, empty_placement)
    super_pos = choose_pos(4, empty_placement)

    for pos in pommes_pos:
        Pomme(pygame.Vector3(pos[0] * UNIT_SIZE,
                pos[1] * UNIT_SIZE, 1))

    for pos in super_pos:
        Super(pygame.Vector3(pos[0] * UNIT_SIZE,
               pos[1] * UNIT_SIZE, 1))

    # pièces

    piece_scheme = None  # à changer

    # à changer en get_empty_placement(piece_scheme)
    piece_spot = empty_placement

    for pos in piece_spot:
        if pos in empty_placement:
            Piece(pygame.Vector3(pos[0] * UNIT_SIZE,
                   pos[1] * UNIT_SIZE, 1))
