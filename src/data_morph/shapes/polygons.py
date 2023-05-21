"""Polygon shapes made from lines."""

from ..data.dataset import Dataset
from .bases.line_collection import LineCollection


class Diamond(LineCollection):
    """
    Class for the diamond shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.polygons import Diamond

        _ = Diamond(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        xmin, xmax = dataset.df.x.quantile([0.05, 0.95])
        ymin, ymax = dataset.df.y.quantile([0.05, 0.95])

        xmid = (xmax + xmin) / 2
        ymid = (ymax + ymin) / 2

        super().__init__(
            [[xmin, ymid], [xmid, ymax]],
            [[xmid, ymax], [xmax, ymid]],
            [[xmax, ymid], [xmid, ymin]],
            [[xmid, ymin], [xmin, ymid]],
        )


class Rectangle(LineCollection):
    """
    Class for the rectangle shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.polygons import Rectangle

        _ = Rectangle(DataLoader.load_dataset('panda')).plot()

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        xmin, xmax = dataset.df.x.quantile([0.1, 0.9])
        ymin, ymax = dataset.df.y.quantile([0.1, 0.9])

        super().__init__(
            [[xmin, ymin], [xmin, ymax]],
            [[xmin, ymin], [xmax, ymin]],
            [[xmax, ymin], [xmax, ymax]],
            [[xmin, ymax], [xmax, ymax]],
        )


class Star(LineCollection):
    """
    Class for the star shape.

    .. plot::
       :scale: 75
       :caption:
            This shape is generated using the panda dataset.

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.shapes.polygons import Star

        _ = Star(DataLoader.load_dataset('panda')).plot()

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

        super().__init__(*list(zip(pts[:-1], pts[1:])))
