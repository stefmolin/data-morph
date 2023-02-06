"""Shapes that are circular in nature."""

import itertools

from .shape import Shape


class Circle(Shape):
    """Class representing a hollow circle."""

    def __init__(self, data) -> None:
        self.cx = data.x.mean()
        self.cy = data.y.mean()
        self.r = 30  # TODO: think about how this could be calculated

    def distance(self, x, y) -> float:
        """
        Calculate the absolute distance between this circle's edge and a point (x, y).

        Parameters
        ----------
        x, y : int or float
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The absolute distance between this circle's edge and the point (x, y).
        """
        return abs(self._euclidean_distance((self.cx, self.cy), (x, y)) - self.r)


class Bullseye(Shape):
    """Class representing a bullseye shape comprising two concentric circles."""

    def __init__(self, data) -> None:
        self.circles = [
            Circle(data.x.mean(), data.y.mean(), r)
            for r in [18, 37]  # TODO: think about how this could be calculated
        ]

    def distance(self, x, y) -> float:
        """
        Calculate the minimum absolute distance between this bullseye's inner and outer
        circles' edges and a point (x, y).

        Parameters
        ----------
        x, y : int or float
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum absolute distance between this bullseye's inner and outer
            circles' edges and the point (x, y).

        See Also
        --------
        Circle.distance
        """
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
        """
        Calculate the minimum Euclidean distance any of the dots in this grid a point (x, y).

        Parameters
        ----------
        x, y : int or float
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum Euclidean distance any of the dots in this grid the point (x, y).
        """
        return min(self._euclidean_distance(dot, (x, y)) for dot in self.dots)
