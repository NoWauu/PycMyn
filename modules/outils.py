"""module de fonctions partiques"""

from typing import Callable, List, Tuple
import pygame

# constantes

UNIT_SIZE = 32

# fonctions


def reste_etendu(a: float, b: float):
    """renvoie a % b si a >= 0 ou a < -1 et a si -1 <= a < 0"""
    return a % b if a >= 0 or a < -UNIT_SIZE else a


class Sequence:
    """classe de gestion des séquences"""

    def __init__(self, seq: List[Tuple[Callable[..., None], float]], loop: bool = False) -> None:
        self.fnct: List[Callable[..., None]] = []
        self.times: List[float] = []
        self.is_running = False
        self.time = 0
        self.tlf = 0
        self.pointer = 0
        self.loop = loop
        for elm in seq:
            self.fnct.append(elm[0])
            self.times.append(elm[1])

    def start(self):
        """commence la séquence"""
        self.is_running = True

    def fin(self):
        """met fin à la séquence"""
        self.is_running = False

    def update(self):
        """met à jour la séquence"""
        self.dt = (pygame.time.get_ticks() - self.tlf) / 1000
        self.tlf = pygame.time.get_ticks()

        if self.is_running:
            self.time += self.dt

            if self.times[self.pointer] <= self.time:
                self.fnct[self.pointer]()
                self.pointer += 1

            if self.pointer >= len(self.times):
                self.time = 0
                self.pointer = 0
                if not self.loop:
                    self.is_running = False
