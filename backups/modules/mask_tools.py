import pygame

from modules.outils import UNIT_SIZE


def mask_to_surface(mask: pygame.mask.Mask):
    """transforme un mask en surface"""
    size = mask.get_size()
    surf = pygame.Surface(size, pygame.SRCALPHA)
    for x in range(size[0]):
        for y in range(size[1]):
            if mask.get_at((x, y)) != 0:
                surf.set_at((x, y), (255, 255, 255))

    return surf


def extend_mask(mask: pygame.mask.Mask) -> pygame.mask.Mask:
    """étend le mask dans toutes les directions de 1 pixel"""
    width, height = mask.get_size()

    new_mask = pygame.mask.Mask(
        (width + 2 * UNIT_SIZE, height + 2 * UNIT_SIZE))
    new_mask.draw(mask, (UNIT_SIZE, UNIT_SIZE))

    # y = -1 & y = height + 1
    for x in range(width):
        if mask.get_at((x, 0)):
            new_mask.set_at((x + UNIT_SIZE, UNIT_SIZE - 1))
        if mask.get_at((x, height - 1)):
            new_mask.set_at((x + UNIT_SIZE, height + UNIT_SIZE))

    # x = -1 & x = width + 1
    for y in range(height):
        if mask.get_at((0, y)):
            new_mask.set_at((UNIT_SIZE - 1, y + UNIT_SIZE))
        if mask.get_at((width - 1, y)):
            new_mask.set_at((width + UNIT_SIZE, y + UNIT_SIZE))

    # corners

    new_mask.set_at((UNIT_SIZE - 1, UNIT_SIZE - 1))
    new_mask.set_at((UNIT_SIZE - 1, height + UNIT_SIZE))
    new_mask.set_at((width + UNIT_SIZE, UNIT_SIZE - 1))
    new_mask.set_at((width + UNIT_SIZE, height + UNIT_SIZE))

    return new_mask
