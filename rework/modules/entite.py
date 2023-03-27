"""Module de gestion des Entités"""
from typing import List, Tuple

import pygame

from modules import animation, plateau
from modules.outils import reste_etendu, UNIT_SIZE

# constantes
# introduit un bug lors du reset du joueur

# fonctions de déplacement


def haut(pos: Tuple[int, int], speed: float, dt: float):
    """déplacement vers le haut"""
    return (pos[0], round(reste_etendu((pos[1] - speed * dt * 100), Entity.plateau.ecran.get_height())))


def bas(pos: Tuple[int, int], speed: float, dt: float):
    """déplacement vers le bas"""
    return (pos[0], round(reste_etendu((pos[1] + speed * dt * 100), Entity.plateau.ecran.get_height())))


def gauche(pos: Tuple[int, int], speed: float, dt: float):
    """déplacement vers la gauche"""
    return (round(reste_etendu((pos[0] - speed * dt * 100), Entity.plateau.ecran.get_width())), pos[1])


def droite(pos: Tuple[int, int], speed: float, dt: float):
    """déplacement vers la droite"""
    return (round(reste_etendu((pos[0] + speed * dt * 100), Entity.plateau.ecran.get_width())), pos[1])


CASE = {1: haut,
        3: bas,
        2: gauche,
        0: droite}


class priorityGroup(pygame.sprite.Group):
    def sort_priority(self, entity: 'Entity'):
        return entity.priority

    def draw(self, surface: pygame.Surface):
        sprites = self.sprites()
        for sprite in sorted(sprites, key=self.sort_priority):
            self.spritedict[sprite] = surface.blit(sprite.image, sprite.rect)
        self.lostsprites = []
        return list(self.spritedict.values())


class Entity(pygame.sprite.Sprite):
    """Classe racine des entités"""
    group = priorityGroup()
    plateau: plateau.Plateau

    def __init__(self, position: Tuple[float, float], textures: Tuple[pygame.Surface, List[pygame.Surface], List[float]], id: str, priority: int = 1) -> None:
        super().__init__()
        self.id = id
        self.priority = priority

        self.position = position

        self.animation = animation.Animation(
            textures[0], textures[1], textures[2])
        self.image = self.animation.default_texture

        self.mask = pygame.mask.from_threshold(
            self.image, (255, 255, 255), (200, 200, 200, 255))  # pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=self.position)

        self.hard_collide = False

        self.add(Entity.group)

    def collide_with_point(self, point: Tuple[int, int], rect: pygame.rect.Rect, ignore: List[pygame.sprite.Sprite] = []) -> List['Entity']:
        """return a liste containing the sprites colliding with the point"""
        for enit in ignore:
            Entity.group.remove(enit)

        rect.center = point

        collide_ls = [
            enit for enit in Entity.group if enit.rect.colliderect(rect)]

        for enit in ignore:
            Entity.group.add(enit)

        return collide_ls

    def collide_with(self) -> List['Entity']:
        """return a list containing the sprites colliding with this one"""
        Entity.group.remove(self)
        ls = pygame.sprite.spritecollide(self, Entity.group, False)
        Entity.group.add(self)
        return ls

    def collide_wall(self, pos: Tuple[int, int]):
        """Check if the entity collide with walls"""
        # (-pos[0], -pos[1]) is used because the top left corner of self.mask
        # is consider to be (0, 0). The wall's mask is therefore shift to the entity
        # Thus, it has to be reshift to (0, 0) world coordinates
        return self.mask.overlap(Entity.plateau.mask, (-pos[0] - UNIT_SIZE, -pos[1] - UNIT_SIZE)) is not None

    def update_texture(self):
        """met à jour la texture de l'entité"""
        image, change = self.animation.check_next_anim()

        if change:
            self.image = image
            self.mask = pygame.mask.from_threshold(
                self.image, (255, 255, 255), (254, 254, 254, 255))
            self.rect = self.image.get_rect(topleft=self.position)

    def destroy(self) -> None:
        """détruit l'entité"""
        self.kill()
        del self
