"""Classes for working with bounds."""

from numbers import Number
from typing import Iterable, Union


def _validate_2d(
    data: Iterable[Number], name: str, validate_range: bool
) -> Iterable[Number]:
    """
    Validate the data is exactly two-dimensional and contains strictly
    increasing numeric values.

    Parameters
    ----------
    data : Iterable[Number]
        Data in two dimensions (e.g., a point or bounds).
    name : str
        The name of the value being passed in as ``data`` (for error messages).
    validate_range : bool
        Whether to also validate that ``data`` is a valid range
        (end of range >= to start of range).

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

    if validate_range and data[0] >= data[1]:
        raise ValueError(f'{name}[0] must be strictly less than {name}[1]')
    return data


class Bounds:
    """
    Class representing a range of numeric values.

    Parameters
    ----------
    bounds : Union[Iterable[Number], None]
        A 2-dimensional numeric iterable or ``None`` for no bounds.
    inclusive : bool, default ``False``
        Whether the bounds include the endpoints. Default
        is exclusive.
    """

    def __init__(
        self,
        bounds: Union[Iterable[Number], None] = None,
        inclusive: bool = False,
    ) -> None:
        self.bounds = self._validate_bounds(bounds)
        self.inclusive = inclusive

    def __bool__(self) -> bool:
        return self.bounds is not None

    def __contains__(self, value: Number) -> bool:
        if not self:
            return True
        if self.inclusive:
            return self.bounds[0] <= value <= self.bounds[1]
        return self.bounds[0] < value < self.bounds[1]

    def __getitem__(self, index: int) -> Number:
        return self.bounds[index]

    def __iter__(self) -> Number:
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
        if bounds is None:
            return bounds
        return list(_validate_2d(bounds, 'bounds', validate_range=True))

    def adjust_bounds(self, value: Number) -> None:
        if isinstance(value, bool) or not isinstance(value, Number):
            raise ValueError('value must be a numeric value')
        if not value:
            raise ValueError('value must be non-zero.')

        offset = value / 2
        self.bounds[0] -= offset
        self.bounds[1] += offset

    def clone(self) -> 'Bounds':
        return Bounds(self.bounds[:], self.inclusive)

    @property
    def range(self) -> Number:
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
        if inclusive is None:
            inclusive = [False] * 2
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
        x, y = _validate_2d(value, 'input', validate_range=False)
        return x in self.x_bounds and y in self.y_bounds

    def __repr__(self) -> str:
        return '<BoundingBox>\n' f'  x={self.x_bounds}' '\n' f'  y={self.y_bounds}'

    def adjust_bounds(self, x: Number = None, y: Number = None) -> None:
        if not x and not y:
            raise ValueError('At least one of x or y must be non-zero.')
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
