"""Club shape."""

from numbers import Number

import numpy as np

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection


class Club(PointCollection):
    """
    Class for the club shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.shapes.points import Club

        _ = Club(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        scale_factor = min(*dataset.data_bounds.range) / 75

        x_lobes, y_lobes = self._get_lobes(scale_factor)
        x_stem, y_stem = self._get_stem(scale_factor)

        x_center, y_center = dataset.data_bounds.center
        xs = x_center + np.concatenate(x_lobes + x_stem)
        ys = y_center + np.concatenate(y_lobes + y_stem)

        super().__init__(*np.stack([xs, ys], axis=1))

    @staticmethod
    def _get_arc(
        r: Number,
        t: np.ndarray,
        angle_offset: np.float64,
        x_offset: Number,
        y_offset: Number,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Get arc of a circle.

        Parameters
        ----------
        r : Number
            The radius of the circle.
        t : numpy.ndarray
            The values to sample at in radians.
        angle_offset : numpy.float64
            Angle at which to start the arc in radians.
        x_offset : Number
            A constant value to shift the *x* coordinates by.
        y_offset : Number
            A constant value to shift the *y* coordinates by.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray]
            The *x* and *y* coordinates for the arc.
        """
        x = r * np.cos(t + angle_offset) + x_offset
        y = r * np.sin(t + angle_offset) + y_offset
        return x, y

    @classmethod
    def _get_lobes(
        cls, scale_factor: Number
    ) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """
        Get the lobes of the club.

        Parameters
        ----------
        scale_factor : Number
            The factor to scale up/down the radius of the arcs used to calculate the lobes.

        Returns
        -------
        tuple[list[numpy.ndarray], list[numpy.ndarray]]
            The *x* and *y* coordinates for the lobes.
        """
        radius = 15 * scale_factor
        top_lobe_y_offset = 18 * scale_factor
        bottom_lobes_x_offset = 15 * scale_factor
        bottom_lobes_y_offset = 9 * scale_factor

        t = np.linspace(0, (2 - 1 / 3) * np.pi, num=30)

        x_top, y_top = cls._get_arc(radius, t, -np.pi / 3, 0, top_lobe_y_offset)
        x_bottom_left, y_bottom_left = cls._get_arc(
            radius, t, np.pi / 3, -bottom_lobes_x_offset, -bottom_lobes_y_offset
        )
        x_bottom_right, y_bottom_right = cls._get_arc(
            radius, t, np.pi, bottom_lobes_x_offset, -bottom_lobes_y_offset
        )

        x_lobes = [x_top, x_bottom_left, x_bottom_right]
        y_lobes = [y_top, y_bottom_left, y_bottom_right]

        return x_lobes, y_lobes

    @classmethod
    def _get_stem(
        cls, scale_factor: Number
    ) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """
        Get the stem of the club.

        Parameters
        ----------
        scale_factor : Number
            The factor to scale up/down the stem.

        Returns
        -------
        tuple[list[numpy.ndarray], list[numpy.ndarray]]
            The *x* and *y* coordinates for the stem.
        """
        stem_x_offset = 8 * scale_factor
        stem_y_offset = 34 * scale_factor
        stem_scaler = 0.35 / scale_factor
        stem_x_pad = 1.5 * scale_factor

        # stem bottom
        x_line = np.linspace(-stem_x_offset, stem_x_offset, num=8)
        y_line = np.repeat(-stem_y_offset, 8)

        # left part of the stem
        x_left = np.linspace(-(stem_x_offset - stem_x_pad), -stem_x_pad, num=6)
        y_left = stem_scaler * np.power(x_left + stem_x_offset, 2) - stem_y_offset

        # right part of the stem
        x_right = np.linspace(stem_x_pad, stem_x_offset - stem_x_pad, num=6)
        y_right = stem_scaler * np.power(x_right - stem_x_offset, 2) - stem_y_offset

        x_stem = [x_line, x_left, x_right]
        y_stem = [y_line, y_left, y_right]

        return x_stem, y_stem
