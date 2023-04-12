"""module de gestion des pièces et des super-pouvoirs"""
from typing import Tuple, List, Set
import random

import pygame

from modules.entite import Entity
from modules.outils import UNIT_SIZE, forme_mask


class Collectable(Entity):
    """classe de gestion des collectables"""
    texture = pygame.Surface((UNIT_SIZE, UNIT_SIZE))  # texture par défaut

    def __init__(self, position: pygame.Vector3) -> None:
        super().__init__(
            position, (self.texture, {}))

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

    return {(x, y) for y in range(height // UNIT_SIZE)
            for x in range(width // UNIT_SIZE)
            if not scheme.get_at((x * UNIT_SIZE,
                                  y * UNIT_SIZE))}


def populate(surface: pygame.Surface):
    """place les pièces sur le plateaux"""
    mask = forme_mask(surface, UNIT_SIZE)
    mask.draw(pygame.mask.from_surface(pygame.image.load('ressources/textures/fantome_map.png')), (0, 0))
    empty_placement = get_empty_placement(mask)

    pommes_pos = choose_pos(4, empty_placement)
    super_pos = choose_pos(4, empty_placement)
    
    for pos in pommes_pos:
        Pomme(pygame.Vector3(pos[0] * UNIT_SIZE,
                pos[1] * UNIT_SIZE, 1))

    for pos in super_pos:
        Super(pygame.Vector3(pos[0] * UNIT_SIZE,
               pos[1] * UNIT_SIZE, 1))

    # pièces

    piece_spot = empty_placement

    for pos in piece_spot:
        if pos in empty_placement:
            Piece(pygame.Vector3(pos[0] * UNIT_SIZE,
                   pos[1] * UNIT_SIZE, 1))

# setup

texture_piece = pygame.Surface((UNIT_SIZE, UNIT_SIZE), pygame.SRCALPHA)
pygame.draw.circle(texture_piece, (250, 198, 53), (UNIT_SIZE // 2, UNIT_SIZE // 2), 3)

texture_pomme = pygame.transform.scale(
    pygame.image.load("ressources/textures/pomme.png"), (UNIT_SIZE, UNIT_SIZE))

texture_super = pygame.Surface((UNIT_SIZE, UNIT_SIZE), pygame.SRCALPHA)
pygame.draw.circle(texture_super, (255, 255, 255), (UNIT_SIZE // 2, UNIT_SIZE // 2), 6)

Piece.settexture(texture_piece)
Pomme.settexture(texture_pomme)
Super.settexture(texture_super)
