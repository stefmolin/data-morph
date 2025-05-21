"""Bullseye shape."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .rings import Rings

if TYPE_CHECKING:
    from ..data.dataset import Dataset


class Bullseye(Rings):
    """
    Class representing a bullseye shape comprising two concentric circles.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.circles import Bullseye

        _ = Bullseye(DataLoader.load_dataset('panda')).plot()

    See Also
    --------
    Circle : The individual rings are represented as circles.
    """

    @staticmethod
    def _derive_radii(dataset: Dataset) -> np.ndarray:
        """
        Derive the radii for the circles in the bullseye.

        Parameters
        ----------
        dataset : Dataset
            The starting dataset to morph into.

        Returns
        -------
        np.ndarray
            The radii for the circles in the bullseye.
        """
        stdev = dataset.data[['x', 'y']].std().mean() * 1.5
        return np.linspace(stdev, 0, 2, endpoint=False)
