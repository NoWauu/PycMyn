"""module principal"""
from typing import List

import pygame

from modules import fantome
import modules.outils as utl
from modules import player
from modules import collectable, entite, plateau
from modules.graphics import (
    Bouton, Frame, Interface, RelativePos, Texte, Sequence)
from modules.overlays import (
    Compteur, HealthBar, StaticTexture, Timer, DtRenderer)

pygame.init()

# constantes

RelativePos.general_window = utl.WINDOW

# fonctions principales


def retour_menu():
    """fin de la partie"""
    utl.call('victoire', {'able': False})
    utl.call('defaite', {'able': False})
    entite.clear()
    Interface.change_interface('menu')


def set_meilleur_temps(temps: int, meilleur_temps: int):
    """remplace le meilleur temps"""
    if temps < meilleur_temps or meilleur_temps == 0:
        utl.SAVE['meilleur_temps'] = temps
        return temps
    return meilleur_temps


def play():
    """lance une partie"""
    # initialisation du terrain
    entite.clear()
    collectable.populate(entite.Entity.plateau.element.surface)

    player.initialisation()
    fantome.initialisation()

    utl.call('init_partie', {})
    utl.call('init_entities', {})

    Interface.change_interface('jeux')


def initialise_menu():
    """initialise le menu"""
    # création du menu
    Interface('menu')

    background = pygame.image.load(
        'ressources/textures/pacman_background.png').convert_alpha()
    background = pygame.transform.scale_by(background, max(utl.WINDOW.get_width(
    ) / background.get_width(), utl.WINDOW.get_height() / background.get_height()))
    background.scroll(dx=-30, dy=-500)
    StaticTexture(background, interface_nom='menu')

    # bouton de lancement du jeux
    Bouton(RelativePos(0.78, 0.64, 1), pygame.Surface((160, 45), pygame.SRCALPHA),
           play, 'menu')

    Interface.change_interface('menu')


def initialise_game_zone():
    """initialise la zone de jeux"""
    # définition de la zone de jeux
    Interface('jeux')
    Frame('plateau', Interface('plateau'), pygame.Surface((448, 496)),
          RelativePos(0.5, 0.5, 0), 'jeux')

    DtRenderer(RelativePos(1, 1, 1, aligne='bottomright'), 'jeux')

    # compteur de points
    Frame('topright', Interface('topright'), pygame.Surface(
        (80, 40), pygame.SRCALPHA), RelativePos(0.99, 0.01, 1, aligne='topright'), 'jeux')

    StaticTexture(pygame.transform.scale(
        collectable.texture_piece, (30, 30)),
        RelativePos(1, 0.5, 1, aligne='right',
                    window=Frame.get_surface_by_name('topright')), interface_nom='topright')

    compteur = Compteur(RelativePos(0.7, 0.5, 1, aligne='right',
                                    window=Frame.get_surface_by_name('topright')),
                        'topright', base='{value}')
    utl.lie('add_point', compteur.incremente)
    utl.lie('vide_point', compteur.vide)

    # vies
    health_texture = pygame.image.load(
        'ressources/textures/coeur.png').convert_alpha()
    health_texture = pygame.transform.scale2x(health_texture)
    health_bar = HealthBar(RelativePos(
        0.5, 1, 1, 'bottom'), health_texture, 3, 'jeux')
    utl.lie('set_vie', health_bar.set_repetition)

    # niveaux
    texte_niveau = Texte(RelativePos(0.5, 0, 1, aligne='top'),
                         f'niveau: {entite.Entity.niveau + 1}',
                         couleur='#0090FF', scale=2, interface_nom='jeux')
    utl.lie('inc_niveau', lambda niveau: setattr(
        texte_niveau, 'texte', f'niveau: {niveau + 1}'))
    utl.lie('inc_niveau', entite.Entity.set_niveau)

    # jeux
    entite.Entity.plateau = plateau.initialisation()


def initialise_end_zone():
    """initialise l'interface de fin de jeux"""

    # timer
    Frame('topleft', Interface('topleft'), pygame.Surface(
        (115, 80), pygame.SRCALPHA), RelativePos(0.01, 0.01, 1, 'topleft'), 'jeux')
    montre_texture = pygame.image.load(
        'ressources/textures/montre.png').convert_alpha()
    montre_texture = pygame.transform.scale(montre_texture, (70, 70))
    StaticTexture(montre_texture, pos=RelativePos(0, 0.5, 1, aligne='left',
                  window=Frame.get_surface_by_name('topleft')), interface_nom='topleft')
    timer = Timer(RelativePos(1, 0.5, 1, aligne='right',
                  window=Frame.get_surface_by_name('topleft')), 'topleft')
    utl.lie('init_partie', timer.start)
    utl.lie('fin_partie', timer.stop)

    # victoire
    Interface('fin_partie')
    victoire_background = StaticTexture(
        pygame.transform.scale(pygame.image.load(
            'ressources/textures/victoire.png').convert_alpha(),
            utl.WINDOW.get_size()), interface_nom='fin_partie')
    utl.lie('victoire', victoire_background.element.able)
    victoire_background.element.able(able=False)

    victoire_fin = Bouton(RelativePos(0.52, 0.68, 2),
                          pygame.Surface((300, 35), pygame.SRCALPHA),
                          retour_menu, interface_nom='fin_partie')
    victoire_fin.element.able(able=False)

    victoire_suivant = Bouton(RelativePos(0.51, 0.51, 2),
                              pygame.Surface((390, 60), pygame.SRCALPHA),
                              play, interface_nom='fin_partie')
    victoire_suivant.element.able(able=False)

    utl.lie('victoire', victoire_fin.element.able)
    utl.lie('victoire', victoire_suivant.element.able)

    # défaite
    defaite_background = StaticTexture(
        pygame.transform.scale(pygame.image.load(
            'ressources/textures/defaite.png').convert_alpha(),
            utl.WINDOW.get_size()), interface_nom='fin_partie')
    utl.lie('defaite', defaite_background.element.able)
    defaite_background.element.able(able=False)

    defaite_fin = Bouton(RelativePos(0.52, 0.7, 2),
                         pygame.Surface((720, 50), pygame.SRCALPHA),
                         retour_menu, interface_nom='fin_partie')
    defaite_fin.element.able(able=False)
    utl.lie('defaite', defaite_fin.element.able)

    # meilleur temps
    meilleur_temps = str(utl.SAVE['meilleur_temps']) + \
        ' s' if utl.SAVE['meilleur_temps'] != 0 else 'Aucun'

    meilleur_temps_texte = Texte(RelativePos(0.5, 0.9, 1, aligne='bottom'),
                                 texte=f'meilleur temps: {meilleur_temps}',
                                 couleur='#0000FF', scale=1.8, interface_nom='fin_partie')
    utl.lie('fin_partie',
            lambda **args: setattr(meilleur_temps_texte, 'texte',
                                   'meilleur temps: {} s'.format(str(
                                       set_meilleur_temps(timer.get_temps(),
                                                          utl.SAVE['meilleur_temps']))))
            if victoire_background.element.enabled else None)


def initialise():
    """fonction d'initialisation"""
    initialise_menu()
    initialise_game_zone()
    initialise_end_zone()


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

# ce n'est pas une constante
running = True

while running:
    running = handle_event(pygame.event.get())
    update()

    # le jeux à besoin d'au moins 60 fps
    # soit moins de 20 ms
    clock.tick(60)  # 60 fps

utl.save()
