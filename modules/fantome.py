import random
from typing import Tuple, List, Dict, Callable

import pygame

from modules.graphics import Sequence
import modules.outils as utl
from modules.entite import Entity, CASE

pygame.init()


class Fantome(Entity):
    """gestion des fantomes"""

    fantomes: List['Fantome'] = []

    def __init__(self, position: pygame.Vector3,
                 textures: Tuple[pygame.Surface, Dict[str, List[Tuple[pygame.Surface, float]]]],
                 comportement_infos: Tuple[Callable[['Fantome', List[int]], int], int]) -> None:
        super().__init__(position, textures)
        self.id = 1
        # mouvements
        self.start_pos = position.xy
        self.direction: int = 1
        self.memoire: int = self.direction
        self.base_speed = 1.2
        self.speed = self.base_speed * \
            float(utl.TABLE[super().niveau if super().niveau <=
                  20 else 21]['vitesse_fantome'])

        self.comportement, periode = comportement_infos

        self.time = 0

        self.fear_state = False
        self.fear_seq = Sequence([((utl.call, ['powerup', {'fear': False}]),
                                   int(utl.TABLE[Fantome.niveau if
                                                 Fantome.niveau <= 20 else 21]['fright_time']) * 1000)])

        self.seq = Sequence(
            [((self.desire_direction, []), periode)], loop=True)

        # on met un delai sur le lancement de la séquence
        self.seq.start()

        Fantome.fantomes.append(self)

    def reset(self):
        """reset le fantome lors de sa mort"""
        self.pos.xy = self.start_pos
        self.fear_state = False
        self.animation.reset_anim()
        self.direction = 1
        self.seq.pause(1500)

    def calc_directions(self):
        """calcule les différentes directions possibles"""
        return [k for k in range(4) if not self.collide_wall(CASE[k](self.pos.xy, self.speed, self.dt))]

    def desire_direction(self):
        """change le fantome de direction"""
        self.direction = self.comportement(self, [0, 1, 2, 3])

    def contourne_mur(self):
        """fait changer le fantome de direction lorsqu'il rencontre un mur"""
        directions = self.calc_directions()
        if directions != []:
            self.direction = self.comportement(self, directions)
            self.memoire = self.direction
        else:
            self.direction = -1
        self.pos.xy = CASE[self.direction](self.pos.xy, self.speed, self.dt)

    def controle(self) -> None:
        """gestion du déplacement d'une entité"""
        if self.dt > 50:
            return

        # on teste d'abord la direction désirée
        futur = CASE[self.direction](self.pos.xy, self.speed, self.dt)
        if not self.collide_wall(futur):
            self.pos.xy = futur
            self.memoire = self.direction
            return

        new_direction = -1
        directions = self.calc_directions()
        print(directions)

        # on regarde si le fantome se situe sur une intersection
        if len(directions) >= 2:
            # on fait en sorte que le fantome ne revienne pas sur ses pas
            if (self.memoire + 2) % 4 in directions:
                directions.remove((self.memoire + 2) % 4)
            new_direction = self.comportement(self, directions)
        elif len(directions) > 0:
            new_direction = directions[0]

        # s'il y a une nouvelle direction, on met à jour la position
        if new_direction != -1:
            futur = CASE[new_direction](self.pos.xy, self.speed, self.dt)
            self.pos.xy = futur

            self.memoire = new_direction

    def set_fear(self, fear: bool):
        """renvoie vrai si le fantome est en état de peur"""
        self.fear_state = fear

        if self.fear_state:
            self.speed = float(utl.TABLE[super().niveau
                                         if super().niveau <= 20 else 21]['fright_ghost_vitesse']) * \
                self.base_speed
            self.animation.start_anim('fear')
            self.fear_seq.start()
        else:
            self.speed = self.base_speed * \
                float(utl.TABLE[super().niveau if super(
                ).niveau <= 20 else 21]['vitesse_fantome'])

    def destroy(self) -> None:
        Fantome.fantomes.remove(self)
        super().destroy()

    def update(self):
        """mise à jour"""
        self.dt = pygame.time.get_ticks() - self.time
        self.time = pygame.time.get_ticks()

        self.seq.update()
        self.controle()

        self.fear_seq.update()

        if self.fear_state and not self.animation.seq.is_running:
            self.animation.start_anim('fear_blink')


class Porte(Entity):
    """gestion des portes"""

    def __init__(self, position: pygame.Vector3, width: int) -> None:
        texture = pygame.Surface((width, utl.UNIT_SIZE))
        pygame.draw.rect(texture, (250, 175, 90),
                         pygame.rect.Rect(0, (utl.UNIT_SIZE - 4) // 2, width, 4))
        super().__init__(position, (texture, {}))
        self.hard_collide = True
        self.id = 3

# fonctions


def find_joueur():
    """trouve le joueur"""
    return [enit for enit in Entity.group if enit.id == 2][0]

# comportements


def aleatoire(fantome: Fantome, directions: List[int]):
    """
    renvoie une direction au
    hazard parmi celles proposées
    """
    choix = random.choice(directions)
    return choix


def follow(fantome: Fantome, directions: List[int]):
    """
    renvoie une direction au
    choix parmi celles proposées
    """
    player = find_joueur()

    direct = (player.pos.xy - fantome.pos.xy).normalize()
    produits_scalaires = [((direction % 2 == 0) * (-(direction // 2) * 2 + 1) * direct.x +
                           (direction % 2 == 1) * ((direction // 2) * 2 - 1) * direct.y) for direction in directions]
    return directions[produits_scalaires.index(max(produits_scalaires))]


# setup


def initialisation():
    """initialisation des fantomes"""
    # textures
    texture_blinky = pygame.transform.scale(
        pygame.image.load("ressources/textures/blinky.png").convert_alpha(), (utl.UNIT_SIZE, utl.UNIT_SIZE))
    texture_inky = pygame.transform.scale(
        pygame.image.load("ressources/textures/inky.png").convert_alpha(), (utl.UNIT_SIZE, utl.UNIT_SIZE))

    texture_fantome_fear = pygame.transform.scale(
        pygame.image.load("ressources/textures/stun.png").convert_alpha(), (utl.UNIT_SIZE, utl.UNIT_SIZE))
    texture_fantome_fear_2 = pygame.transform.scale(
        pygame.image.load("ressources/textures/stun2.png").convert_alpha(), (utl.UNIT_SIZE, utl.UNIT_SIZE))

    # entités

    blinky = Fantome(pygame.Vector3(192, 224, 2), (texture_blinky, {'fear': [(texture_fantome_fear, 0),
                                                                             (texture_fantome_fear, 3000)],
                                                                    'fear_blink': [(texture_fantome_fear, 0),
                                                                                   (texture_fantome_fear_2, 200),
                                                                                   (texture_blinky, 200)]}),
                     (aleatoire, 5000))
    inky = Fantome(pygame.Vector3(192, 224, 2), (texture_inky, {'fear': [(texture_fantome_fear, 0),
                                                                         (texture_fantome_fear, 3000)],
                                                                'fear_blink': [(texture_fantome_fear, 0),
                                                                               (texture_fantome_fear_2, 200),
                                                                               (texture_inky, 200)]}),
                   (follow, 1000))
    Porte(pygame.Vector3(208, 196, 1), 32)

    # événements
    utl.lie('init_entities', blinky.reset)
    utl.lie('powerup', blinky.set_fear)

    utl.lie('init_entities', inky.reset)
    utl.lie('powerup', inky.set_fear)
