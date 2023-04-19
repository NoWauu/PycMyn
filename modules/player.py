from typing import Dict, List, Tuple

import pygame

import modules.outils as utl
from modules import collectable
from modules.entite import CASE, Entity, clear
from modules.graphics import Interface

pygame.init()


class Player(Entity):

    def __init__(self, pos: pygame.Vector3, textures: Tuple[pygame.Surface, Dict[str, List[Tuple[pygame.Surface, float]]]],
                 speed: float) -> None:
        super().__init__(pos, textures)
        self.id = 2
        self.reset_pos = pos.xy
        # mouvements
        self.mem: int = 0
        self.direction: int = -1
        self.base_speed = speed
        self.speed = self.base_speed * \
            float(utl.TABLE[super().niveau if super().niveau <=
                  20 else 20]['vitesse_pacman'])

        self.time_since_last_frame = pygame.time.get_ticks()

        self.health = 3
        self.points = 0

    def on_keypress(self, event: pygame.event.Event):
        """méthode de traitement des touches"""
        match event.key:
            case pygame.K_LEFT:
                self.direction = 2
            case pygame.K_RIGHT:
                self.direction = 0
            case pygame.K_UP:
                self.direction = 1
            case pygame.K_DOWN:
                self.direction = 3
            case _:
                ...

    def controle(self) -> None:
        """gestion du déplacement d'une entité"""
        if self.direction == -1:
            return

        futur = CASE[self.direction](self.pos.xy, self.speed, self.dt)

        # si la direction indiquée convient on avance
        if (not self.collide_wall(futur) and
                not any([enit.hard_collide for enit in
                         self.collide_with(futur)])):
            self.pos.xy = futur
            if self.mem != self.direction:
                self.mem = self.direction

        else:
            futur = CASE[self.mem](self.pos.xy, self.speed, self.dt)
            # sinon, on regarde dans la mémoire et si
            # celle ci convient, on avance
            if (not self.collide_wall(futur) and
                    not any([enit.hard_collide for enit in
                             self.collide_with(futur)])):
                self.pos.xy = futur
            else:
                futur = CASE[self.mem](self.pos.xy, 10/self.dt, self.dt)
                # si on peut tout de même avancer légèrement
                # on avance de 1 pixel
                if not self.collide_wall(futur):
                    self.pos.xy = futur

    def collect(self, entity: Entity):
        """gestion de la collecte des collectables"""
        if isinstance(entity, collectable.Piece):
            utl.call('add_point', {'point': 1})
            self.points += 1

        elif isinstance(entity, collectable.Fruit):
            points = int(utl.TABLE[super().niveau if super().niveau
                                                          <= 19 else 20]['points_bonus'])
            utl.call('add_point', {'point': points})
            self.points += points

        elif isinstance(entity, collectable.Super):
            utl.call('powerup', {'fear': True})

    def change_speed(self, fear: bool):
        """change le vitesse"""
        if fear:
            self.speed = self.base_speed * float(utl.TABLE[super().niveau if super().niveau
                                                           <= 19 else 20]["super_pacman_vitesse"])
        else:
            self.speed = self.base_speed * float(utl.TABLE[super().niveau if super().niveau
                                                           <= 19 else 20]["vitesse_pacman"])

    def interact(self):
        """gestion des intéractions avec le joueur"""
        for entity in self.collide_with():
            if entity.id == 0:
                ancien = self.points
                self.collect(entity)
                entity.destroy()

                # s'il n'y a plus de pièce, on gagne
                if len(collectable.Piece.pieces) == 0:
                    victoire()
                
                if self.points >= 10000 and ancien < 10000:
                    self.health += 1
                    utl.call('set_vie', {'nombre': self.health})

            elif entity.id == 1:
                # cas de collision avec un fantome
                if entity.fear_state:
                    entity.reset()

                elif self.health > 1:
                    self.health -= 1
                    utl.call('set_vie', {'nombre': self.health})
                    utl.call('init_entities', {})

                else:
                    defaite()

    def reset(self):
        """initialise une manche"""
        self.pos.xy = self.reset_pos

    def update(self):
        """met à jour l'entité"""
        self.dt = pygame.time.get_ticks() - self.time_since_last_frame
        self.time_since_last_frame = pygame.time.get_ticks()
        save_pos = self.pos.xy
        self.controle()
        self.rotation = (self.mem * 90) % 360

        if save_pos != self.pos.xy and not self.animation.seq.is_running:
            self.animation.start_anim('normal')

        self.interact()

# fonction


def victoire():
    """victoire"""
    clear()
    utl.call('inc_niveau', {'niveau': Entity.niveau + 1})
    Interface.change_interface('menu')


def defaite():
    """défaite"""
    clear()
    utl.call('inc_niveau', {'niveau': 0})
    Interface.change_interface('menu')


# setup


def initialisation():
    """initialisation"""
    # textures
    texture_player = pygame.transform.smoothscale(
        pygame.image.load("ressources/textures/pacman.png").convert_alpha(), (utl.UNIT_SIZE, utl.UNIT_SIZE))

    texture_player_2 = pygame.Surface(
        (utl.UNIT_SIZE, utl.UNIT_SIZE), pygame.SRCALPHA)
    texture_player_2.fill(pygame.Color(255, 255, 255, 10))
    pygame.draw.circle(texture_player_2, "#FFCC00",
                       (utl.UNIT_SIZE // 2, utl.UNIT_SIZE // 2), utl.UNIT_SIZE // 2)

    # entité
    player = Player(pygame.Vector3(utl.UNIT_SIZE, utl.UNIT_SIZE, 2), (texture_player, {'normal': [(texture_player, 0),
                                                                                                  (texture_player_2, 200),
                                                                                                  (texture_player, 200)]}), 1)
    # événements
    utl.lie('init_entities', player.reset)
    utl.lie('powerup', player.change_speed)
