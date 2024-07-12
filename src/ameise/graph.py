import random
import typing as t

import pygame


class Color(t.NamedTuple):
    r: int
    g: int
    b: int
    a: int


GREEN_COLOR = Color(0, 255, 0, 255)
RED_COLOR = Color(255, 0, 0, 255)
WHITE_COLOR = Color(255, 255, 255, 255)
BLACK_COLOR = Color(0, 0, 0, 255)
LIGHT_BLUE_COLOR = Color(163, 206, 230, 255)  # RGB + Alpha


class Point(t.NamedTuple):
    x: int
    y: int

    def move(self, dx: int, dy: int) -> 'Point':
        return Point(self.x + dx, self.y + dy)


def _is_color(color, ref_color, threshold: int = 15):
    dx = color[0] - ref_color[0]
    dy = color[1] - ref_color[1]
    dz = color[2] - ref_color[2]
    return dx * dx + dy * dy + dz * dz < threshold ** 2


def is_near(pt1: Point, pt2: Point, radius: int) -> bool:
    """Return True if the distance between two points is less than d."""
    return ((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2) ** 0.5 <= radius

class Graph:
    def __init__(self, image: pygame.Surface):
        self._image = image
        self._width = image.get_width()
        self._height = image.get_height()
        self._start_points = set()
        self._end_points = set()

        for x in range(1, image.get_width(), 3):
            for y in range(0, image.get_height(), 3):
                if _is_color(image.get_at(Point(x, y)), RED_COLOR):
                    self._start_points.add(Point(x, y))
                if _is_color(image.get_at(Point(x, y)), GREEN_COLOR):
                    self._end_points.add(Point(x, y))

    @property
    def start_points(self) -> t.FrozenSet[Point]:
        return frozenset(self._start_points)

    @property
    def end_points(self) -> t.FrozenSet[Point]:
        return frozenset(self._end_points)

    def is_free(self, pt: Point) -> bool:
        if 0 <= pt.x < self._width and 0 <= pt.y < self._height:
            color = self._image.get_at(pt)
            return _is_color(color, WHITE_COLOR) or _is_color(color, LIGHT_BLUE_COLOR)
        return False

    def neighbors(self, point: Point, d=3) -> t.Sequence[Point]:
        directions = [(-d, 0), (d, 0), (0, -d), (0, d)]
        random.shuffle(directions)
        neighbors = []
        for dx, dy in directions:
            if 0 <= point.x + dx < self._width and 0 <= point.y + dy < self._height:
                target = Point(point.x + dx, point.y + dy)
                if self.is_free(target):
                    neighbors.append(target)
        return neighbors

    def reach_end(self, pt: Point) -> bool:
        return any(is_near(pt, end_pt, 3) for end_pt in self._end_points)
