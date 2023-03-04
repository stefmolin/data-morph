"""Utility functions for working with intervals."""

from numbers import Number
from typing import Iterable


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
