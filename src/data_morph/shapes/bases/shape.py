"""Abstract base class for shapes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Iterable
    from numbers import Number

    from matplotlib.axes import Axes


class Shape(ABC):
    """Abstract base class for a shape."""

    name: str | None = None
    """The display name for the shape, if the lowercased class name is not desired."""

    @classmethod
    def get_name(cls) -> str:
        """
        Get the name of the shape.

        Returns
        -------
        str
            The name of the shape.
        """
        return cls.name or cls.__name__.lower()

    def __repr__(self) -> str:
        """
        Return string representation of the shape.

        Returns
        -------
        str
            The unambiguous string representation of the shape.
        """
        return self._recursive_repr()

    def __str__(self) -> str:
        """
        Return string representation of the shape.

        Returns
        -------
        str
            The human-readable string representation of the shape.

        See Also
        --------
        get_name : This calls the :meth:`.get_name` class method.
        """
        return self.get_name()

    @abstractmethod
    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the distance between this shape and a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The distance between this shape and the point (x, y).
        """
        raise NotImplementedError

    @staticmethod
    def _euclidean_distance(a: Iterable[Number], b: Iterable[Number]) -> float:
        """
        Calculate the Euclidean distance between points a and b.

        Parameters
        ----------
        a, b : Iterable[numbers.Number]
            Coordinates of points in two-dimensional space.

        Returns
        -------
        float
            The Euclidean distance between a and b.

        See Also
        --------
        numpy.linalg.norm : Euclidean distance calculation.
        """
        return np.linalg.norm(a - b)

    def _recursive_repr(self, attr: str | None = None) -> str:
        """
        Return string representation of the shape incorporating
        any items inside a specific attribute.

        Parameters
        ----------
        attr : str, optional
            The attribute to incorporate into the result; must
            be iterable.

        Returns
        -------
        str
            The unambiguous string representation of the shape.
        """
        value = f'<{self.__class__.__name__}>'
        if not attr:
            return value

        indented_line = '\n  '
        offset = len(attr) + 4
        hanging_indent = f'{indented_line:<{offset}}'
        return (
            value
            + f'{indented_line}{attr}={hanging_indent}'
            + f'{hanging_indent}'.join(repr(item) for item in getattr(self, attr))
        )

    @abstractmethod
    def plot(self, ax: Axes | None = None) -> Axes:
        """
        Plot the shape.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            An optional :class:`~matplotlib.axes.Axes` object to plot on.

        Returns
        -------
        matplotlib.axes.Axes
            The :class:`~matplotlib.axes.Axes` object containing the plot.

        Notes
        -----
        When implementing this method for subclasses, make sure to apply the
        :func:`.plotting.style.plot_with_custom_style` decorator.
        """
        raise NotImplementedError
