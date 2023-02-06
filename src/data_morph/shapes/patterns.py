"""Shapes that are patterns of lines."""

from .lines import Lines


class XLines(Lines):
    """Class for the X shape consisting of two crossing, perpendicular lines."""

    def __init__(self, data) -> None:
        xmin, ymin = data.min()
        xmax, ymax = data.max()

        super().__init__([[xmin, ymin], [xmax, ymax]], [[xmin, ymax], [xmax, ymin]])

    def __repr__(self) -> str:
        """Return string representation of the shape."""
        return 'x'
