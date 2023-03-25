"""module de gestion des élements de décoration du jeu"""
from typing import Tuple, List

import pygame


def render(screen: pygame.Surface, game_surf_info: Tuple[pygame.Surface, pygame.Rect]):
    """fonction d'affichage"""
    screen.blit(*game_surf_info)

    Element.elements.draw(screen)

    pygame.display.flip()


class Element(pygame.sprite.Sprite):
    """classe de gestion des éléments de décoration"""
    elements: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self, surf: pygame.Surface, rect: pygame.Rect) -> None:
        super().__init__()

        self.image = surf
        self.rect = rect

        self.add(Element.elements)


class Texte(Element):
    """classe de gestion du texte"""

    def __init__(self, texte: str, taille: int, couleur: str, position: Tuple[int, int]) -> None:
        super().__init__(*self.texte2surf(texte, taille, couleur))
        self.position = position
        self.rect.center = position

        self.taille = taille
        self.color = couleur

    def set_texte(self, texte: str, taille: int=0, couleur: str='#000000'):
        """change le texte de l'élément"""
        if taille == 0:
            taille = self.taille
        if couleur == '#000000':
            couleur = self.color

        self.image, self.rect = self.texte2surf(texte, taille, couleur)
        self.rect.center = self.position

    @classmethod
    def texte2surf(cls, texte: str, taille: int, couleur: str) -> Tuple[pygame.Surface, pygame.Rect]:
        """transforme du texte en surface"""
        police = pygame.font.Font(None, taille)
        ls_texte = texte.split('\n')
        textes_render: List[pygame.Surface] = []  # liste des surfaces de texte

        for txt in ls_texte:
            textes_render.append(police.render(txt, True, couleur))

        texte_surf = pygame.Surface((max((surf.get_width() for surf in textes_render)),
                                     sum((surf.get_height() for surf in textes_render))))

        texte_surf.blits(list((surf, (texte_surf.get_rect().centerx - surf.get_width() / 2,
                                  sum((surf.get_height() for surf in
                                       textes_render[:index]))))
                          for index, surf in enumerate(textes_render)))

        return texte_surf, texte_surf.get_rect()
