"""Vertical lines shape."""

import numpy as np

from ...data.dataset import Dataset
from ..bases.line_collection import LineCollection


class VerticalLines(LineCollection):
    """
    Class for the vertical lines shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.lines import VerticalLines

        dataset = DataLoader.load_dataset('panda')
        shape = VerticalLines(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=False, alpha=0.25)

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'v_lines'

    def __init__(self, dataset: Dataset) -> None:
        x_bounds, y_bounds = dataset.data_bounds

        super().__init__(
            *[
                [[x, y_bounds[0]], [x, y_bounds[1]]]
                for x in np.linspace(x_bounds[0], x_bounds[1], 5)
            ]
        )
