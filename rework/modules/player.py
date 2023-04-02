import pygame
from typing import Tuple, List, Dict
from modules.entite import Entity, CASE
from modules import collectable, fantome


class Player(Entity):
    def __init__(self, pos: pygame.Vector3, textures: Tuple[pygame.Surface, Dict[str, List[pygame.Surface]],
                                                            Dict[str, List[float]]], speed: float) -> None:
        super().__init__(pos, textures)
        # mouvements
        self.mem: int = 0
        self.direction: int = -1
        self.speed = speed

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

        if (not self.collide_wall(futur) and
                not any([enit.hard_collide for enit in
                         self.collide_with(futur)])):
            self.pos.xy = futur
            if self.mem != self.direction:
                self.mem = self.direction

        else:
            futur = CASE[self.mem](self.pos.xy, self.speed, self.dt)
            if (not self.collide_wall(futur) and
                    not any([enit.hard_collide for enit in
                             self.collide_with(futur)])):
                self.pos.xy = futur

    def collect(self, entity: Entity):
        """gestion de la collecte des collectables"""
        if isinstance(entity, collectable.Piece):
            self.points += 1

        elif isinstance(entity, collectable.Pomme):
            ...

        elif isinstance(entity, collectable.Super):
            for entity in fantome.Fantome.fantomes:
                entity.fear()

    def interact(self):
        """gestion des intéractions avec le joueur"""
        for entity in self.collide_with():
            if isinstance(entity, collectable.Collectable):
                self.collect(entity)
                entity.destroy()

            elif isinstance(entity, fantome.Fantome):
                if entity.is_fearing():
                    entity.reset()

                elif self.health > 1:
                    self.health -= 1
                    self.reset()

                else:
                    self.destroy()

    def reset(self):
        """initialise une manche"""
        for enit in fantome.Fantome.fantomes:
            enit.reset()
        self.pos.xy = pygame.Vector2(32, 32)

    def update(self):
        """met à jour l'entité"""
        self.dt = pygame.time.get_ticks() - self.time_since_last_frame
        self.time_since_last_frame = pygame.time.get_ticks()
        save_pos = self.pos.xy
        self.controle()
        self.rotation = (self.mem * 90) % 360

        if save_pos != self.pos.xy and not self.animation.is_in_animation:
            self.animation.start_anim('normal')

        self.interact()
