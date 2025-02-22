"""Base test class for circle shapes."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import pytest

from data_morph.shapes.circles import Circle

if TYPE_CHECKING:
    from numbers import Number

CIRCLE_REPR = r'<Circle center=\((\d+\.*\d*), (\d+\.*\d*)\) radius=(\d+\.*\d*)>'


class CirclesModuleTestBase:
    """Base for testing circle shapes."""

    shape_name: str
    distance_test_cases: tuple[tuple[tuple[Number], float]]
    repr_regex: str

    @pytest.fixture(scope='class')
    def shape(self, shape_factory):
        """Fixture to get the shape for testing."""
        return shape_factory.generate_shape(self.shape_name)

    def test_distance(self, shape, test_point, expected_distance):
        """
        Test the distance() method parametrized by distance_test_cases
        (see conftest.py).
        """
        actual_distance = shape.distance(*test_point)
        assert pytest.approx(actual_distance) == expected_distance

    def test_repr(self, shape):
        """Test that the __repr__() method is working."""
        assert re.match(self.repr_regex, repr(shape)) is not None

    @pytest.mark.parametrize('ax', [None, plt.subplots()[1]])
    def test_plot(self, shape, ax):
        """Test that the plot() method is working."""
        if ax:
            ax.clear()

        plot_ax = shape.plot(ax)
        if ax:
            assert plot_ax is ax
        else:
            assert plot_ax is not ax

        plotted_circles = plot_ax.patches
        plotted_centers = {plotted_circle._center for plotted_circle in plotted_circles}
        plotted_radii = {
            plotted_circle._width / 2 for plotted_circle in plotted_circles
        }

        if isinstance(shape, Circle):
            assert len(plotted_circles) == 1
            assert plotted_centers == {shape.center}
            assert plotted_radii == {shape.radius}
        else:
            assert len(plotted_circles) == len(shape.circles)
            assert plotted_centers == {tuple(np.unique(shape._centers))}
            assert plotted_radii.difference(shape._radii) == set()

        plt.close()
