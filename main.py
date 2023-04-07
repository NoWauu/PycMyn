"""module principal"""
from typing import List, Iterable, Tuple
import pygame
from modules.classes import Interface, Frame
from modules.outils import UNIT_SIZE
from modules import collectable, entite, plateau, fantome, player

pygame.init()

# constantes

WINDOW = pygame.display.set_mode((600, 600), pygame.RESIZABLE)

# fonctions principales


def blits(surface: pygame.Surface, blit_sequence: Iterable[Tuple[pygame.Surface, pygame.Rect]]):
    """multiple blit"""
    for surf, rect in blit_sequence:
        surface.blit(surf, rect)


def initialise():
    """fonction d'initialisation"""
    interface_jeux = Interface('jeux')
    interface_principale = Interface('principale')
    Frame('jeux', interface_jeux, pygame.Surface((448, 496)),
          pygame.Vector3(32, 32, 0), 'principale')

    Interface.current_interface = interface_principale


def handle_event(events: List[pygame.event.Event]) -> bool:
    """gestion des événements"""
    for event in events:
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYDOWN:
                Interface.current_interface.on_keypress(event)
            case _:
                ...
    return True


def update():
    """fonction de mis à jour"""
    Interface.current_interface.update()
    blits(WINDOW, Interface.current_interface.render())
    pygame.display.flip()


# initialisation


initialise()

# setup debug


def check_victory():
    return not any([isinstance(entity, collectable.Piece) for entity in entite.Entity.group])


def check_defaite():
    return not joueur in entite.Entity.group

# -- mis en place

screen = pygame.display.set_mode((1200, 640), pygame.RESIZABLE)
width, height = screen.get_size()

# création des textures

texture_piece = pygame.Surface((UNIT_SIZE, UNIT_SIZE), pygame.SRCALPHA)
pygame.draw.circle(texture_piece, (250, 198, 53), (UNIT_SIZE // 2, UNIT_SIZE // 2), 3)

texture_pomme = pygame.transform.scale(
    pygame.image.load("ressources/pomme.png"), (UNIT_SIZE, UNIT_SIZE))

texture_super = pygame.Surface((UNIT_SIZE, UNIT_SIZE), pygame.SRCALPHA)
pygame.draw.circle(texture_super, (255, 255, 255), (UNIT_SIZE // 2, UNIT_SIZE // 2), 6)

collectable.Piece.settexture(texture_piece)
collectable.Pomme.settexture(texture_pomme)
collectable.Super.settexture(texture_super)

# -- debug

texture_player = pygame.transform.smoothscale(
    pygame.image.load("ressources/pacman.png"), (UNIT_SIZE, UNIT_SIZE))

texture_player_2 = pygame.Surface((UNIT_SIZE, UNIT_SIZE), pygame.SRCALPHA)
texture_player_2.fill(pygame.Color(255, 255, 255, 10))
pygame.draw.circle(texture_player_2, "#FFCC00", (UNIT_SIZE // 2, UNIT_SIZE // 2), UNIT_SIZE // 2)

texture_fantome = pygame.transform.scale(
    pygame.image.load("ressources/blinky.png"), (UNIT_SIZE, UNIT_SIZE))

texture_fantome_fear = pygame.transform.scale(
    pygame.image.load("ressources/stun.png"), (UNIT_SIZE, UNIT_SIZE))
texture_fantome_fear_2 = pygame.transform.scale(
    pygame.image.load("ressources/stun2.png"), (UNIT_SIZE, UNIT_SIZE))

texture_porte = pygame.Surface((UNIT_SIZE, UNIT_SIZE))
pygame.draw.rect(texture_porte, (250, 175, 90),
                 pygame.rect.Rect(0, (UNIT_SIZE - 4) // 2, UNIT_SIZE, 4))


# définition des entités

joueur = player.Player(
    pygame.Vector3(UNIT_SIZE, UNIT_SIZE, 2), (texture_player, {'normal': [(texture_player, 0), (texture_player_2, 200), (texture_player, 200)]}), 1.5)

fantome1 = fantome.Fantome(pygame.Vector3(400, 16, 2), (texture_fantome, {'fear': [(texture_fantome_fear, 0), (
    texture_fantome_fear, 3000)], 'fear_blink': [(texture_fantome_fear, 0), (texture_fantome_fear_2, 200), (texture_fantome, 200)]}))

fantome.Porte(pygame.Vector3(224, 196, 1), texture_porte)
fantome.Porte(pygame.Vector3(208, 196, 1), texture_porte)


# définition du plateaux

plt = plateau.Plateau()
entite.Entity.plateau = plt

# définition de la clock du jeu

clock = pygame.time.Clock()

# initialisation du terrain

collectable.populate(plt.element.surface)

# boucle principale

running = True

while running:
    running = handle_event(pygame.event.get())
    update()

    if check_victory():
        running = False
    elif check_defaite():
        running = False

    clock.tick(90)  # 90 fps
