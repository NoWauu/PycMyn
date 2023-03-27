"""module principal"""
from typing import List, Iterable, Tuple
import pygame
from modules.classes import Interface, Text

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
    interface = Interface()
    Interface.current_interface = interface

    Text('DEF', (400, 400), 5, '#FF0000')
    Text('ABC', (400, 400), 3, '#00FF00')


def handle_event(events: List[pygame.event.Event]) -> bool:
    """gestion des événements"""
    for event in events:
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYDOWN:
                ...
            case _:
                ...
    return True

def update():
    """fonction de mis à jour"""
    Interface.current_interface.update()
    blits(WINDOW, Interface.current_interface.render())
    pygame.display.flip()

# boucle principale

initialise()

running = True

while running:
    running = handle_event(pygame.event.get())
    update()