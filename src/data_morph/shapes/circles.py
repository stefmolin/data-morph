"""Shapes that are circular in nature."""

import itertools
from numbers import Number
from typing import Tuple

from ..data.dataset import Dataset
from .bases.shape import Shape


class Circle(Shape):
    """
    Class representing a hollow circle.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    r : numbers.Number, optional
        The radius of the circle.
    """

    def __init__(self, dataset: Dataset, r: Number = None) -> None:
        self.cx: Number = dataset.df.x.mean()
        """numbers.Number: The x coordinate of the circle's center."""

        self.cy: Number = dataset.df.y.mean()
        """numbers.Number: The y coordinate of the circle's center."""

        self.r: Number = r or dataset.df.std().mean() * 1.5
        """numbers.Number: The radius of the circle."""

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} cx={self.cx} cy={self.cy} r={self.r}>'

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the absolute distance between this circle's edge and a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The absolute distance between this circle's edge and the point (x, y).
        """
        return abs(self._euclidean_distance((self.cx, self.cy), (x, y)) - self.r)


class Bullseye(Shape):
    """
    Class representing a bullseye shape comprising two concentric circles.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        stdev = dataset.df.std().mean()
        self.circles: list[Circle] = [Circle(dataset, r) for r in [stdev, stdev * 2]]
        """list[Circle]: The inner and outer :class:`Circle` objects."""

    def __repr__(self) -> str:
        return self._recursive_repr('circles')

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum absolute distance between this bullseye's inner and outer
        circles' edges and a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum absolute distance between this bullseye's inner and outer
            circles' edges and the point (x, y).

        See Also
        --------
        Circle.distance :
            A bullseye consists of two circles, so we use the minimum
            distance to one of the circles.
        """
        return min(circle.distance(x, y) for circle in self.circles)


class Dots(Shape):
    """
    Class representing a 3x3 grid of dots.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        self.dots: list[Tuple[Number, Number]] = list(
            itertools.product(
                *(
                    dataset.df[coord].quantile([0.05, 0.5, 0.95]).tolist()
                    for coord in ['x', 'y']
                )
            )
        )
        """list[Tuple[numbers.Number, numbers.Number]]: List of (x, y) coordinates."""

    def __repr__(self) -> str:
        return self._recursive_repr('dots')

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum Euclidean distance any of the dots in this grid a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum Euclidean distance any of the dots in this grid the point (x, y).
        """
        return min(self._euclidean_distance(dot, (x, y)) for dot in self.dots)


class Scatter(Circle):  # numpydoc ignore: PR02
    """
    Class for the scatter shape: a circular cloud of scattered points.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the distance between this circular cloud of scattered points and a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The distance between this circular cloud of scattered points and the point (x, y).
        """
        return max(self._euclidean_distance((self.cx, self.cy), (x, y)) - self.r, 0)
