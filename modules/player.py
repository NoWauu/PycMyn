"""module de gestion du joueur"""

from typing import Dict, List, Tuple, Any

import pygame

import modules.outils as utl
from modules import collectable
from modules.entite import CASE, Entity
from modules.graphics import Interface, Sequence
from modules import sounds

pygame.init()


class Player(Entity):
    """gestion du joueur"""

    def __init__(self, pos: pygame.Vector3,
                 textures: Tuple[pygame.Surface,
                                 Dict[str, List[Tuple[pygame.Surface, float]]]]) -> None:
        super().__init__(pos, textures)
        self.rotation: int

        self.idt = 2
        self.reset_pos = pos.xy
        # mouvements
        self.mouvement_dct: Dict[str, Any] = {
            'reset_pos': pos.xy,
            'memoire': 0,
            'direction': -1,
            'base_speed': 80,
            'speed': 80 * float(utl.TABLE[super().niveau if super().niveau <=
                                          20 else 20]['vitesse_pacman']),
            'deltat': 0,
            'last_time': 0
        }

        # gameplay
        self.gameplay_dct: Dict[str, Any] = {
            'health': 3,
            'points': 0,
            'eat_bonus': 0
        }

        # sounds
        self.eat_seq = Sequence([((sounds.EAT_SOUND.play, []), 0),
                                 (None, int(sounds.EAT_SOUND.get_length() * 1000 - 215))])

    def on_keypress(self, event: pygame.event.Event):
        """méthode de traitement des touches"""
        match event.key:
            case pygame.K_LEFT:
                self.mouvement_dct['direction'] = 2
            case pygame.K_RIGHT:
                self.mouvement_dct['direction'] = 0
            case pygame.K_UP:
                self.mouvement_dct['direction'] = 1
            case pygame.K_DOWN:
                self.mouvement_dct['direction'] = 3
            case _:
                ...

    def controle(self) -> None:
        """gestion du déplacement d'une entité"""
        if self.mouvement_dct['direction'] == -1:
            return

        futur = CASE[self.mouvement_dct['direction']](
            self.pos.xy, self.mouvement_dct['speed'], self.mouvement_dct['deltat'])

        # si la direction indiquée convient on avance
        if (not self.collide_wall(futur) and
                not any(enit.hard_collide for enit in
                        self.collide_with(futur))):
            self.pos.xy = futur
            if self.mouvement_dct['memoire'] != self.mouvement_dct['direction']:
                self.mouvement_dct['memoire'] = self.mouvement_dct['direction']

        else:
            futur = CASE[self.mouvement_dct['memoire']](
                self.pos.xy, self.mouvement_dct['speed'], self.mouvement_dct['deltat'])
            # sinon, on regarde dans la mémoire et si
            # celle ci convient, on avance
            if (not self.collide_wall(futur) and
                    not any(enit.hard_collide for enit in
                            self.collide_with(futur))):
                self.pos.xy = futur

    def collect(self, entity: Entity):
        """gestion de la collecte des collectables"""
        if isinstance(entity, collectable.Piece):
            utl.call('add_point', {'point': 1})
            self.gameplay_dct['points'] += 1
            if not self.eat_seq.is_running:
                self.eat_seq.start()

        elif isinstance(entity, collectable.Fruit):
            points = int(utl.TABLE[super().niveau if super().niveau
                                   <= 19 else 20]['points_bonus'])
            utl.call('add_point', {'point': points})
            self.gameplay_dct['points'] += points
            sounds.FRUIT_SOUND.play()

        elif isinstance(entity, collectable.Super):
            utl.call('powerup', {'fear': True})

    def super_pacman(self, fear: bool):
        """change le vitesse"""
        if fear:
            self.mouvement_dct['speed'] = (self.mouvement_dct['base_speed'] *
                                           float(utl.TABLE[super().niveau if super().niveau
                                                           <= 19 else 20]["super_pacman_vitesse"]))
            self.eat_bonus = 200
        else:
            self.mouvement_dct['speed'] = (self.mouvement_dct['base_speed'] *
                                           float(utl.TABLE[super().niveau if super().niveau
                                                           <= 19 else 20]["vitesse_pacman"]))
            self.eat_bonus = 0

    def interact(self):
        """gestion des intéractions avec le joueur"""
        for entity in self.collide_with():
            if entity.idt == 0:
                ancien = self.gameplay_dct['points']
                self.collect(entity)
                entity.destroy()

                # s'il n'y a plus de pièce, on gagne
                if len(collectable.Piece.pieces) == 0:
                    victoire()

                if self.gameplay_dct['points'] >= 10000 > ancien:
                    self.gameplay_dct['health'] += 1
                    utl.call('set_vie', {'nombre': self.gameplay_dct['health']})
                    sounds.EXTRA_SOUND.play()

            elif entity.idt == 1:
                # cas de collision avec un fantome
                if entity.fear_state:
                    entity.reset()
                    utl.call('add_point', {'point': self.eat_bonus})
                    self.eat_bonus *= 2
                    sounds.GHOST_SOUND.play()

                elif self.gameplay_dct['health'] > 1:
                    self.gameplay_dct['health'] -= 1
                    utl.call('set_vie', {'nombre': self.gameplay_dct['health']})
                    utl.call('init_entities', {})
                    sounds.DEATH_SOUND.play()
                    return

                else:
                    defaite()
                    sounds.DEATH_SOUND.play()

    def reset(self):
        """initialise une manche"""
        self.pos.xy = self.reset_pos

    def update(self):
        """met à jour l'entité"""
        self.mouvement_dct['deltat'] = pygame.time.get_ticks() - self.mouvement_dct['last_time']
        self.mouvement_dct['last_time'] = pygame.time.get_ticks()

        save_pos = self.pos.xy
        self.controle()
        self.rotation = (self.mouvement_dct['memoire'] * 90) % 360

        if save_pos != self.pos.xy and not self.animation.seq.is_running:
            self.animation.start_anim('normal')

        self.interact()
        self.eat_seq.step()

# fonction


def victoire():
    """victoire"""
    utl.call('inc_niveau', {'niveau': Entity.niveau + 1})
    utl.call('victoire', {'able': True})
    utl.call('fin_partie', {})
    Interface.change_interface('fin_partie')


def defaite():
    """défaite"""
    utl.call('inc_niveau', {'niveau': 0})
    utl.call('defaite', {'able': True})
    utl.call('fin_partie', {})
    Interface.change_interface('fin_partie')


# setup


def initialisation():
    """initialisation"""
    # textures
    texture_player = pygame.transform.smoothscale(
        pygame.image.load("ressources/textures/pacman.png").convert_alpha(),
        (utl.UNIT_SIZE, utl.UNIT_SIZE))

    texture_player_2 = pygame.Surface(
        (utl.UNIT_SIZE, utl.UNIT_SIZE), pygame.SRCALPHA)
    texture_player_2.fill(pygame.Color(255, 255, 255, 10))
    pygame.draw.circle(texture_player_2, "#FFCC00",
                       (utl.UNIT_SIZE // 2, utl.UNIT_SIZE // 2), utl.UNIT_SIZE // 2)

    # entité
    player = Player(pygame.Vector3(utl.UNIT_SIZE, utl.UNIT_SIZE, 2),
                    (texture_player, {'normal': [(texture_player, 0),
                                                 (texture_player_2, 200),
                                                 (texture_player, 200)]}))
    # événements
    utl.lie('init_entities', player.reset)
    utl.lie('powerup', player.super_pacman)
