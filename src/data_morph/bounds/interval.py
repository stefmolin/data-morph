"""Class for working with bounds."""

from numbers import Number
from typing import Iterable

from .utils import _validate_2d


class Interval:
    """
    Class representing a range of numeric values.

    Parameters
    ----------
    bounds : Iterable[Number]
        A 2-dimensional numeric iterable.
    inclusive : bool, default ``False``
        Whether the bounds include the endpoints. Default
        is exclusive.
    """

    def __init__(
        self,
        bounds: Iterable[Number],
        inclusive: bool = False,
    ) -> None:
        self.bounds = self._validate_bounds(bounds)
        self.inclusive = inclusive

    def __contains__(self, value: Number) -> bool:
        """
        Add support for using the ``in`` operator to check whether
        ``value`` is in the interval.

        Parameters
        ----------
        value : Number
            A numeric value.

        Returns
        -------
        bool
            Whether ``value`` is contained in the interval.
        """
        if not isinstance(value, Number) or isinstance(value, bool) or value is None:
            raise TypeError('This operation is only supported for numeric values.')

        if self.inclusive:
            return self.bounds[0] <= value <= self.bounds[1]
        return self.bounds[0] < value < self.bounds[1]

    def __eq__(self, other: 'Interval') -> bool:
        """
        Check whether two :class:`Interval` objects are equivalent.

        Parameters
        ----------
        other : Interval
            A :class:`Interval` object.

        Returns
        -------
        bool
            Whether the two :class:`Interval` objects are equivalent.
        """
        if not isinstance(other, Interval):
            raise TypeError('Equality is only defined between Interval objects.')
        return self.bounds == other.bounds and self.inclusive == other.inclusive

    def __getitem__(self, index: int) -> Number:
        """
        Add support for indexing into the bounds.

        Parameters
        ----------
        index : int
            The index to access.

        Returns
        -------
        Number
            The value for the bounds at ``index``.
        """
        return self.bounds[index]

    def __iter__(self) -> Number:
        """
        Iterate over the bounds.

        Returns
        -------
        Number
            The next value of the bounds.
        """
        return iter(self.bounds)

    def __repr__(self) -> str:
        values = ', '.join(map(str, self.bounds))
        if self.inclusive:
            interval = f'[{values}]'
            kind = 'inclusive'
        else:
            interval = f'({values})'
            kind = 'exclusive'
        return f'<Interval {kind} {interval}>'

    def _validate_bounds(self, bounds: Iterable[Number]) -> Iterable[Number]:
        """
        Validate the proposed bounds.

        Parameters
        ----------
        bounds : Iterable[Number]
            An iterable of min/max bounds.

        Returns
        -------
        Iterable[Number]
            An iterable of min/max bounds.
        """
        bounds = list(_validate_2d(bounds, 'bounds'))

        if bounds[0] >= bounds[1]:
            raise ValueError('Right bound must be strictly greater than left bound.')
        return bounds

    def adjust_bounds(self, value: Number) -> None:
        """
        Adjust bound range.

        Parameters
        ----------
        value : Number
            The amount to change the range by (half will be applied to each end).
        """
        if isinstance(value, bool) or not isinstance(value, Number) or value is None:
            raise TypeError('value must be a numeric value')
        if not value:
            raise ValueError('value must be non-zero')

        offset = value / 2
        self.bounds[0] -= offset
        self.bounds[1] += offset

    def clone(self) -> 'Interval':
        """
        Clone this instance.

        Returns
        -------
        :class:`Interval`
            A new :class:`Interval` instance with the same bounds.
        """
        return Interval(self.bounds[:], self.inclusive)

    @property
    def range(self) -> Number:
        """
        Calculate the range (width) of the interval.

        Returns
        -------
        Number
            The range covered by the interval.
        """
        return abs(self.bounds[1] - self.bounds[0])
