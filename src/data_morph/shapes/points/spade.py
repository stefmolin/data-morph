"""Spade shape."""

from numbers import Number

import numpy as np

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection
from .heart import Heart


class Spade(PointCollection):
    """
    Class for the spade shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import Spade

        _ = Spade(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        _, xmax = dataset.data_bounds.x_bounds
        x_shift, y_shift = dataset.data_bounds.center

        # upside-down heart
        heart_points = self._get_inverted_heart(dataset, y_shift)

        # base of the spade
        base_x, base_y = self._get_base(xmax, x_shift, y_shift)

        # combine all points
        x = np.concatenate((heart_points[:, 0], base_x), axis=0)
        y = np.concatenate((heart_points[:, 1], base_y), axis=0)

        super().__init__(*np.stack([x, y], axis=1))

    @staticmethod
    def _get_inverted_heart(dataset: Dataset, y_shift: Number) -> np.ndarray:
        """
        Get points for an inverted heart.

        Parameters
        ----------
        dataset : Dataset
            The starting dataset to morph into other shapes.
        y_shift : Number
            The constant value to shift the *y* up/down by.

        Returns
        -------
        numpy.ndarray
            The points for the upside-down heart.

        See Also
        --------
        Heart : This shape is reused to calculate the spade.
        """
        heart_points = Heart(dataset).points
        heart_points[:, 1] = -heart_points[:, 1] + 2 * y_shift
        return heart_points

    @staticmethod
    def _get_base(
        xmax: Number, x_shift: Number, y_shift: Number
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Get the base of the spade.

        Parameters
        ----------
        xmax : Number
            The maximum *x* value for the shape.
        x_shift : Number
            The constant value to shift the *x* left/right by.
        y_shift : Number
            The constant value to shift the *y* up/down by.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray]
            The *x* and *y* coordinates for the base of the spade.
        """
        # line base
        line_x = np.linspace(-6, 6, num=12)
        line_y = np.repeat(-16, 12)

        # left wing
        left_x = np.linspace(-6, 0, num=12)
        left_y = 0.278 * np.power(left_x + 6, 2) - 16

        # right wing
        right_x = np.linspace(0, 6, num=12)
        right_y = 0.278 * np.power(right_x - 6, 2) - 16

        # shift and scale the base and wing
        base_x = np.concatenate((line_x, left_x, right_x), axis=0)
        base_y = np.concatenate((line_y, left_y, right_y), axis=0)

        # scale by the half the widest width of the spade
        scale_factor = (xmax - x_shift) / 16

        base_x = base_x * scale_factor + x_shift
        base_y = base_y * scale_factor + y_shift

        return base_x, base_y
