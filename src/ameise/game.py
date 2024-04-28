"""
Ameise is a Python animation project that simulates the behavior of an ant navigating through a maze to find food.
It displays the maze as a background image, traces the ant's path, and represents the ant itself as a sprite.
The ant randomly moves through the maze, occasionally depositing pheromones to guide its way.
With dynamic weighting algorithms, the ant intelligently explores the maze while adapting to changes in its environment.
Ameise provides a captivating visualization of ant behavior and maze-solving strategies.
"""

import importlib.resources
import random
import time
import typing as t

import pygame

from ameise.a_star import AStar
from ameise.graph import Graph, LIGHT_BLUE_COLOR, BLACK_COLOR
from ameise.resources import BACKGROUND_IMAGE


def game():
    """
    Initialize the game window and load the maze image.
    """

    with importlib.resources.path("ameise.resources", BACKGROUND_IMAGE) as path:
        maze = pygame.image.load(path)

    g = Graph(maze)

    count = 1
    ants: t.List[AStar] = []
    for _ in range(count):
        start_pt = random.choice(list(g.start_points))
        goal_pt = random.choice(list(g.end_points))
        ant = AStar(g, start_pt, goal_pt)
        ants.append(ant)

    pygame.init()
    pygame.display.set_caption('Ameise')

    screen = pygame.display.set_mode((maze.get_width(), maze.get_height()))

    try:
        while ants:
            for ant in ants:
                # dépose un peu de phéromone bleu clair
                pygame.draw.circle(maze, LIGHT_BLUE_COLOR, ant.pos, 1)

            for ant in ants[:]:
                new_pos = next(ant.advance())
                if g.reach_end(new_pos):
                    ants.remove(ant)

            for ant in ants:
                pygame.draw.circle(maze, BLACK_COLOR, ant.pos, 1)

            screen.blit(maze, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            time.sleep(0.1)
            pygame.display.flip()

        time.sleep(10)

    finally:
        pygame.quit()



if __name__ == '__main__':
    game()
