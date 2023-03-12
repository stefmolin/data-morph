"""Polygon shapes made from lines."""

from ..data.dataset import Dataset
from .bases.lines import Lines


class Star(Lines):
    """
    Class for the star shape.

    .. plot::
       :scale: 75

        import matplotlib.pyplot as plt
        from data_morph.data.loader import DataLoader
        from data_morph.plotting.style import plot_with_custom_style
        from data_morph.shapes.polygons import Star

        @plot_with_custom_style
        def _plot_star():
            dataset = DataLoader.load_dataset('dino')
            star = Star(dataset)

            fig, ax = plt.subplots()
            for start, end in star.lines:
                ax.plot(*list(zip(start, end)), 'k-')

        _plot_star()

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
