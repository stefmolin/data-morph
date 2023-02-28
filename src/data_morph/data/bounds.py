"""Classes for working with bounds."""

from numbers import Number
from typing import Iterable, Union


def _validate_2d(data: Iterable[Number], name: str) -> Iterable[Number]:
    """
    Validate the data is exactly two-dimensional.

    Parameters
    ----------
    data : Iterable[Number]
        Data in two dimensions (e.g., a point or bounds).
    name : str
        The name of the value being passed in as ``data`` (for error messages).

    Returns
    -------
    Iterable[Number]
        The validated data.
    """
    if not (
        isinstance(data, (tuple, list))
        and len(data) == 2
        and all(isinstance(x, Number) and not isinstance(x, bool) for x in data)
    ):
        raise ValueError(f'{name} must be an iterable of 2 numeric values')

    return data


class Bounds:
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
        ``value`` is in the bounds.

        Parameters
        ----------
        value : Number
            A numeric value.

        Returns
        -------
        bool
            Whether ``value`` is contained in the bounds.
        """
        if not isinstance(value, Number) or isinstance(value, bool) or value is None:
            raise TypeError('This operation is only supported for numeric values.')

        if self.inclusive:
            return self.bounds[0] <= value <= self.bounds[1]
        return self.bounds[0] < value < self.bounds[1]

    def __eq__(self, other: 'Bounds') -> bool:
        """
        Check whether two :class:`Bounds` objects are equivalent.

        Parameters
        ----------
        other : Bounds
            A :class:`Bounds` object.

        Returns
        -------
        bool
            Whether the two :class:`Bounds` objects are equivalent.
        """
        if not isinstance(other, Bounds):
            raise TypeError('Equality is only defined between Bounds objects.')
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
        return f'<Bounds {kind} {interval}>'

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

    def clone(self) -> 'Bounds':
        """
        Clone this instance.

        Returns
        -------
        :class:`Bounds`
            A new :class:`Bounds` instance with the same bounds.
        """
        return Bounds(self.bounds[:], self.inclusive)

    @property
    def range(self) -> Number:
        """
        Calculate the range (width) of the bounds.

        Returns
        -------
        Number
            The range covered by the bounds.
        """
        return self.bounds[1] - self.bounds[0]


class BoundingBox:
    """
    Class representing 2-dimensional range of numeric values.

    Parameters
    ----------
    x_bounds, y_bounds : Union[Bounds, Iterable[Number]]
        A 2-dimensional numeric iterable or a :class:`Bounds` object.
    inclusive : bool, default ``False``
        Whether the bounds include the endpoints. Default
        is exclusive. If :class:`Bounds` objects are provided,
        their settings are used.
    """

    def __init__(
        self,
        x_bounds: Union[Bounds, Iterable[Number]],
        y_bounds: Union[Bounds, Iterable[Number]],
        inclusive: Iterable[bool] = False,
    ):
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
            if isinstance(x_bounds, Bounds)
            else Bounds(x_bounds, inclusive[0])
        )
        self.y_bounds = (
            y_bounds.clone()
            if isinstance(y_bounds, Bounds)
            else Bounds(y_bounds, inclusive[1])
        )

    def __contains__(self, value: Iterable[Number]) -> bool:
        """
        Add support for using the ``in`` operator to check whether
        a two-dimensional point is in the bounding box.

        Parameters
        ----------
        value : Iterable[Number]
            A two-dimensional point.

        Returns
        -------
        bool
            Whether ``value`` is contained in the bounding box.
        """
        x, y = _validate_2d(value, 'input')
        return x in self.x_bounds and y in self.y_bounds

    def __eq__(self, other: 'BoundingBox') -> bool:
        """
        Check whether two :class:`BoundingBox` objects are equivalent.

        Parameters
        ----------
        other : BoundingBox
            A :class:`BoundingBox` object.

        Returns
        -------
        bool
            Whether the two :class:`BoundingBox` objects are equivalent.
        """
        if not isinstance(other, BoundingBox):
            raise TypeError('Equality is only defined between BoundingBox objects.')
        return self.x_bounds == other.x_bounds and self.y_bounds == other.y_bounds

    def __repr__(self) -> str:
        return '<BoundingBox>\n' f'  x={self.x_bounds}' '\n' f'  y={self.y_bounds}'

    def adjust_bounds(self, x: Number = None, y: Number = None) -> None:
        """
        Adjust bounding box range.

        Parameters
        ----------
        x, y : Number
            The amount to change the x/y bound range by (half will be applied to each end).

        See Also
        --------
        :meth:`Bounds.adjust_bounds` : Method that performs the adjustment.
        """
        if x:
            self.x_bounds.adjust_bounds(x)
        if y:
            self.y_bounds.adjust_bounds(y)

    def align_aspect_ratio(self) -> None:
        x_range, y_range = self.range
        diff = x_range - y_range
        if diff < 0:
            self.adjust_bounds(x=-diff)
        elif diff > 0:
            self.adjust_bounds(y=diff)

    def clone(self) -> 'BoundingBox':
        return BoundingBox(
            self.x_bounds.clone(),
            self.y_bounds.clone(),
        )

    @property
    def range(self) -> Iterable[Number]:
        return self.x_bounds.range, self.y_bounds.range
