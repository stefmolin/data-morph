"""Class for working with two-dimensional bounds."""

from __future__ import annotations

from collections.abc import Iterable
from numbers import Number

from ._utils import _validate_2d
from .interval import Interval


class BoundingBox:
    """
    Class representing 2-dimensional range of numeric values.

    Parameters
    ----------
    x_bounds, y_bounds : Interval | Iterable[numbers.Number]
        A 2-dimensional numeric iterable or an :class:`.Interval` object.
    inclusive : bool, default ``False``
        Whether the bounds include the endpoints. Default
        is exclusive. If :class:`.Interval` objects are provided,
        their settings are used.
    """

    def __init__(
        self,
        x_bounds: Interval | Iterable[Number],
        y_bounds: Interval | Iterable[Number],
        inclusive: Iterable[bool] = False,
    ) -> None:
        if x_bounds is None or y_bounds is None:
            raise ValueError('BoundingBox requires bounds for both dimensions.')

        if isinstance(inclusive, bool):
            inclusive = [inclusive] * 2
        if not (
            isinstance(inclusive, (tuple, list))
            and len(inclusive) == 2
            and all(isinstance(x, bool) for x in inclusive)
        ):
            raise ValueError(
                'inclusive must be an iterable of 2 Boolean values'
                ' or a single Boolean value'
            )

        self.x_bounds = (
            x_bounds.clone()
            if isinstance(x_bounds, Interval)
            else Interval(x_bounds, inclusive[0])
        )
        """Interval: The bounds for the x direction."""

        self.y_bounds = (
            y_bounds.clone()
            if isinstance(y_bounds, Interval)
            else Interval(y_bounds, inclusive[1])
        )
        """Interval: The bounds for the y direction."""

    def __contains__(self, value: Iterable[Number]) -> bool:
        """
        Add support for using the ``in`` operator to check whether
        a two-dimensional point is in the bounding box.

        Parameters
        ----------
        value : Iterable[numbers.Number]
            A two-dimensional point.

        Returns
        -------
        bool
            Whether ``value`` is contained in the bounding box.
        """
        x, y = _validate_2d(value, 'input')
        return x in self.x_bounds and y in self.y_bounds

    def __eq__(self, other: BoundingBox) -> bool:
        """
        Check whether two :class:`.BoundingBox` objects are equivalent.

        Parameters
        ----------
        other : BoundingBox
            A :class:`.BoundingBox` object.

        Returns
        -------
        bool
            Whether the two :class:`.BoundingBox` objects are equivalent.
        """
        if not isinstance(other, BoundingBox):
            raise TypeError('Equality is only defined between BoundingBox objects.')
        return self.x_bounds == other.x_bounds and self.y_bounds == other.y_bounds

    def __repr__(self) -> str:
        return '<BoundingBox>\n' f'  x={self.x_bounds}' '\n' f'  y={self.y_bounds}'

    def adjust_bounds(self, x: Number | None = None, y: Number | None = None) -> None:
        """
        Adjust bounding box range.

        Parameters
        ----------
        x : numbers.Number, optional
            The amount to change the x bound range by (half will be applied to each end).
        y : numbers.Number, optional
            The amount to change the y bound range by (half will be applied to each end).

        See Also
        --------
        :meth:`.Interval.adjust_bounds` : Method that performs the adjustment.
        """
        if x:
            self.x_bounds.adjust_bounds(x)
        if y:
            self.y_bounds.adjust_bounds(y)

    def align_aspect_ratio(self) -> None:
        """Align the aspect ratio to 1:1."""
        x_range, y_range = self.range
        diff = x_range - y_range
        if diff < 0:
            self.adjust_bounds(x=-diff)
        elif diff > 0:
            self.adjust_bounds(y=diff)

    @property
    def aspect_ratio(self) -> Number:
        """
        Calculate the aspect ratio of the bounding box.

        Returns
        -------
        numbers.Number
            The range in the x direction divided by the range in the y direction.
        """
        x_range, y_range = self.range
        return x_range / y_range

    def clone(self) -> BoundingBox:
        """
        Clone this instance.

        Returns
        -------
        BoundingBox
            A new :class:`.BoundingBox` instance with the same bounds.
        """
        return BoundingBox(
            self.x_bounds.clone(),
            self.y_bounds.clone(),
        )

    @property
    def range(self) -> Iterable[Number]:
        """
        Calculate the range (width) of the bounding box in each direction.

        Returns
        -------
        Iterable[numbers.Number]
            The range covered by the x and y bounds, respectively.
        """
        return self.x_bounds.range, self.y_bounds.range
