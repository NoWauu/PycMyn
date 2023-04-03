"""module outils"""
from typing import List, Tuple, Callable, Any
import pygame

# constantes

UNIT_SIZE = 32

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


class Sequence:
    """classe de gestion des séquences"""

    def __init__(self, seq: List[Tuple[Tuple[Callable[..., None], List[Any]] | None, float]],
                 last_call: Tuple[Callable[..., None], List[Any]] = (lambda: None, []), loop: bool = False) -> None:

        self.fnct: List[Tuple[Callable[..., None], List[Any]] | None] = []
        self.times: List[float] = []
        self.is_running = False
        self.sqc_timer = pygame.time.get_ticks()
        self.pointer = 0
        self.loop = loop

        for elm in seq:
            self.fnct.append(elm[0])
            self.times.append(elm[1])

    def start(self):
        """commence la séquence"""
        self.is_running = True
        self.pointer = 0
        self.sqc_timer = pygame.time.get_ticks()

    def fin(self):
        """met fin à la séquence"""
        self.is_running = False

    def update(self):
        """met à jour la séquence"""
        if not self.is_running or (self.times[self.pointer] >
                                   pygame.time.get_ticks() - self.sqc_timer):
            return False

        fnct = self.fnct[self.pointer]
        if fnct is not None:
            fnct[0](*fnct[1])
        self.pointer += 1
        self.sqc_timer = pygame.time.get_ticks()

        if self.pointer >= len(self.times):
            if self.loop:
                self.start()
            else:
                self.is_running = False

        return True

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
