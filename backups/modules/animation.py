"""module d'animation"""

from enum import auto
from typing import List, Tuple

import pygame


class Animation:
    """classe de gestion des animations"""

    def __init__(self, default_texture: pygame.Surface, textures: List[pygame.Surface], times: List[float]) -> None:
        """infos: temps en millisecondes"""
        self.id = auto()

        self.default_texture = default_texture
        self.textures = textures
        self.times = times
        self.valide_start = True

        if len(self.textures) != len(self.times):
            raise ValueError

        self.anim_index: int
        self.is_in_animation = False

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
