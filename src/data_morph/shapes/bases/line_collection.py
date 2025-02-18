"""Base class for shapes that are composed of lines."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np

from ...plotting.style import plot_with_custom_style
from .shape import Shape

if TYPE_CHECKING:
    from collections.abc import Iterable
    from numbers import Number

    from matplotlib.axes import Axes


class LineCollection(Shape):
    """
    Class representing a shape consisting of one or more lines.

    Parameters
    ----------
    *lines : Iterable[Iterable[numbers.Number]]
        An iterable of two (x, y) pairs representing the endpoints
        of a line.
    """

    def __init__(self, *lines: Iterable[Iterable[Number]]) -> None:
        # check that lines with the same starting and ending points raise an error
        for line in lines:
            if np.allclose(*line):
                raise ValueError(f'Line {line} has the same start and end point')

        self.lines = np.array(lines)
        """Iterable[Iterable[numbers.Number]]: An iterable
        of two (x, y) pairs representing the endpoints of a line."""

    def __repr__(self) -> str:
        return self._recursive_repr('lines')

    def distance(self, x: Number, y: Number) -> float:
        """
        Calculate the minimum distance from the lines of this shape
        to a point (x, y).

        Parameters
        ----------
        x, y : numbers.Number
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum distance from the lines of this shape to the
            point (x, y).

        Notes
        -----
        Implementation based on `this Stack Overflow answer`_.

        .. _this Stack Overflow answer: https://stackoverflow.com/a/58781995
        """
        point = np.array([x, y])

        start_points = self.lines[:, 0, :]
        end_points = self.lines[:, 1, :]

        tangent_vector = end_points - start_points
        normalized_tangent_vectors = np.divide(
            tangent_vector,
            np.hypot(tangent_vector[:, 0], tangent_vector[:, 1]).reshape(-1, 1),
        )

        # row-wise dot products of 2D vectors
        signed_parallel_distance_start = np.multiply(
            start_points - point, normalized_tangent_vectors
        ).sum(axis=1)
        signed_parallel_distance_end = np.multiply(
            point - end_points, normalized_tangent_vectors
        ).sum(axis=1)

        clamped_parallel_distance = np.maximum.reduce(
            [
                signed_parallel_distance_start,
                signed_parallel_distance_end,
                np.zeros(signed_parallel_distance_start.shape[0]),
            ]
        )

        # row-wise cross products of 2D vectors
        diff = point - start_points
        perpendicular_distance_component = (
            diff[..., 0] * normalized_tangent_vectors[..., 1]
            - diff[..., 1] * normalized_tangent_vectors[..., 0]
        )

        return np.min(
            np.hypot(clamped_parallel_distance, perpendicular_distance_component)
        )

    @plot_with_custom_style
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
        """
        if not ax:
            fig, ax = plt.subplots(layout='constrained')
            fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)
        _ = ax.axis('equal')
        for start, end in self.lines:
            ax.plot(*list(zip(start, end)), 'k-')
        return ax
