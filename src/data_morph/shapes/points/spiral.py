"""Spiral shape."""

import numpy as np

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection


class Spiral(PointCollection):
    """
    Class for the spiral shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import Spiral

        _ = Spiral(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.

    Notes
    -----
    This shape uses the formula for an `Archimedean spiral
    <https://en.wikipedia.org/wiki/Archimedean_spiral>`_.
    """

    def __init__(self, dataset: Dataset) -> None:
        max_radius = min(*dataset.morph_bounds.range) / 2

        x_center, y_center = dataset.data_bounds.center
        x_range, y_range = dataset.data_bounds.range
        num_rotations = 3 if x_range >= y_range else 3.25

        # progress of the spiral growing wider (0 to 100%)
        t = np.concatenate(
            [
                np.linspace(0, 0.1, 3, endpoint=False),
                np.linspace(0.1, 0.2, 5, endpoint=False),
                np.linspace(0.2, 0.5, 25, endpoint=False),
                np.linspace(0.5, 0.75, 30, endpoint=False),
                np.linspace(0.75, 1, 35, endpoint=True),
            ]
        )

        # x and y calculations for a spiral
        x = (t * max_radius) * np.cos(2 * num_rotations * np.pi * t) + x_center
        y = (t * max_radius) * np.sin(2 * num_rotations * np.pi * t) + y_center

        super().__init__(*np.stack([x, y], axis=1))
