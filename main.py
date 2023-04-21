"""module principal"""
from typing import List

import pygame

import modules.fantome as fantome
import modules.outils as utl
import modules.player as player
from modules import collectable, entite, plateau
from modules.graphics import (
    Bouton, Frame, Interface, RelativePos, Texte, Sequence)
from modules.overlays import Compteur, DtRenderer, HealthBar, Background

pygame.init()

# constantes

RelativePos.window = utl.WINDOW

# fonctions principales


def play():
    """lance une partie"""
    # initialisation du terrain
    collectable.populate(entite.Entity.plateau.element.surface)

    player.initialisation()
    fantome.initialisation()

    utl.call('init_entities', {})

    Interface.change_interface('jeux')


def initialise():
    """fonction d'initialisation"""
    # création du menu
    interface_menu = Interface('menu')

    background = pygame.image.load('ressources/textures/pacman_background.png').convert_alpha()
    background = pygame.transform.scale_by(background, max(utl.WINDOW.get_width() / background.get_width(), utl.WINDOW.get_height() / background.get_height()))
    background.scroll(dx = -30, dy = -500)
    Background(background, 'menu')

    # bouton de lancement du jeux
    Bouton(RelativePos(0.65, 0.17, 1), pygame.Surface((200, 50), pygame.SRCALPHA),
           play, 'menu')

    Interface.current_interface = interface_menu

    # définition de la zone de jeux
    interface_plateau = Interface('plateau')
    Interface('jeux')
    Frame('plateau', interface_plateau, pygame.Surface((448, 496)),
          RelativePos(0.5, 0.5, 0), 'jeux')
    texte_niveau = Texte(RelativePos(0.5, 1, 1, aligne='bottom'),
                         f'niveau: {entite.Entity.niveau}', interface_nom='jeux')
    utl.lie('inc_niveau', lambda niveau: setattr(
        texte_niveau, 'texte', f'niveau: {niveau + 1}'))

    # compteur de points
    compteur = Compteur(RelativePos(0.5, 0, 1, aligne='top'), 'jeux')
    utl.lie('add_point', compteur.incremente)
    utl.lie('vide_point', compteur.vide)

    DtRenderer(RelativePos(1, 0, 1, aligne='topright'), interface_nom='jeux')

    # vies
    health_bar = HealthBar(RelativePos(0, 1, 1, 'bottomleft'), pygame.image.load(
        'ressources/textures/coeur.png').convert_alpha(), 3, 'jeux')
    utl.lie('set_vie', health_bar.set_repetition)

    # jeux
    plt = plateau.Plateau()
    entite.Entity.plateau = plt

    # niveaux
    utl.lie('inc_niveau', entite.Entity.set_niveau)


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
            case pygame.VIDEORESIZE:
                Interface.current_interface.on_video_resize()
            case _:
                ...
    return True


def update():
    """fonction de mis à jour"""
    utl.WINDOW.fill('#000000')
    Sequence.update()
    Interface.current_interface.update()
    utl.WINDOW.blits(Interface.current_interface.render())
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
