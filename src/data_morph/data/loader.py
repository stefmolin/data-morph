"""Load and prepare data for morphing."""

import os
from importlib.resources import files
from typing import Iterable, Union

import pandas as pd

from .. import MAIN_DIR


class DataLoader:
    """
    Class for loading and preparing datasets for morphing.

    Parameters
    ----------
    bounds : Iterable[Union[int, float]]
        An iterable of min/max bounds for normalization.
    """

    _DATA_PATH: str = 'data/datasets/'
    _DATASETS: dict = {
        'dino': 'dino.csv',
    }
    AVAILABLE_DATASETS = list(_DATASETS.keys())

    def __init__(self, bounds: Iterable[Union[int, float]]) -> None:
        self._bounds: Iterable[Union[int, float]] = bounds

    def load_dataset(self, dataset: str) -> tuple[str, pd.DataFrame]:
        """
        Load dataset and apply normalization.

        Parameters
        ----------
        name : str
            Either one of :attr:`AVAILABLE_DATASETS` or a path to a
            CSV file containing two columns: x and y.

        Returns
        -------
        pandas.DataFrame
            The normalized dataset for morphing.
        """
        try:
            filepath = files(MAIN_DIR).joinpath(
                f'{self._DATA_PATH}/{self._DATASETS[dataset]}'
            )
            return (dataset, pd.read_csv(filepath).pipe(self._normalize_data))
        except KeyError:
            try:
                # TODO: for custom datasets we need to scale it to be within the
                # bounds of the target datasets or find a map to map the logic to
                # target dataset values dynamically
                return (
                    os.path.splitext(os.path.basename(dataset))[0],
                    pd.read_csv(dataset).pipe(self._normalize_data),
                )
            except FileNotFoundError:
                raise ValueError(
                    f'Unknown dataset "{dataset}". '
                    'Provide a valid path to a CSV dataset or use one of '
                    f'the included datasets: {", ".join(self.AVAILABLE_DATASETS)}.'
                )

    def _normalize_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply normalization.

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame containing columns x and y.

        Returns
        -------
        pandas.DataFrame
            The normalized data.
        """
        a, b = self._bounds
        required_columns = ['x', 'y']
        try:
            return data[required_columns].apply(
                lambda c: a + (c - c.min()).multiply(b - a).div(c.max() - c.min())
            )
        except KeyError:
            missing_columns = ', '.join(
                sorted(set(required_columns).difference(data.columns))
            )
            raise ValueError(
                'Columns "x" and "y" are required for datasets. The provided '
                f'dataset is missing the following column(s): {missing_columns}.'
            )
