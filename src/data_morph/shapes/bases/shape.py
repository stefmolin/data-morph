"""Abstract base class for shapes."""

from abc import ABC, abstractmethod
from typing import Iterable, Union

from scipy.spatial import distance


class Shape(ABC):
    """Abstract base class for a shape."""

    def __repr__(self) -> str:
        """Return string representation of the shape."""
        return self.__class__.__name__.lower()

    @abstractmethod
    def distance(self, x: Union[int, float], y: Union[int, float]) -> float:
        """
        Calculate the distance between this shape and a point (x, y).

        Parameters
        ----------
        x, y : int or float
            Coordinates a of point in 2D space.

        Returns
        -------
        float
            The distance between this shape and the point (x, y).
        """
        raise NotImplementedError

    @staticmethod
    def _euclidean_distance(
        a: Iterable[Union[int, float]], b: Iterable[Union[int, float]]
    ) -> float:
        """
        Calculate the Euclidean distance between points a and b.

        Parameters
        ----------
        a, b : Iterable[Union[int, float]]
            Coordinates of points in space.

        Returns
        -------
        float
            The Euclidean distance between a and b.

        See Also
        --------
        scipy.spatial.distance.euclidean
        """
        return distance.euclidean(a, b)
