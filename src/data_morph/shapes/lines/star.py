"""Star shape."""

from ...data.dataset import Dataset
from ..bases.line_collection import LineCollection


class Star(LineCollection):
    """
    Class for the star shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.lines import Star

        _ = Star(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        bounds = dataset.morph_bounds.clone()
        bounds.align_aspect_ratio(shrink=True)

        (xmin, xmax), (ymin, ymax) = bounds
        x_range, y_range = bounds.range

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

        super().__init__(*list(zip(pts[:-1], pts[1:])))
