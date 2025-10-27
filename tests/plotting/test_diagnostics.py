"""Test the diagnostics module."""

import pytest
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

from data_morph.data.loader import DataLoader
from data_morph.plotting.diagnostics import plot_shape_on_dataset
from data_morph.shapes.bases.line_collection import LineCollection
from data_morph.shapes.bases.point_collection import PointCollection
from data_morph.shapes.factory import ShapeFactory


@pytest.mark.parametrize(
    ('dataset_name', 'shape_name', 'show_bounds', 'alpha'),
    [
        ('panda', 'heart', True, 0.4),
        ('music', 'rectangle', False, 0.25),
        ('sheep', 'circle', False, 0.5),
    ],
)
def test_plot_shape_on_dataset(dataset_name, shape_name, show_bounds, alpha):
    """Test the plot_shape_on_dataset() function."""
    dataset = DataLoader.load_dataset(dataset_name)
    shape = ShapeFactory(dataset).generate_shape(shape_name)
    ax = plot_shape_on_dataset(dataset, shape, show_bounds, alpha)

    assert isinstance(ax, Axes)
    assert not ax.get_title()

    assert ax.collections[0].get_alpha() == alpha

    points_expected = dataset.data.shape[0]
    if isinstance(shape, PointCollection):
        points_expected += shape.points.shape[0]

    points_plotted = sum(
        collection.get_offsets().data.shape[0] for collection in ax.collections
    )
    assert points_expected == points_plotted

    if isinstance(shape, LineCollection):
        assert len(ax.lines) == len(shape.lines)

    if show_bounds:
        assert sum(isinstance(patch, Rectangle) for patch in ax.patches) == 3
