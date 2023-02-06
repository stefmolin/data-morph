"""Shapes that are composed of curves."""

import numpy as np

from .lines import Lines


class DownParab(Lines):
    """Class for the down parabola shape."""

    def __init__(self, data) -> None:
        q1, q3 = data.y.quantile([0.25, 0.75])

        # TODO: figure out how to use the data to derive these
        curve = [[x, -(((x - 50) / 4) ** 2) + 90] for x in np.arange(0, 100, 3)]

        super().__init__(*[curve[i : i + 2] for i in range(0, len(curve) - 1, 1)])

    def __repr__(self) -> str:
        """Return string representation of the shape."""
        return 'down_parab'


# class UpParab(Lines): # TODO
#     """Class for the up parabola shape."""

#     def __init__(self, data) -> None:
#         # TODO
#         pass

#     def __repr__(self) -> str:
#         """Return string representation of the shape."""
#         return 'up_parab'
