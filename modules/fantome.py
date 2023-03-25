import random
from typing import Tuple, List

import pygame

from modules import outils
from modules import entite


class Fantome(entite.Entity):
    fantomes: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self, position: Tuple[int, int], textures: Tuple[pygame.Surface, List[pygame.Surface], List[float]], comportement=None) -> None:
        super().__init__(position, textures, 'fantome')
        # mouvements
        self.start_pos = position
        self.direction: int = 0  # a modifier potentiellement
        self.direction_new: int = self.direction
        self.tester = []
        self.speed = 1.4

        self.tlf = 0

        self.fear_state = False

        self.add(Fantome.fantomes)
        self.seq = outils.Sequence([(self.change_direction, 5)], True)
        self.seq.start()

    def reset(self):
        """reset le fantome lors de sa mort"""
        self.position = self.start_pos
        self.fear_state = False
        self.animation.reset_anim()

    def fear(self):
        """active la peur chez le fantome"""
        self.animation.start_anim()
        self.fear_state = True

    def calc_directions(self):
        """calcule les différentes directions possibles"""
        self.directions = [k for k in range(4) if not self.collide_wall(entite.CASE[k](self.position, self.speed, self.dt))]

    def change_direction(self):
        """change le fantome de direction"""
        self.calc_directions()
        self.direction_new = choix_direction(self.directions)

    def move_direction(self, direction: int):
        """bouge dans une direction"""
        futur = entite.CASE[direction](self.position, self.speed, self.dt)

        if not self.collide_wall(futur):
            self.position = futur
            return True
        return False

    def contourne_mur(self):
        """fait changer le fantome de direction lorsqu'il rencontre un mur"""
        self.change_direction()
        self.direction = self.direction_new
        self.move_direction(self.direction)

    def controle(self) -> None:
        """gestion du déplacement d'une entité"""
        self.calc_directions()
        
        # on regarde si le fantome se situe sur une intersection
        if len(self.directions) >= 2:
            # on fait en sorte que le fantome ne revienne pas sur ses pas
            if (self.direction + 2)%4 in self.directions:
                self.directions.remove((self.direction + 2)%4)
            self.direction_new = choix_direction(self.directions)

        # si il y a une nouvelle direction, on la met à jour
        if self.direction_new != -1:
            self.move_direction(self.direction_new)
            self.direction = self.direction_new
            self.direction_new = -1
        else:
            # sinon, on continue dans la même direction
            res = self.move_direction(self.direction)

            # si on rencontre un mur
            # on change de direction
            if not res:
                self.contourne_mur()
            

    def isFearing(self) -> bool:
        """renvoie vrai si le fantome est en état de peur"""
        return self.fear_state

    def update(self, event: List[pygame.event.Event]):
        self.dt = (pygame.time.get_ticks() - self.tlf) / 1000
        self.tlf = pygame.time.get_ticks()

        self.seq.update()
        self.controle()
        self.rect.topleft = self.position

        self.update_texture()

        if not self.animation.is_in_animation:
            self.fear_state = False


class Porte(entite.Entity):
    """gestion des portes"""

    def __init__(self, position: Tuple[float, float], texture: pygame.Surface) -> None:
        super().__init__(position, (texture, [], []), 'porte', priority=0)
        self.hard_collide = True


def choix_direction(directions: List[int]):
    choix = random.choice(directions)
    return choix
