"""Scatter shape."""

from numbers import Number

import numpy as np

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection


class Scatter(PointCollection):
    """
    Class for the scatter shape: a cloud of randomly-scattered points.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import Scatter

        _ = Scatter(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        rng = np.random.default_rng(1)
        morph_range = dataset.morph_bounds.range
        center = dataset.morph_bounds.center
        points = [center]
        points.extend(
            [
                (
                    center[0] + np.cos(angle) * rng.uniform(0, morph_range[0] / 2),
                    center[1] + np.sin(angle) * rng.uniform(0, morph_range[1] / 2),
                )
                for angle in np.linspace(0, 720, num=100, endpoint=False)
            ]
        )
        super().__init__(*points)

        self._alpha = 0.4

    def distance(self, x: Number, y: Number) -> int:
        """
        No-op that allows returns 0 so that all perturbations are accepted.

        Parameters
        ----------
        x, y : int or float
            Coordinates of a point in 2D space.

        Returns
        -------
        int
            Always returns 0 to allow for scattering of the points.
        """
        return 0
