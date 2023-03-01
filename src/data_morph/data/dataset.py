"""Class representing a dataset for morphing."""

from numbers import Number
from typing import Iterable

import pandas as pd

from .bounds import BoundingBox, Bounds


class Dataset:
    """
    Class for starting data to morph into another shape.

    Parameters
    ----------
    name : str
        The name to use for the dataset.
    df : pandas.DataFrame
        DataFrame containing columns x and y.
    bounds : Iterable[Number], optional
        An iterable of min/max bounds for normalization.
    """

    REQUIRED_COLUMNS = ['x', 'y']

    def __init__(
        self, name: str, df: pd.DataFrame, bounds: Iterable[Number] = None
    ) -> None:
        self.name: str = name
        self.df: pd.DataFrame = self._validate_data(df).pipe(
            self._normalize_data, bounds
        )
        self._derive_bounds()

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} name={self.name} '
            f'normalized={self.normalized}>'
        )

    def _derive_bounds(self) -> None:
        """Derive morphing and plotting bounds based on the data."""
        # TODO: range/5 is still a bit arbitrary (need to take into account density at the edges)
        # TODO: add tests for this logic
        self.morph_bounds = BoundingBox(
            *[
                Bounds([self.df[dim].min(), self.df[dim].max()], inclusive=False)
                for dim in self.REQUIRED_COLUMNS
            ]
        )

        x_offset, y_offset = [offset / 5 for offset in self.morph_bounds.range]

        self.morph_bounds.adjust_bounds(x=x_offset, y=y_offset)

        self.plot_bounds = self.morph_bounds.clone()
        self.plot_bounds.adjust_bounds(x=x_offset, y=y_offset)
        self.plot_bounds.align_aspect_ratio()

    def _normalize_data(self, df, bounds: Iterable[Number]) -> pd.DataFrame:
        """
        Apply normalization.

        Parameters
        ----------
        df : pandas.DataFrame
            The data to normalize.
        bounds : Iterable[Number]
            The desired minimum/maximum values.

        Returns
        -------
        pandas.DataFrame
            The normalized data.
        """
        if bounds is None:
            self.normalized = False
            return df

        a, b = Bounds(bounds, inclusive=True)
        normalized_df = df[self.REQUIRED_COLUMNS].apply(
            lambda c: a + (c - c.min()).multiply(b - a).div(c.max() - c.min())
        )
        self.normalized = True
        return normalized_df

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
