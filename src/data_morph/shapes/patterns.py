"""Shapes that are patterns of lines."""

from ..data.dataset import Dataset
from .bases.lines import Lines


class HighLines(Lines):
    """
    Class for the high lines shape.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        x_bounds = dataset.morph_bounds.x_bounds
        y_bounds = dataset.data_bounds.y_bounds

        offset = y_bounds.range / 5
        lower = y_bounds[0] + offset
        upper = y_bounds[1] - offset

        super().__init__(
            [[x_bounds[0], lower], [x_bounds[1], lower]],
            [[x_bounds[0], upper], [x_bounds[1], upper]],
        )

    def __str__(self) -> str:
        return 'high_lines'


class HorizontalLines(Lines):
    """Class for the horizontal lines shape."""

    def __init__(self, dataset: Dataset) -> None:
        # xmin, ymin = dataset.df.min()[['x', 'y']]
        # xmax, ymax = dataset.df.max()[['x', 'y']]

        super().__init__(
            *[[[0, y], [100, y]] for y in [10, 30, 50, 70, 90]]
        )  # TODO: figure out the values based on the data

    def __str__(self) -> str:
        return 'h_lines'


class SlantDownLines(Lines):
    """Class for the slant down lines shape."""

    def __init__(self, dataset: Dataset) -> None:
        # q1, q3 = dataset.df.y.quantile([0.25, 0.75])

        super().__init__(
            [[0, 100], [100, 0]],
            [[0, 70], [70, 0]],
            [[30, 100], [100, 30]],
            [[0, 50], [50, 0]],
            [[50, 100], [100, 50]],
        )  # TODO: figure out how to use the data to derive these

    def __str__(self) -> str:
        return 'slant_down'


class SlantUpLines(Lines):
    """Class for the slant up lines shape."""

    def __init__(self, dataset: Dataset) -> None:
        # q1, q3 = dataset.df.y.quantile([0.25, 0.75])

        super().__init__(
            [[0, 0], [100, 100]],
            [[0, 30], [70, 100]],
            [[30, 0], [100, 70]],
            [[50, 0], [100, 50]],
            [[0, 50], [50, 100]],
        )  # TODO: figure out how to use the data to derive these

    def __str__(self) -> str:
        return 'slant_up'


class VerticalLines(Lines):
    """Class for the vertical lines shape."""

    def __init__(self, dataset: Dataset) -> None:
        # xmin, ymin = dataset.df.min()[['x', 'y']]
        # xmax, ymax = dataset.df.max()[['x', 'y']]

        super().__init__(
            *[[[x, 0], [x, 100]] for x in [10, 30, 50, 70, 90]]
        )  # TODO: figure out the values based on the data

    def __str__(self) -> str:
        return 'v_lines'


class WideLines(Lines):
    """
    Class for the wide lines shape.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        q1, q3 = dataset.df.x.quantile([0.25, 0.75])

        super().__init__(
            [[q1, 0], [q1, 100]], [[q3, 0], [q3, 100]]
        )  # TODO: figure out way to get 0, 100 min/max plus offset?

    def __str__(self) -> str:
        return 'wide_lines'


class XLines(Lines):
    """
    Class for the X shape consisting of two crossing, perpendicular lines.

    Parameters
    ----------
    dataset : Dataset
        The starting dataset to morph into other shapes.
    """

    def __init__(self, dataset: Dataset) -> None:
        xmin, ymin = dataset.df.min()
        xmax, ymax = dataset.df.max()

        super().__init__([[xmin, ymin], [xmax, ymax]], [[xmin, ymax], [xmax, ymin]])

    def __str__(self) -> str:
        return 'x'
