"""Polygon shapes made from lines."""

from ..data.dataset import Dataset
from .bases.line_collection import LineCollection


class Rectangle(LineCollection):
    """
    Class for the rectangle shape.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        xmin, xmax = dataset.data_bounds.x_bounds
        ymin, ymax = dataset.data_bounds.y_bounds

        x_offset = dataset.data_bounds.x_bounds.range / 5
        y_offset = dataset.data_bounds.y_bounds.range / 5

        xmin += x_offset
        xmax -= x_offset

        ymin += y_offset
        ymax -= y_offset

        super().__init__(
            [[xmin, ymin], [xmin, ymax]],
            [[xmin, ymin], [xmax, ymin]],
            [[xmax, ymin], [xmax, ymax]],
            [[xmin, ymax], [xmax, ymax]],
        )


class Star(LineCollection):
    """
    Class for the star shape.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        bounds = dataset.data_bounds.clone()
        bounds.align_aspect_ratio()

        x_bounds = bounds.x_bounds
        y_bounds = bounds.y_bounds

        xmin, xmax = x_bounds
        ymin, ymax = y_bounds

        x_range = x_bounds.range
        y_range = y_bounds.range

        pts = [
            [xmin, ymin + y_range * 0.625],
            [xmin + x_range * 0.375, ymin + y_range * 0.625],
            [xmin + x_range * 0.5, ymax],
            [xmin + x_range * 0.625, ymin + y_range * 0.625],
            [xmax, ymin + y_range * 0.625],
            [xmin + x_range * 0.6875, ymin + y_range * 0.375],
            [xmin + x_range * 0.8125, ymin],
            [xmin + x_range * 0.5, ymin + y_range * 0.25],
            [xmin + x_range * 0.1875, ymin],
            [xmin + x_range * 0.3125, ymin + y_range * 0.375],
            [xmin, ymin + y_range * 0.625],
        ]

        super().__init__(*[line for line in zip(pts[:-1], pts[1:])])
