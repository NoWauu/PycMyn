"""Module de gestion des Entités"""
from typing import List

import enum
import pygame

class Entity(pygame.sprite.Sprite):
    """Classe racine des entités"""
    group = pygame.sprite.Group()
    screen = None
    

    def __init__(self, position, textures) -> None:
        super().__init__()
        self.id = enum.auto()
        self.position = position
        self.textures : List[pygame.Surface] = textures
        
        self.image = self.textures[0]
        self.rect = self.image.get_rect(center=self.position)

        self.add(Entity.group)  

    def collide_with(self) -> List:
        """renvoie la liste des sprites rentrant en collision avec celui-ci"""
        Entity.group.remove(self)
        ls =  pygame.sprite.spritecollide(self, Entity.group, False)
        Entity.group.add(self)
        return ls

    @classmethod
    def render(cls):
        """Affiche tous les sprites"""
        # on crée une surface ne contenant que les sprites
        background = Entity.screen  
        background.fill((0, 0, 0))
        Entity.group.clear(Entity.screen, background)
        Entity.group.draw(Entity.screen) 
