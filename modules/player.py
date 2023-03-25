import pygame
from typing import Tuple, List
from modules import entite, collectable, fantome

# constante

KEYBINDS = {pygame.K_UP: 1, pygame.K_DOWN: 3,
            pygame.K_LEFT: 2, pygame.K_RIGHT: 0}


class Player(entite.Entity):
    def __init__(self, position: Tuple[int, int], textures: Tuple[pygame.Surface, List[pygame.Surface], List[float]], speed: float) -> None:
        super().__init__(position, textures, 'player')
        # mouvements
        self.mem: int = -1
        self.direction: int = 0  # a modifier potentiellement
        self.speed = speed

        self.tlf = pygame.time.get_ticks()

        self.health = 3
        self.points = 0

    def controle(self, event: List[pygame.event.Event]) -> None:
        """gestion du déplacement d'une entité"""
        direction: int = -1
        for e in event:
            if e.type == pygame.KEYDOWN and e.key in KEYBINDS:
                direction = KEYBINDS[e.key]

        if direction == -1 and self.mem == -1:
            direction = self.direction

        if direction == -1 and self.mem != -1:
            direction = self.mem

        futur = entite.CASE[direction](self.position, self.speed, self.dt)

        if (not self.collide_wall(futur) and
                not any([enit.hard_collide for enit in
                         self.collide_with_point(futur, self.rect, ignore=[self])])):
            self.position = futur
            self.direction = direction
            self.mem = direction

            if not self.animation.is_in_animation:
                self.animation.start_anim()

        else:
            futur = entite.CASE[self.direction](self.position, self.speed, self.dt)
            if (not self.collide_wall(futur) and
                    not any([enit.hard_collide for enit in
                             self.collide_with_point(futur, self.rect, ignore=[self])])):
                self.position = futur
                self.mem = direction

                if not self.animation.is_in_animation:
                    self.animation.start_anim()

    def collect(self, id: str):
        """gestion de la collecte des collectables"""
        if id == 'piece':
            self.points += 1

        elif id == 'pomme':
            ...

        elif id == 'super':
            self.animation.start_anim()

            for entity in fantome.Fantome.fantomes:
                entity.fear()

    def interact(self):
        """gestion des intéractions avec le joueur"""
        for entity in self.collide_with():
            if isinstance(entity, collectable.Collectable):
                self.collect(entity.id)
                entity.destroy()

            elif isinstance(entity, fantome.Fantome):
                if entity.isFearing():
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
        self.position = (32, 32)

    def update_rotation(self, anc_dir: int):
        """met à jour la rotation de l'entité"""
        # rotatation selon la direction
        self.image = pygame.transform.rotate(
            self.image, (self.direction - anc_dir) * 90)

    def update_texture(self):
        """met à jour la texture de l'entité"""
        image, change = self.animation.check_next_anim()

        if change:
            self.image = pygame.transform.rotate(
                image, self.direction * 90)
            # self.mask = pygame.mask.from_threshold(
            #    self.image, (255, 255, 255), (254, 254, 254, 255))
            #self.rect = self.image.get_rect(topleft=self.position)

    def update(self, event: List[pygame.event.Event]):
        """met à jour l'entité"""
        self.dt = (pygame.time.get_ticks() - self.tlf) / 1000
        self.tlf = pygame.time.get_ticks()
        anc_dir = self.direction

        self.controle(event)
        self.rect.topleft = self.position

        self.update_rotation(anc_dir)

        self.interact()

        self.update_texture()
