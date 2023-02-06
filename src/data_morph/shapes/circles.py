"""Shapes that are circular."""

import itertools

from .shape import Shape


class Circle(Shape):
    """Class representing a hollow circle."""

    def __init__(self, data) -> None:
        self.cx = data.x.mean()
        self.cy = data.y.mean()
        self.r = 30  # TODO: think about how this could be calculated

    def distance(self, x, y) -> float:
        return abs(self._euclidean_distance((self.cx, self.cy), (x, y)) - self.r)


class Bullseye(Shape):
    """Class representing a bullseye shape comprising two concentric circles."""

    def __init__(self, data) -> None:
        self.circles = [
            Circle(data.x.mean(), data.y.mean(), r)
            for r in [18, 37]  # TODO: think about how this could be calculated
        ]

    def distance(self, x, y) -> float:
        return min(circle.distance(x, y) for circle in self.circles)


class Dots(Shape):
    """Class representing a 3x3 grid of dots."""

    def __init__(self, data) -> None:
        self.dots = list(
            itertools.product(
                data[coord].quantile([0.05, 0.5, 0.95]).tolist() for coord in ['x', 'y']
            )
        )

    def distance(self, x, y) -> float:
        return min(self._euclidean_distance(dot, (x, y)) for dot in self.dots)
