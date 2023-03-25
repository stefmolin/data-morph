"""Class representing a dataset for morphing."""

from numbers import Number

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes

from ..bounds.bounding_box import BoundingBox
from ..bounds.interval import Interval
from ..plotting.style import plot_with_custom_style


class Dataset:
    """
    Class for representing a starting dataset and bounds.

    .. plot::
        :caption:
            Upon creation, these bounds are automatically calculated.
            Use :meth:`plot` to generate this visualization.

        from data_morph.data.loader import DataLoader
        _ = DataLoader.load_dataset('panda').plot()

    Parameters
    ----------
    name : str
        The name to use for the dataset.
    df : pandas.DataFrame
        DataFrame containing columns x and y.
    scale : numbers.Number, optional
        The factor to scale the data by (can be used to speed up morphing).
        Values in the data's x and y columns will be divided by this value.

    See Also
    --------
    DataLoader
        Utility for creating :class:`Dataset` objects from CSV files.
    """

    _REQUIRED_COLUMNS = ['x', 'y']

    def __init__(
        self,
        name: str,
        df: pd.DataFrame,
        scale: Number,
    ) -> None:
        self.df: pd.DataFrame = self._validate_data(df).pipe(self._scale_data, scale)
        """pandas.DataFrame: DataFrame containing columns x and y."""

        self.name: str = name
        """str: The name to use for the dataset."""

        self.data_bounds: BoundingBox = self._derive_data_bounds()
        """BoundingBox: The bounds of the data."""

        self.morph_bounds: BoundingBox = self._derive_morphing_bounds()
        """BoundingBox: The limits for the morphing process."""

        self.plot_bounds: BoundingBox = self._derive_plotting_bounds()
        """BoundingBox: The bounds to use when plotting the morphed data."""

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} name={self.name} ' f'scaled={self._scaled}>'

    def _derive_data_bounds(self) -> None:
        """
        Derive bounds based on the data.

        Returns
        -------
        BoundingBox
            The bounds of the data.
        """
        return BoundingBox(
            *[
                Interval([self.df[dim].min(), self.df[dim].max()], inclusive=False)
                for dim in self._REQUIRED_COLUMNS
            ]
        )

    def _derive_morphing_bounds(self) -> None:
        """
        Derive morphing bounds based on the data.

        Returns
        -------
        BoundingBox
            The bounds of the morphing process.
        """
        # TODO: range * 0.2 is still a bit arbitrary (need to take into account density at the edges)
        # could also make this a parameter to __init__()
        morph_bounds = self.data_bounds.clone()

        x_offset, y_offset = [offset * 0.2 for offset in self.data_bounds.range]

        morph_bounds.adjust_bounds(x=x_offset, y=y_offset)
        return morph_bounds

    def _derive_plotting_bounds(self) -> None:
        """
        Derive plotting bounds based on the morphing bounds.

        Returns
        -------
        BoundingBox
            The bounds of the plot.
        """
        # TODO: range * 0.2 is still a bit arbitrary (need to take into account density at the edges)
        # could also make this a parameter to __init__()
        x_offset, y_offset = [offset * 0.2 for offset in self.data_bounds.range]

        plot_bounds = self.morph_bounds.clone()
        plot_bounds.adjust_bounds(x=x_offset, y=y_offset)
        plot_bounds.align_aspect_ratio()
        return plot_bounds

    def _scale_data(self, df, scale: Number) -> pd.DataFrame:
        """
        Apply scaling to the data.

        Parameters
        ----------
        df : pandas.DataFrame
            The data to scale.
        scale : numbers.Number, optional
            The factor to scale the data by (can be used to speed up morphing).
            Values in the data's x and y columns will be divided by this value.

        Returns
        -------
        pandas.DataFrame
            The scaled data.
        """
        if scale is None:
            self._scaled = False
            return df

        scaled_df = df.assign(x=df.x.div(scale), y=df.y.div(scale))
        self._scaled = True
        return scaled_df

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
        required = set(self._REQUIRED_COLUMNS)
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

    @plot_with_custom_style
    def plot(self, ax: Axes = None) -> Axes:
        """
        Plot the dataset and its bounds.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            An optional :class:`~matplotlib.axes.Axes` object to plot on.

        Returns
        -------
        matplotlib.axes.Axes
            The :class:`~matplotlib.axes.Axes` object containing the plot.
        """
        if not ax:
            fig, ax = plt.subplots(layout='constrained')
            fig.get_layout_engine().set(w_pad=0.2, h_pad=0.2)

        ax.axis('equal')
        ax = self.df.plot(kind='scatter', x='x', y='y', color='k', ax=ax, title=self)
        ax.set(xlabel='', ylabel='')

        scale_base = 85

        # data bounds
        x_offset = self.data_bounds.x_bounds.range / scale_base
        y_offset = self.data_bounds.y_bounds.range / scale_base
        data_rectangle = [
            self.data_bounds.x_bounds[0] - x_offset,
            self.data_bounds.y_bounds[0] - y_offset,
        ]

        ax.add_patch(
            plt.Rectangle(
                data_rectangle,
                width=self.data_bounds.x_bounds.range + x_offset * 2,
                height=self.data_bounds.y_bounds.range + y_offset * 2,
                ec='blue',
                linewidth=2,
                fill=False,
            )
        )
        ax.text(
            (self.df.x.max() + self.df.x.min()) / 2,
            self.df.y.max() + self.data_bounds.y_bounds.range / scale_base,
            'DATA BOUNDS',
            color='blue',
            va='bottom',
            ha='center',
        )

        # morph bounds
        morph_rectangle = [self.morph_bounds.x_bounds[0], self.morph_bounds.y_bounds[0]]
        ax.add_patch(
            plt.Rectangle(
                morph_rectangle,
                width=self.morph_bounds.x_bounds.range,
                height=self.morph_bounds.y_bounds.range,
                ec='red',
                linewidth=2,
                fill=False,
            )
        )
        ax.text(*morph_rectangle, ' MORPH BOUNDS', color='red', va='bottom', ha='left')

        # plot bounds
        plot_rectangle = [self.plot_bounds.x_bounds[0], self.plot_bounds.y_bounds[0]]
        ax.add_patch(
            plt.Rectangle(
                plot_rectangle,
                width=self.plot_bounds.x_bounds.range,
                height=self.plot_bounds.y_bounds.range,
                ec='#7CA1CC',
                linewidth=2,
                fill=False,
            )
        )
        ax.text(
            *plot_rectangle, ' PLOT BOUNDS', color='#7CA1CC', va='bottom', ha='left'
        )

        ax.autoscale()
        return ax
