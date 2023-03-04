"""Class representing a dataset for morphing."""

from numbers import Number
from typing import Iterable

import pandas as pd

from ..bounds.bounding_box import BoundingBox
from ..bounds.interval import Interval


class Dataset:
    """
    Class for starting data to morph into another shape.

    Parameters
    ----------
    name : str
        The name to use for the dataset.
    df : pandas.DataFrame
        DataFrame containing columns x and y.
    x_bounds, y_bounds : Iterable[Number], optional
        An iterable of min/max bounds for normalization.
    """

    REQUIRED_COLUMNS = ['x', 'y']

    def __init__(
        self,
        name: str,
        df: pd.DataFrame,
        x_bounds: Iterable[Number] = None,
        y_bounds: Iterable[Number] = None,
    ) -> None:
        self.name: str = name
        self.df: pd.DataFrame = self._validate_data(df).pipe(
            self._normalize_data, x_bounds, y_bounds
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
        # could also make this a parameter to __init__()
        self.morph_bounds = BoundingBox(
            *[
                Interval([self.df[dim].min(), self.df[dim].max()], inclusive=False)
                for dim in self.REQUIRED_COLUMNS
            ]
        )

        x_offset, y_offset = [offset / 5 for offset in self.morph_bounds.range]

        self.morph_bounds.adjust_bounds(x=x_offset, y=y_offset)

        self.plot_bounds = self.morph_bounds.clone()
        self.plot_bounds.adjust_bounds(x=x_offset, y=y_offset)
        self.plot_bounds.align_aspect_ratio()

    def _normalize_data(
        self, df, x_bounds: Iterable[Number], y_bounds: Iterable[Number]
    ) -> pd.DataFrame:
        """
        Apply normalization.

        Parameters
        ----------
        df : pandas.DataFrame
            The data to normalize.
        x_bounds, y_bounds : Iterable[Number], optional
            The desired minimum/maximum values. Either pass both or none.

        Returns
        -------
        pandas.DataFrame
            The normalized data.
        """
        if (x_bounds is None and y_bounds is not None) or (
            x_bounds is not None and y_bounds is None
        ):
            raise ValueError(
                "Either don't supply bounds or supply both x and y bounds."
            )
        if x_bounds is None and y_bounds is None:
            self.normalized = False
            return df

        for col, bounds in [('x', x_bounds), ('y', y_bounds)]:
            a, b = Interval(bounds, inclusive=True)
            df = df.assign(
                **{
                    col: lambda c: (a + (c[col] - c[col].min()))
                    .multiply(b - a)
                    .div(c[col].max() - c[col].min())
                }
            )

        self.normalized = True
        return df

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
