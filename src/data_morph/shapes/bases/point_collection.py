"""Base class for shapes that are composed of points."""

from numbers import Number

import numpy as np

from .shape import Shape


class PointCollection(Shape):
    """
    Class representing a shape formed by a collection of points.

    Parameters
    ----------
    *points : Iterable[Iterable[Number]]
        An iterable of (x, y) values representing an arrangement of points.
    """

    def __init__(self, *points) -> None:
        self.points = points

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} of {len(self.points)} points>'

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum distance from the points of this shape
        to a point (x, y).

        Parameters
        ----------
        x, y : int or float
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum distance from the points of this shape
            to the point (x, y).
        """
        return np.min(
            np.linalg.norm(np.array(self.points) - np.array((x, y)), ord=2, axis=1)
        )
