import random
from typing import Tuple, List, Dict

import pygame

from modules.classes import Sequence
from modules.outils import UNIT_SIZE
from modules import entite


class Fantome(entite.Entity):
    """gestion des fantomes"""
    fantomes: List['Fantome'] = []

    def __init__(self, position: pygame.Vector3,
                 textures: Tuple[pygame.Surface, Dict[str, List[Tuple[pygame.Surface, float]]]],
                 comportement=None) -> None:
        super().__init__(position, textures)
        # mouvements
        self.start_pos = position.xy
        self.direction: int = 0  # a modifier potentiellement
        self.direction_new: int = self.direction
        self.speed = 1.4

        self.time = 0

        self.fear_state = False
        self.fear_seq = Sequence([((self.set_fear, [False]), 4000)], loop=True)

        self.seq = Sequence(
            [((self.change_direction, []), 5000)], loop=True)
        self.seq.start()

        Fantome.fantomes.append(self)

    def reset(self):
        """reset le fantome lors de sa mort"""
        self.pos.xy = self.start_pos
        self.fear_state = False
        self.animation.reset_anim()

    def fear(self):
        """active la peur chez le fantome"""
        self.animation.start_anim('fear')
        self.fear_seq.start()
        self.fear_state = True

    def calc_directions(self):
        """calcule les différentes directions possibles"""
        return [k for k in range(4) if not self.collide_wall(entite.CASE[k](self.pos.xy, self.speed, self.dt))]

    def change_direction(self):
        """change le fantome de direction"""
        directions = self.calc_directions()
        self.direction_new = choix_direction(directions)

    def move_direction(self, direction: int):
        """bouge dans une direction"""
        futur = entite.CASE[direction](self.pos.xy, self.speed, self.dt)

        if not self.collide_wall(futur):
            self.pos.xy = futur
            return True
        return False

    def contourne_mur(self):
        """fait changer le fantome de direction lorsqu'il rencontre un mur"""
        self.change_direction()
        self.direction = self.direction_new
        self.move_direction(self.direction)

    def controle(self) -> None:
        """gestion du déplacement d'une entité"""
        if self.dt > 50:
            return
        directions = self.calc_directions()

        # on regarde si le fantome se situe sur une intersection
        if len(directions) >= 2:
            # on fait en sorte que le fantome ne revienne pas sur ses pas
            if (self.direction + 2) % 4 in directions:
                directions.remove((self.direction + 2) % 4)
            self.direction_new = choix_direction(directions)
            self.direction_cooldown = 10

        # s'il y a une nouvelle direction, on la met à jour
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

    def set_fear(self, fear: bool):
        """renvoie vrai si le fantome est en état de peur"""
        self.fear_state = fear

    def update(self):
        """mise à jour"""
        self.dt = pygame.time.get_ticks() - self.time
        self.time = pygame.time.get_ticks()

        self.seq.update()
        self.controle()

        self.fear_seq.update()

        if self.fear_state and not self.animation.seq.is_running:
            self.animation.start_anim('fear_blink')


class Porte(entite.Entity):
    """gestion des portes"""

    def __init__(self, position: pygame.Vector3, width: int) -> None:
        texture = pygame.Surface((width, UNIT_SIZE))
        pygame.draw.rect(texture, (250, 175, 90),
                 pygame.rect.Rect(0, (UNIT_SIZE - 4) // 2, width, 4))
        super().__init__(position, (texture, {}))
        self.hard_collide = True


def choix_direction(directions: List[int]):
    """
    renvoie une direction au
    choix parmi celles proposées
    """
    choix = random.choice(directions)
    return choix

'''
def find_exit(fantomes: List[Fantome], porte: Porte):
    """sort les fantomes de la zone de départ"""

    for fantome in fantomes:
        pos = fantome.pos.xy
        pos_porte = porte.pos.xy

        path, succes = path_find(entite.Entity.plateau.element.mask, pos, pos_porte)
        if succes:
            # on crée une séquence que
            # le fantome va suivre
            Sequence()

def path_find(mask: pygame.mask.Mask, pos: pygame.Vector2, fin: pygame.Vector2,
              visited: List[pygame.Vector2] = []) -> Tuple[List[pygame.Vector2], bool]:
    """trouve un chemin depuis le point de départ jusqu'à l'arrivée"""

    if (fin - pos).length_squared() < UNIT_SIZE ** 2:
        return visited, True

    for direction in range(4):
        position = pos + ((1 if direction // 2 == 0 else -1) *
                          (pygame.Vector2(UNIT_SIZE, 0) if direction % 2 == 0 else pygame.Vector2(UNIT_SIZE, 1)))
        res = False
        path = []
        if not mask.get_at(position) and pos not in visited:
            path, res = path_find(mask, start, fin, position, visited + [position])
        
        if res:
            return path, True
    
    return [], False'''

# setup

texture_fantome = pygame.transform.scale(
    pygame.image.load("ressources/textures/blinky.png"), (UNIT_SIZE, UNIT_SIZE))

texture_fantome_fear = pygame.transform.scale(
    pygame.image.load("ressources/textures/stun.png"), (UNIT_SIZE, UNIT_SIZE))
texture_fantome_fear_2 = pygame.transform.scale(
    pygame.image.load("ressources/textures/stun2.png"), (UNIT_SIZE, UNIT_SIZE))
