"""module outils"""
from typing import List
import pygame

# constantes

UNIT_SIZE = 16

# fonctions


def dichotomie(liste: List[float], valeur: float) -> int:
    """
    renvoie l'index d'une liste
    avec une recherche dichotomique
    >>> dichotomie([1, 2, 3], 2.5)
    2
    """
    if len(liste) == 0:
        # cas d'une liste vide
        return 0

    if len(liste) == 1:
        # les listes commencent à zéros
        return valeur >= liste[0]

    mid_index: int = len(liste)//2
    mid: float = liste[mid_index]

    if mid <= valeur:
        return mid_index + dichotomie(liste[mid_index:], valeur)
    else:
        return dichotomie(liste[:mid_index], valeur)


def reste_etendu(a: float, b: float):
    """renvoie (a % b si a >= 0 ou a < -1) et (a si -1 <= a < 0)"""
    return a % b if a >= 0 or a < -UNIT_SIZE else a


def extend_mask(mask: pygame.mask.Mask) -> pygame.mask.Mask:
    """étend le mask dans toutes les directions de 1 pixel"""
    width, height = mask.get_size()

    new_mask = pygame.mask.Mask(
        (width + 2 * UNIT_SIZE, height + 2 * UNIT_SIZE))
    new_mask.draw(mask, (UNIT_SIZE, UNIT_SIZE))

    # y = -1 & y = height + 1
    for x in range(width):
        if mask.get_at((x, 0)):
            new_mask.set_at((x + UNIT_SIZE, UNIT_SIZE - 1))
        if mask.get_at((x, height - 1)):
            new_mask.set_at((x + UNIT_SIZE, height + UNIT_SIZE))

    # x = -1 & x = width + 1
    for y in range(height):
        if mask.get_at((0, y)):
            new_mask.set_at((UNIT_SIZE - 1, y + UNIT_SIZE))
        if mask.get_at((width - 1, y)):
            new_mask.set_at((width + UNIT_SIZE, y + UNIT_SIZE))

    # corners
    new_mask.set_at((UNIT_SIZE - 1, UNIT_SIZE - 1))
    new_mask.set_at((UNIT_SIZE - 1, height + UNIT_SIZE))
    new_mask.set_at((width + UNIT_SIZE, UNIT_SIZE - 1))
    new_mask.set_at((width + UNIT_SIZE, height + UNIT_SIZE))

    return new_mask


def forme_mask(surface: pygame.Surface):
    """crée un mask à partir d'une surface donnée"""
    mask = pygame.Mask((UNIT_SIZE, UNIT_SIZE), True)
    if surface.get_width() % UNIT_SIZE or surface.get_height() % UNIT_SIZE:
        raise ValueError
    
    surf_mask = pygame.mask.from_surface(surface, 1)
    forme_surf_mask = pygame.Mask(surface.get_size())
    
    for coordx in range(surface.get_width() // UNIT_SIZE):
        for coordy in range(surface.get_height() // UNIT_SIZE):
            # si un pixel de la surface est actif
            # on considère la case entière comme active dans le mask
            if surf_mask.overlap(mask, (UNIT_SIZE * coordx, UNIT_SIZE * coordy)) is not None:
                forme_surf_mask.draw(mask, (UNIT_SIZE * coordx, UNIT_SIZE * coordy))
    return forme_surf_mask
