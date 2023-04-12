"""module principal"""
from typing import List
import pygame
from modules.graphics import Interface, Frame, Bouton, POLICE, RelativePos
from modules.outils import UNIT_SIZE
from modules import collectable, entite, plateau, fantome, player

pygame.init()

# constantes

WINDOW = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
RelativePos.window = WINDOW

# fonctions principales

def initialise():
    """fonction d'initialisation"""
    # définition de la zone de jeux
    interface_plateau = Interface('plateau')
    Interface('jeux')
    Frame('plateau', interface_plateau, pygame.Surface((448, 496)),
          RelativePos(0.5, 0.5, 0), 'jeux')
    
    # création du menu
    interface_menu = Interface('menu')

    Bouton(RelativePos(0.5, 0.5, 1), POLICE.render('Jouer', True, '#FFFFFF'),
           lambda: Interface.change_interface('jeux'), 'menu')

    Interface.current_interface = interface_menu


def handle_event(events: List[pygame.event.Event]) -> bool:
    """gestion des événements"""
    for event in events:
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYDOWN:
                Interface.current_interface.on_keypress(event)
            case pygame.MOUSEBUTTONDOWN:
                Interface.current_interface.on_click(event)
            case _:
                ...
    return True


def update():
    """fonction de mis à jour"""
    Interface.current_interface.update()
    WINDOW.blits(Interface.current_interface.render())
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

# définition des entités

joueur = player.Player(
    pygame.Vector3(UNIT_SIZE, UNIT_SIZE, 2), (player.texture_player, {'normal': [(player.texture_player, 0), 
                                                                                 (player.texture_player_2, 200),
                                                                                 (player.texture_player, 200)]}), 1.5)

fantome1 = fantome.Fantome(pygame.Vector3(196, 220, 2), (fantome.texture_fantome, {'fear': [(fantome.texture_fantome_fear, 0), (
    fantome.texture_fantome_fear, 3000)], 'fear_blink': [(fantome.texture_fantome_fear, 0), (fantome.texture_fantome_fear_2, 200), (fantome.texture_fantome, 200)]}))

fantome.Porte(pygame.Vector3(208, 196, 1), 32)

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
