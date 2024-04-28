"""
A-star algorithm implementation.
"""

import dataclasses
import functools
import heapq
import typing as t

from ameise.graph import Point, Graph


@dataclasses.dataclass
@functools.total_ordering
class Node:
    """A-star node."""

    pos: Point
    cost: float
    heuristic: float

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.pos == other.pos
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Node):
            return self.pos != other.pos
        return NotImplemented

    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic

    def __repr__(self):
        return f"Node(pos={self.pos}, total_cost={self.cost + self.heuristic})"


def calc_heuristic(pt1: Point, pt2: Point) -> float:
    """Return the Euclidean distance between two points."""
    return ((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2) ** 0.5 * 5


class AStar:
    def __init__(self, graph: Graph, start_pt: Point, goal_pt: Point):
        self._graph = graph
        self._start_node = start_node = Node(start_pt, 0, calc_heuristic(start_pt, goal_pt))
        self._goal_node = Node(goal_pt, 0, 0)
        self._open_list: t.List[Node] = [start_node]
        self._closed_list: t.List[Node] = []
        self._current = start_node

    @property
    def pos(self) -> Point:
        return self._current.pos

    def advance(self, radius=3) -> t.Generator[Point, None, None]:
        while self._open_list:
            node = heapq.heappop(self._open_list)

            if node.heuristic <= radius:
                # No move needed
                self._current = node
                yield node.pos
                return

            for neighbor_pt in self._graph.neighbors(node.pos, d=radius):
                neighbor = Node(neighbor_pt, node.cost + radius, calc_heuristic(neighbor_pt, self._goal_node.pos))
                if neighbor in self._closed_list:
                    continue
                if neighbor not in self._open_list or neighbor.cost < node.cost:
                    heapq.heappush(self._open_list, neighbor)

            self._closed_list.append(node)
            self._current = node
            yield node.pos
