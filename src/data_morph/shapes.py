"""Classes for specific shapes that data can be morphed into."""

from abc import ABC
import itertools

from scipy.spatial import distance


# TODO: make this a mapping of name to class
LINE_SHAPES = [
    'x', 'h_lines', 'v_lines', 'wide_lines', 'high_lines', 'slant_up',
    'slant_down', 'center', 'star', 'down_parab'
]
ALL_TARGETS = LINE_SHAPES + ['circle', 'bullseye', 'dots']


class Shape(ABC):
    """Abstract class for a shape."""

    def __init__(self, *args, **kwargs):
        pass

    def distance(self, x, y) -> float:
        raise NotImplementedError

    @staticmethod
    def _euclidean_distance(a, b) -> float:
        return distance.euclidean(a, b)

class Circle(Shape):
    """Class representing a hollow circle."""

    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r

    def distance(self, x, y) -> float:
        return abs(
            self._euclidean_distance((self.cx, self.cy), (x, y))
            - self.r
        )

class Bullseye(Shape):
    """Class representing a bullseye shape comprising two concentric circles."""

    def __init__(self, cx, cy, rs):
        self.circles = [
            Circle(cx, cy, r)
            for r in rs
        ]

    def distance(self, x, y) -> float:
        return min(circle.distance(x, y) for circle in self.circles)

class Dots(Shape):
    """Class representing a 3x3 grid of dots."""

    def __init__(self, xs, ys):
        self.dots = list(itertools.product(xs, ys))

    def distance(self, x, y) -> float:
        return min(
            self._euclidean_distance(dot, (x, y))
            for dot in self.dots
        )
