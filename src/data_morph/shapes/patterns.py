"""Shapes that are patterns of lines."""

from .lines import Lines


class HorizontalLines(Lines):
    """Class for the horizontal lines shape."""

    def __init__(self, data) -> None:
        # xmin, ymin = data.min()[['x', 'y']]
        # xmax, ymax = data.max()[['x', 'y']]

        super().__init__(
            *[[[0, y], [100, y]] for y in [10, 30, 50, 70, 90]]
        )  # TODO: figure out the values based on the data

    def __repr__(self) -> str:
        """Return string representation of the shape."""
        return 'h_lines'


class XLines(Lines):
    """Class for the X shape consisting of two crossing, perpendicular lines."""

    def __init__(self, data) -> None:
        xmin, ymin = data.min()
        xmax, ymax = data.max()

        super().__init__([[xmin, ymin], [xmax, ymax]], [[xmin, ymax], [xmax, ymin]])

    def __repr__(self) -> str:
        """Return string representation of the shape."""
        return 'x'
