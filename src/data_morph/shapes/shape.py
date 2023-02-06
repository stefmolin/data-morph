"""Abstract base class for shapes."""

from abc import ABC

from scipy.spatial import distance


class Shape(ABC):
    """Abstract base class for a shape."""

    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        """Return string representation of the shape."""
        return self.__class__.__name__.lower()

    def distance(self, x, y) -> float:
        raise NotImplementedError

    @staticmethod
    def _euclidean_distance(a, b) -> float:
        return distance.euclidean(a, b)
