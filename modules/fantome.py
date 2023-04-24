"""module de gestion des fantômes"""

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
    fantome_map = pygame.mask.from_surface(
        pygame.image.load('ressources/textures/fantome_map.png'))

    def __init__(self, position: pygame.Vector3,
                 textures: Tuple[pygame.Surface,
                                 Dict[str, List[Tuple[pygame.Surface, float]]]],
                 comportement_infos: Tuple[Callable[['Fantome',
                                                     List[int]], int], int]) -> None:
        super().__init__(position, textures)
        self.idt = 1
        # mouvements
        self.start_pos = position.xy
        self.direction: int = 1
        self.memoire: int = self.direction
        self.base_speed = 80
        self.speed = self.base_speed * \
            float(utl.TABLE[super().niveau if super().niveau <=
                  20 else 20]['vitesse_fantome'])

        self.base_comportement, periode = comportement_infos
        self.comportement = self.base_comportement

        self.has_hard_collide = False

        self.time = 0
        self.deltat: int

        self.fear_state = False
        self.fear_seq = Sequence([((utl.call, ['powerup', {'fear': False}]),
                                   int(utl.TABLE[Fantome.niveau if
                                                 Fantome.niveau <= 19 else 20]['fright_time'])
                                   * 1000)])

        self.seq = Sequence(
            [((self.desire_direction, []), periode)], loop=True)

        # on met un delai sur le lancement de la séquence
        self.seq.start()

        Fantome.fantomes.append(self)

    def reset(self):
        """reset le fantome lors de sa mort"""
        self.pos.xy = self.start_pos
        self.set_fear(False)
        self.animation.reset_anim()
        self.direction = 1
        self.seq.pause(1500)

    def calc_directions(self):
        """calcule les différentes directions possibles"""
        directions: List[int] = []
        for k in range(4):
            if not (self.collide_wall(CASE[k](self.pos.xy, self.speed, self.deltat))
                    or (self.has_hard_collide and
                        any(enit.hard_collide for enit in
                            self.collide_with(CASE[k](self.pos.xy,
                                                      self.speed, self.deltat))))):
                directions.append(k)
        return directions

    def desire_direction(self):
        """change le fantome de direction"""
        self.direction = self.comportement(self, [0, 1, 2, 3])

    def contourne_mur(self):
        """fait changer le fantome de direction lorsqu'il rencontre un mur"""
        directions = self.calc_directions()
        if directions:
            self.direction = self.comportement(self, directions)
            self.memoire = self.direction
        else:
            self.direction = -1
        self.pos.xy = CASE[self.direction](self.pos.xy, self.speed, self.deltat)

    def controle(self) -> None:
        """gestion du déplacement d'une entité"""
        # le fantome ne peut que sortir de la zone
        if (0 < self.animation.rect.centerx < Fantome.fantome_map.get_size()[0] and
                Fantome.fantome_map.overlap(self.animation.mask,
                                            self.animation.pos.xy) is not None):
            self.has_hard_collide = False
        else:
            self.has_hard_collide = True

        if self.deltat > 50:
            return

        # on teste d'abord la mémoire
        futur = CASE[self.direction](self.pos.xy, self.speed, self.deltat)
        if not self.collide_wall(futur) and not (self.has_hard_collide and
                                                 any(enit.hard_collide for enit in
                                                     self.collide_with(futur))):
            self.pos.xy = futur
            self.memoire = self.direction
            return

        # on teste ensuite la mémoire désirée
        futur = CASE[self.memoire](self.pos.xy, self.speed, self.deltat)
        if not self.collide_wall(futur) and not (self.has_hard_collide and
                                                 any(enit.hard_collide for enit
                                                     in self.collide_with(futur))):
            self.pos.xy = futur
            return

        new_direction = -1
        directions = self.calc_directions()

        # on regarde si le fantome se situe sur une intersection
        if len(directions) >= 2:
            # on fait en sorte que le fantome ne revienne pas sur ses pas
            if (self.memoire + 2) % 4 in directions:
                directions.remove((self.memoire + 2) % 4)
            new_direction = self.comportement(self, directions)

        # s'il n'y a qu'une direction, on repart
        elif len(directions) > 0:
            new_direction = directions[0]
            Sequence(
                [((setattr, [self, 'direction', self.direction]), 200)],
                local=True).start()
            self.direction = new_direction

        # s'il y a une nouvelle direction, on met
        # à jour la position et la mémoire
        if new_direction != -1:
            futur = CASE[new_direction](self.pos.xy, self.speed, self.deltat)
            self.pos.xy = futur
            self.memoire = new_direction

    def set_fear(self, fear: bool):
        """active ou désactive le comportement de peur"""
        self.fear_state = fear

        if self.fear_state:
            self.speed = (float(utl.TABLE[super().niveau if super().niveau <= 19
                                          else 20]['fright_ghost_vitesse']) *
                          self.base_speed)
            self.animation.start_anim('fear')
            self.fear_seq.start()
            self.comportement = evite
        else:
            self.speed = (self.base_speed *
                          float(utl.TABLE[super().niveau if super(
                          ).niveau <= 19 else 20]['vitesse_fantome']))
            self.animation.reset_anim()
            self.comportement = self.base_comportement

    def destroy(self) -> None:
        Fantome.fantomes.remove(self)
        super().destroy()

    def update(self):
        """mise à jour"""
        self.deltat = pygame.time.get_ticks() - self.time
        self.time = pygame.time.get_ticks()

        self.seq.step()
        self.controle()

        self.fear_seq.step()

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
        self.idt = 3

# fonctions


def find_joueur():
    """trouve le joueur"""
    return [enit for enit in Entity.group if enit.idt == 2][0]

# comportements


def aleatoire(_: Fantome, directions: List[int]):
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

    vector = player.pos.xy - fantome.pos.xy
    direct = vector.normalize() if vector.length() != 0 else vector
    produits_scalaires = [utl.gen_vector(
        direction).dot(direct) for direction in directions]
    return directions[produits_scalaires.index(max(produits_scalaires))]


def evite(fantome: Fantome, directions: List[int]):
    """évite pacman"""
    player = find_joueur()
    vector = player.pos.xy - fantome.pos.xy

    direct = vector.normalize()
    produits_scalaires = [utl.gen_vector(
        direction).dot(direct) for direction in directions]

    return directions[produits_scalaires.index(min(produits_scalaires))]


def piege(fantome: Fantome, directions: List[int]):
    """
    renvoie une direction au
    choix parmi celles proposées
    """
    player = find_joueur()
    coef_dir = 4
    coef_dst = 3

    if player.mouvement_dct['memoire'] == -1:
        return follow(fantome, directions)

    vector: pygame.Vector2 = (player.pos.xy + (coef_dir * utl.UNIT_SIZE *
                                               utl.gen_vector(player.mouvement_dct['memoire']) -
                                               fantome.pos.xy))

    if vector.length() < utl.UNIT_SIZE * coef_dst:
        direct = player.pos.xy - fantome.pos.xy

    direct = vector.normalize() if vector.length() != 0 else vector
    produits_scalaires = [utl.gen_vector(direction).dot(direct)
                          for direction in directions]

    return directions[produits_scalaires.index(max(produits_scalaires))]


# setup


def initialisation():
    """initialisation des fantomes"""
    # textures
    texture_blinky = pygame.transform.scale(
        pygame.image.load("ressources/textures/blinky.png").convert_alpha(),
        (utl.UNIT_SIZE, utl.UNIT_SIZE))
    texture_clyde = pygame.transform.scale(
        pygame.image.load("ressources/textures/clyde.png").convert_alpha(),
        (utl.UNIT_SIZE, utl.UNIT_SIZE))
    texture_inky = pygame.transform.scale(
        pygame.image.load("ressources/textures/inky.png").convert_alpha(),
        (utl.UNIT_SIZE, utl.UNIT_SIZE))
    texture_pinky = pygame.transform.scale(
        pygame.image.load("ressources/textures/pinky.png").convert_alpha(),
        (utl.UNIT_SIZE, utl.UNIT_SIZE))

    texture_fantome_fear = pygame.transform.scale(
        pygame.image.load("ressources/textures/stun.png").convert_alpha(),
        (utl.UNIT_SIZE, utl.UNIT_SIZE))
    texture_fantome_fear_2 = pygame.transform.scale(
        pygame.image.load("ressources/textures/stun2.png").convert_alpha(),
        (utl.UNIT_SIZE, utl.UNIT_SIZE))

    # entités
    blinky = Fantome(pygame.Vector3(192, 224, 2),
                     (texture_blinky,
                      {'fear': [(texture_fantome_fear, 0),
                                (texture_fantome_fear,
                                 max(int(utl.TABLE[Fantome.niveau
                                                   if Fantome.niveau <= 19 else 20]['fright_time'])
                                     * 1000 -
                                     int(utl.TABLE[Fantome.niveau
                                                   if Fantome.niveau <= 19 else 20]['nb_flashes'])
                                     * 400, 0))],
                       'fear_blink': [(texture_fantome_fear, 0),
                                      (texture_fantome_fear_2, 200),
                                      (texture_blinky, 200)]}),
                     (follow, 1000))
    clyde = Fantome(pygame.Vector3(192, 224, 2),
                    (texture_clyde,
                     {'fear': [(texture_fantome_fear, 0),
                               (texture_fantome_fear,
                                max(int(utl.TABLE[Fantome.niveau
                                                  if Fantome.niveau <= 19 else 20]['fright_time'])
                                    * 1000 -
                                    int(utl.TABLE[Fantome.niveau
                                                  if Fantome.niveau <= 19 else 20]['nb_flashes'])
                                    * 400, 0))],
                      'fear_blink': [(texture_fantome_fear, 0),
                                     (texture_fantome_fear_2, 200),
                                     (texture_clyde, 200)]}),
                    (aleatoire, 1000))
    inky = Fantome(pygame.Vector3(192, 224, 2),
                   (texture_inky,
                    {'fear': [(texture_fantome_fear, 0),
                              (texture_fantome_fear,
                               max(int(utl.TABLE[Fantome.niveau
                                                 if Fantome.niveau <= 19 else 20]['fright_time'])
                                   * 1000 -
                                   int(utl.TABLE[Fantome.niveau
                                                 if Fantome.niveau <= 19 else 20]['nb_flashes'])
                                   * 400, 0))],
                     'fear_blink': [(texture_fantome_fear, 0),
                                    (texture_fantome_fear_2, 200),
                                    (texture_inky, 200)]}),
                   (evite, 1000))

    pinky = Fantome(pygame.Vector3(192, 224, 2),
                    (texture_pinky,
                     {'fear': [(texture_fantome_fear, 0),
                               (texture_fantome_fear,
                                max(int(utl.TABLE[Fantome.niveau
                                                  if Fantome.niveau <= 19 else 20]['fright_time'])
                                    * 1000 -
                                    int(utl.TABLE[Fantome.niveau
                                                  if Fantome.niveau <= 19 else 20]['nb_flashes'])
                                    * 400, 0))],
                      'fear_blink': [(texture_fantome_fear, 0),
                                     (texture_fantome_fear_2, 200),
                                     (texture_pinky, 200)]}),
                    (piege, 1000))

    Porte(pygame.Vector3(208, 196, 1), 32)

    # événements
    utl.lie('init_entities', blinky.reset)
    utl.lie('powerup', blinky.set_fear)

    utl.lie('init_entities', clyde.reset)
    utl.lie('powerup', clyde.set_fear)

    utl.lie('init_entities', inky.reset)
    utl.lie('powerup', inky.set_fear)

    utl.lie('init_entities', pinky.reset)
    utl.lie('powerup', pinky.set_fear)
