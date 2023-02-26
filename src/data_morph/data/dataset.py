"""Class representing a dataset for morphing."""

from typing import Iterable, Union

import pandas as pd

from .bounds import Bounds


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

        self._bounds: Bounds = Bounds(bounds, inclusive=True)

        if self._bounds:
            self.df = self._normalize_data()

        # TODO: make a _derive_bounds() method here
        # TODO: range/5 is still a bit arbitrary (need to take into account density at the edges)
        # TODO: allow x_bounds and y_bounds for different aspect ratios?
        # this might not work with the shapes (circle could be a ellipse?)
        # will need to test with a vertical/horizontal line of points as
        # the starting shape
        # TODO: to preserve the aspect ratio, pick the bounds with the largest range
        # and use that value to extend the morph bounds into the plot bounds for 
        # both dimensions
        # TODO: add tests for this logic
        self.x_morph_bounds, self.y_morph_bounds = [
            Bounds((self.df[dim].min(), self.df[dim].max()), inclusive=False)
            for dim in self.REQUIRED_COLUMNS
        ]

        # TODO: should create a class that handles all of this logic
        x_offset = self.x_morph_bounds.range
        self.x_morph_bounds.adjust_bounds(x_offset / 5)
        self.x_plot_bounds = self.x_morph_bounds.clone()
        self.x_plot_bounds.adjust_bounds(x_offset / 5)

        y_offset = self.y_morph_bounds.range
        self.y_morph_bounds.adjust_bounds(y_offset / 5)
        self.y_plot_bounds = self.y_morph_bounds.clone()
        self.y_plot_bounds.adjust_bounds(y_offset / 5)

        print(self.x_morph_bounds, self.y_morph_bounds)
        print(self.x_plot_bounds, self.y_plot_bounds)
        print(x_offset, y_offset)

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} name={self.name} '
            # f'x_bounds={self.x_bounds} y_bounds={self.y_bounds}>'
            # TODO: here we would print the repr of the Bounds objects inside
        )

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
