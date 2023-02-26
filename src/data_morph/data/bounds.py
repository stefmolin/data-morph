"""Classes for working with bounds."""

from typing import Iterable, Union


class Bounds:
    """Class representing a range of numeric values."""

    def __init__(
        self,
        bounds: Union[Iterable[Union[int, float]], None] = None,
        inclusive: bool = False,
    ) -> None:
        self.bounds = self._validate_bounds(bounds)
        self.inclusive = inclusive
    
    def __bool__(self) -> bool:
        return self.bounds is not None

    def __contains__(self, value: Union[int, float]) -> bool:
        if not self:
            return True
        if self.inclusive:
            return self.bounds[0] <= value <= self.bounds[1]
        return self.bounds[0] < value < self.bounds[1]

    def __getitem__(self, index: int) -> Union[int, float]:
        return self.bounds[index]

    def __iter__(self) -> Union[int, float]:
        return iter(self.bounds)
    
    def __repr__(self) -> str:
        if self.inclusive:
            sep = '[]'
            kind = 'inclusive'
        else:
            sep = '()'
            kind = 'exclusive'
        return f'<Bounds {kind} {sep[0]}{", ".join(map(str, self.bounds))}{sep[1]}>'

    @staticmethod
    def _validate_2d(data: Iterable[Union[int, float]], name: str) -> Iterable[Union[int, float]]:
        """
        Validate the data is 2D.

        Parameters
        ----------
        data : Iterable[Union[int, float]]
            Data in two dimensions (e.g., a point or bounds).

        Returns
        -------
        Iterable[Union[int, float]]
            The validated data.
        """
        if not (
            isinstance(data, (tuple, list))
            and len(data) == 2
            and all(
                isinstance(x, (float, int)) and not isinstance(x, bool) for x in data
            )
        ):
            raise ValueError(f'{name} must be an iterable of 2 numeric values')

        return data

    def _validate_bounds(self, bounds: Iterable[Union[int, float]]) -> Iterable[Union[int, float]]:
        """
        Validate the proposed bounds.

        Parameters
        ----------
        bounds : Iterable[Union[int, float]]
            An iterable of min/max bounds.

        Returns
        -------
        Iterable[Union[int, float]]
            An iterable of min/max bounds.
        """
        if bounds is None:
            return bounds 
        return list(self._validate_2d(bounds, 'bounds'))

    def adjust_bounds(self, value: Union[float, int]) -> None:
        # TODO: look for a way to check if the value is a number but not boolean
        # maybe numbers.number? but would need to allow numpy types too
        if isinstance(value, bool) or not isinstance(value, (float, int)):
            raise ValueError('value must be a numeric value')
        if not value:
            raise ValueError('value must be non-zero.')
        
        offset = value / 2
        self.bounds[0] -= offset 
        self.bounds[1] += offset
    
    def clone(self) -> "Bounds":
        return Bounds(self.bounds[:], self.inclusive)

    @property
    def range(self) -> Union[int, float]:
        return self.bounds[1] - self.bounds[0]


class BoundingBox:
    
    def __init__(
        self,
        x_bounds: Iterable[Union[int, float]],
        y_bounds: Iterable[Union[int, float]],
        inclusive: Iterable[bool] = False,
    ):
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
        self.x_bounds = Bounds(x_bounds, inclusive[0])
        self.y_bounds = Bounds(y_bounds, inclusive[1])
    
    def __contains__(self, value: Iterable[Union[int, float]]) -> bool:
        x, y = self._validate_2d(value, 'input')
        return x in self.x_bounds and y in self.y_bounds