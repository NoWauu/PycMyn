from typing import List
import pygame

def follow(pos_player: pygame.Vector2, pos: pygame.Vector2, directions: List[int]):
    """
    renvoie une direction au
    choix parmi celles proposées
    """

    direct = (pos_player - pos).normalize()
    produits_scalaires = [((direction % 2 == 0) * (-(direction // 2) * 2 + 1) * direct.x +
      (direction % 2 == 1) * ((direction // 2) * 2 - 1) * direct.y) for direction in directions]
    return directions[produits_scalaires.index(max(produits_scalaires))]

print(follow(pygame.Vector2(0, 10), pygame.Vector2(0, 0), [0, 1, 2, 3]))