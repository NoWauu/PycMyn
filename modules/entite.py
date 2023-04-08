"""Module de gestion des Entités"""
from typing import List, Tuple, Dict, Set

import pygame

from modules.classes import AnimElement, Frame, vect2_to_tuple
from modules import plateau
from modules.outils import reste_etendu, UNIT_SIZE

# fonctions de déplacement


def haut(pos: pygame.Vector2, speed: float, dt: float):
    """déplacement vers le haut"""
    return pygame.Vector2(pos.x, round(reste_etendu((pos.y - speed * dt / 10), Frame.frames['plateau'].surface.get_height())))


def bas(pos: pygame.Vector2, speed: float, dt: float):
    """déplacement vers le bas"""
    return pygame.Vector2(pos.x, round(reste_etendu((pos.y + speed * dt / 10), Frame.frames['plateau'].surface.get_height())))


def gauche(pos: pygame.Vector2, speed: float, dt: float):
    """déplacement vers la gauche"""
    return pygame.Vector2(round(reste_etendu((pos.x - speed * dt / 10), Frame.frames['plateau'].surface.get_width())), pos.y)


def droite(pos: pygame.Vector2, speed: float, dt: float):
    """déplacement vers la droite"""
    return pygame.Vector2(round(reste_etendu((pos.x + speed * dt / 10), Frame.frames['plateau'].surface.get_width())), pos.y)


CASE = {1: haut,
        3: bas,
        2: gauche,
        0: droite}


class Entity(pygame.sprite.Sprite):
    """Classe racine des entités"""
    plateau: plateau.Plateau
    group: Set['Entity'] = set()

    def __init__(self, pos: pygame.Vector3, anim_infos: Tuple[pygame.Surface,
                                                              Dict[str, List[Tuple[pygame.Surface, float]]]]) -> None:
        super().__init__()

        self.pos = pos
        self.hard_collide = False

        # renderer
        self.animation = AnimElement(self, anim_infos[0], anim_infos[1], 'plateau')

        Entity.group.add(self)

    @classmethod
    def collide_with_point(cls, point: pygame.Vector2, ignore: List['Entity'] = []) -> List['Entity']:
        """return a liste containing the sprites colliding with the point"""
        for enit in ignore:
            Entity.group.remove(enit)

        collide_ls: List['Entity'] = [
            enit for enit in Entity.group if enit.animation.rect.collidepoint(point)]

        for enit in ignore:
            Entity.group.add(enit)

        return collide_ls

    def collide_with(self, point: pygame.Vector2 | None = None) -> List['Entity']:
        """return a list containing the sprites colliding with this one"""
        Entity.group.remove(self)
        ls: List['Entity'] = []
        
        save_pos = self.animation.rect.topleft
        if point is not None:
                self.animation.rect.topleft = vect2_to_tuple(point)
        for enit in Entity.group:
            if enit.animation.rect.colliderect(self.animation.rect):
                ls.append(enit)
        if point is not None:
            self.animation.rect.topleft = save_pos

        Entity.group.add(self)
        return ls

    def collide_wall(self, pos: pygame.Vector2):
        """Check if the entity collide with walls"""
        # (-pos.x, -pos.y) is used because the top left corner of self.mask
        # is consider to be (0, 0). The wall's mask is therefore shift to the entity
        # Thus, it has to be reshift to (0, 0) world coordinates
        return Entity.plateau.element.mask.overlap(self.animation.mask, (pos.x + UNIT_SIZE, pos.y + UNIT_SIZE)) is not None

    def destroy(self) -> None:
        """détruit l'entité"""
        self.animation.delink()
        Entity.group.remove(self)
        del self.animation
        del self
