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
        center = (dataset.df.x.mean(), dataset.df.y.mean())
        points = [center]
        max_radius = max(dataset.df.x.std(), dataset.df.y.std())
        for radius in np.linspace(max_radius // 5, max_radius, num=5):
            for angle in np.linspace(0, 360, num=50, endpoint=False):
                points.append(
                    (
                        center[0]
                        + np.cos(angle) * radius
                        + rng.standard_normal() * max_radius,
                        center[1]
                        + np.sin(angle) * radius
                        + rng.standard_normal() * max_radius,
                    )
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
