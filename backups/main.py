import pygame
import sys
from modules import entite, fantome, player, plateau, collectable, decoration

pygame.init()

# gestion de la fenêtre


def quit(event: pygame.event.Event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

# gestion des fonctions usuelles du jeu


def check_victory():
    return not any([entity.id == 'piece' for entity in entite.Entity.group])


def check_defaite():
    return not joueur in entite.Entity.group

# -- mis en place


screen = pygame.display.set_mode((1200, 640), pygame.RESIZABLE)
width, height = screen.get_size()

# création des textures

texture_piece = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.circle(texture_piece, (250, 198, 53), (16, 16), 3)

texture_pomme = pygame.Surface((32, 32))
texture_pomme.blit(pygame.transform.scale(
    pygame.image.load("ressources/textures/pomme.png"), (16, 16)), (8, 8))

texture_super = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.circle(texture_super, (255, 255, 255), (16, 16), 6)

collectable.Piece.settexture(texture_piece)
collectable.Pomme.settexture(texture_pomme)
collectable.Super.settexture(texture_super)

# -- debug

texture_player = pygame.transform.smoothscale(
    pygame.image.load("ressources/textures/pacman.png"), (32, 32))

texture_player_2 = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.circle(texture_player_2, "#FFCC00", (16, 16), 16)

texture_fantome = pygame.transform.scale(
    pygame.image.load("ressources/textures/blinky.png"), (32, 32))

texture_fantome_fear = pygame.transform.scale(
    pygame.image.load("ressources/textures/stun.png"), (32, 32))

texture_porte = pygame.Surface((32, 32))
pygame.draw.rect(texture_porte, (250, 175, 90),
                 pygame.rect.Rect(0, 14, 32, 4))

# définition des entités

joueur = player.Player(
    (32, 32), (texture_player, [texture_player, texture_player_2], [100, 100]), 1.5)

fantome1 = fantome.Fantome((128, 96), (texture_fantome, [texture_fantome_fear, texture_fantome,
                                                                            texture_fantome_fear, texture_fantome,
                                                                            texture_fantome_fear, texture_fantome,
                                                                            texture_fantome_fear], [3000, 400, 300, 200, 200, 200, 200]))

porte1 = fantome.Porte((96, 64), texture_porte)
porte2 = fantome.Porte((192, 64), texture_porte)

# définition des décors

points = decoration.Texte(
    f'points: {joueur.points}', 35, '#FFFFFF', (width//2, 30))
vies = decoration.Texte(
    f'vies: {joueur.health}', 35, '#FFFFFF', (3 * width//4, height - 50))

# définition du plateaux

plt = plateau.Plateau(10, 10)
entite.Entity.plateau = plt

plt.update_texture()

# définition de la clock du jeu

clock = pygame.time.Clock()

# initialisation du terrain

collectable.populate()

# boucle de jeu

run = True

while run:
    events = pygame.event.get()

    points.set_texte(f'points: {joueur.points}')
    vies.set_texte(f'vies: {joueur.health}')

    for event in events:
        quit(event)

    if check_victory():
        decoration.Texte(
            f'You Win', 35, '#FFFFFF', (width//2, height-50))
        run = False
    elif check_defaite():
        decoration.Texte(
            f'Game Over\npoints: {joueur.points}', 35, '#FFFFFF', (width//2, height-50))
        vies.set_texte('vies: 0')
        run = False

    plt.update(entite.Entity.group, events)
    game_surf, game_rect = plt.render(entite.Entity.group)
    game_rect.center = screen.get_rect().center

    decoration.render(screen, (game_surf, game_rect))

    clock.tick(90)  # 90 fps

pygame.time.wait(5000)
