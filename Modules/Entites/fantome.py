import pygame, sys
from Entite import Entity

pygame.init()

screen = pygame.display.set_mode((600, 600))
Entity.screen = screen


class Fantome(Entity):
    def __init__(self, textures, position, comportement=None) -> None:
        super().__init__(position, textures)
        


    def fear(self):
        self.textures = pygame.image.load("Design/stun.png")


    def isFeared(self) -> bool:
        pass


blinky = Fantome([pygame.image.load("Design/blinky.png")], (300, 300))
pinky = Fantome([pygame.image.load("Design/pinky.png")], (200, 200))
inky = Fantome([pygame.image.load("Design/inky.png")], (100, 300))
clyde = Fantome([pygame.image.load("Design/clyde.png")], (400, 400))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    Entity.render()
    pygame.display.flip()
