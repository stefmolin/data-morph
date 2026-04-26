"""Parabola shapes."""

import numpy as np

from ...data.dataset import Dataset
from ..bases.point_collection import PointCollection


class DownParabola(PointCollection):
    """
    Class for the down parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.points import DownParabola

        dataset = DataLoader.load_dataset('panda')
        shape = DownParabola(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=False, alpha=0.25)

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'down_parab'

    def __init__(self, dataset: Dataset) -> None:
        x_bounds, (ymin, ymax) = dataset.data_bounds
        xmin, xmax = x_bounds

        x_offset = x_bounds.range / 10
        xmin += x_offset
        xmax -= x_offset

        poly = np.polynomial.Polynomial.fit(
            [xmin, x_bounds.center, xmax], [ymin, ymax, ymin], 2
        )

        super().__init__(*np.stack(poly.linspace(), axis=1))


class LeftParabola(PointCollection):
    """
    Class for the left parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.points import LeftParabola

        dataset = DataLoader.load_dataset('panda')
        shape = LeftParabola(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=False, alpha=0.25)

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'left_parab'

    def __init__(self, dataset: Dataset) -> None:
        (xmin, xmax), y_bounds = dataset.data_bounds
        ymin, ymax = y_bounds

        y_offset = y_bounds.range / 10
        ymin += y_offset
        ymax -= y_offset

        poly = np.polynomial.Polynomial.fit(
            [ymin, y_bounds.center, ymax], [xmin, xmax, xmin], 2
        )

        super().__init__(*np.stack(poly.linspace()[::-1], axis=1))


class RightParabola(PointCollection):
    """
    Class for the right parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.points import RightParabola

        dataset = DataLoader.load_dataset('panda')
        shape = RightParabola(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=False, alpha=0.25)

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'right_parab'

    def __init__(self, dataset: Dataset) -> None:
        (xmin, xmax), y_bounds = dataset.data_bounds
        ymin, ymax = y_bounds

        y_offset = y_bounds.range / 10
        ymin += y_offset
        ymax -= y_offset

        poly = np.polynomial.Polynomial.fit(
            [ymin, y_bounds.center, ymax], [xmax, xmin, xmax], 2
        )

        super().__init__(*np.stack(poly.linspace()[::-1], axis=1))


class UpParabola(PointCollection):
    """
    Class for the up parabola shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.points import UpParabola

        dataset = DataLoader.load_dataset('panda')
        shape = UpParabola(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=False, alpha=0.25)

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    name = 'up_parab'

    def __init__(self, dataset: Dataset) -> None:
        x_bounds, (ymin, ymax) = dataset.data_bounds
        xmin, xmax = x_bounds

        x_offset = x_bounds.range / 10
        xmin += x_offset
        xmax -= x_offset

        poly = np.polynomial.Polynomial.fit(
            [xmin, x_bounds.center, xmax], [ymax, ymin, ymax], 2
        )

        super().__init__(*np.stack(poly.linspace(), axis=1))
