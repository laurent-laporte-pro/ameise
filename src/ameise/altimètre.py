"""
Recherche de l'altitude moyenne d'un point sur la carte à partir de ses coordonnées géographiques.
"""
import math
import statistics

import pygame
import importlib.resources

from ameise.resources import BACKGROUND_IMAGE


def altimeter(image, x, y, radius=5):
    """
    Return the average altitude of a point on the map from its geographical coordinates.
    """
    width = image.get_width()
    height = image.get_height()

    total = 0
    count = 0
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if math.hypot(i, j) <= radius and 0 <= x + i < width and 0 <= y + j < height:
                total += statistics.mean(image.get_at((x + i, y + j))[:3])
                count += 1
    return 255 - total / count


def main():
    with importlib.resources.path("ameise.resources", BACKGROUND_IMAGE) as path:
        maze = pygame.image.load(path)

    pygame.init()
    pygame.display.set_caption("Ameise")

    screen_width = maze.get_width()
    screen_height = maze.get_height()
    screen = pygame.display.set_mode((screen_width, screen_height))

    radius = 8

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            x, y = pygame.mouse.get_pos()
            altitude = altimeter(maze, x, y, radius=radius)

            screen.blit(maze, (0, 0))

            # Couleur bleu brillant pour le pointeur
            blue_pointer = (30, 144, 255)
            pygame.draw.circle(screen, blue_pointer, (x, y), radius, width=2)

            # affiche l'altitude en haut à droite
            font = pygame.font.Font(None, 24)
            text = font.render(f"Altitude: {altitude:.2f} m", True, (0, 0, 0))
            screen.blit(text, (screen_width - 200, 20))

            pygame.display.flip()

            pygame.time.wait(10)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
