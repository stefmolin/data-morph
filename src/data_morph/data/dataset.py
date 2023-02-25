"""Class representing a dataset for morphing."""

from typing import Iterable, Union

import pandas as pd


class Dataset:
    """
    Class for starting data to morph into another shape.

    Parameters
    ----------
    name : str
        The name to use for the dataset.
    df : pandas.DataFrame
        DataFrame containing columns x and y.
    bounds : Iterable[Union[int, float]], optional
        An iterable of min/max bounds for normalization.
    """

    REQUIRED_COLUMNS = ['x', 'y']

    def __init__(
        self, name: str, df: pd.DataFrame, bounds: Iterable[Union[int, float]] = None
    ) -> None:
        self.name: str = name
        self.df: pd.DataFrame = self._validate_data(df)

        if bounds is not None and not (
            isinstance(bounds, (tuple, list))
            and len(bounds) == 2
            and all(
                isinstance(x, (float, int)) and not isinstance(x, bool) for x in bounds
            )
        ):
            raise ValueError('bounds must be an iterable of 2 numeric values or None')

        self._bounds: Iterable[Union[int, float]] = bounds

        if self._bounds:
            self.df = self._normalize_data()
        else:  # TODO: should this store bounds as xbounds and ybounds?
            self._bounds = [self.df.min().min(), self.df.max().max()]

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} name={self.name}>'  # TODO: add bounds here

    def _normalize_data(self) -> pd.DataFrame:
        """
        Apply normalization.

        Returns
        -------
        pandas.DataFrame
            The normalized data.
        """
        a, b = self._bounds
        return self.df[self.REQUIRED_COLUMNS].apply(
            lambda c: a + (c - c.min()).multiply(b - a).div(c.max() - c.min())
        )

    def _validate_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate the data.

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame for morphing.

        Returns
        -------
        pandas.DataFrame
            DataFrame provided it contains columns x and y.
        """
        required = set(self.REQUIRED_COLUMNS)
        missing_columns = required.difference(data.columns)

        if missing_columns:
            case_insensitive_missing = missing_columns.difference(
                data.columns.str.lower()
            )
            if case_insensitive_missing:
                raise ValueError(
                    'Columns "x" and "y" are required for datasets. The provided '
                    'dataset is missing the following column(s): '
                    f"{', '.join(sorted(missing_columns))}."
                )
            data = data.rename(columns={col.upper(): col for col in missing_columns})

        return data
