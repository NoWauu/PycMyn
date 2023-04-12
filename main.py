"""module principal"""
from typing import List
import pygame
from modules.graphics import Interface, Frame, Bouton, POLICE, RelativePos
from modules import collectable, entite, plateau
import modules.player as player
import modules.fantome as fantome

pygame.init()

# constantes

WINDOW = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
RelativePos.window = WINDOW

# fonctions principales

def play():
    """lance une partie"""
    # initialisation du terrain
    collectable.populate(entite.Entity.plateau.element.surface)

    player.initialisation()
    fantome.initialisation()

    Interface.change_interface('jeux')

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
           play, 'menu')

    Interface.current_interface = interface_menu

    # jeux
    plt = plateau.Plateau()
    entite.Entity.plateau = plt


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
    WINDOW.fill('#000000')
    Interface.current_interface.update()
    WINDOW.blits(Interface.current_interface.render())
    pygame.display.flip()


# initialisation

initialise()

# -- mis en place

screen = pygame.display.set_mode((1200, 640), pygame.RESIZABLE)
width, height = screen.get_size()

# définition de la clock du jeu

clock = pygame.time.Clock()

# boucle principale

running = True

while running:
    running = handle_event(pygame.event.get())
    update()

    clock.tick(90)  # 90 fps
