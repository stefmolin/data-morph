"""Functions for loading and preparing data for morphing."""

import os
from importlib.resources import files
from typing import Iterable, Tuple, Union

import pandas as pd

from . import MAIN_DIR

DATASETS = {
    'dino': 'dino.csv',
}


def load_dataset(
    dataset: str, bounds: Iterable[Union[int, float]]
) -> Tuple[str, pd.DataFrame]:
    """
    Load dataset and apply normalization.

    Parameters
    ----------
    name : str
        Either one of TODO or a path to a CSV file containing two columns: x and y.
    bounds : Iterable[Union[int, float]]
        An iterable of min/max bounds for normalization.

    Returns
    -------
    pandas.DataFrame
        The normalized dataset for morphing.
    """
    try:
        filepath = files(MAIN_DIR).joinpath(f'data/{DATASETS[dataset]}')
        return (dataset, pd.read_csv(filepath).pipe(normalize_data, bounds))
    except KeyError:
        try:
            # TODO: for custom datasets we need to scale it to be within the
            # bounds of the target datasets or find a map to map the logic to
            # target dataset values dynamically
            return (
                os.path.splitext(os.path.basename(dataset))[0],
                pd.read_csv(dataset).pipe(normalize_data, bounds),
            )
        except FileNotFoundError:
            raise ValueError(
                f'Unknown dataset "{dataset}". '
                'Provide a valid path to a CSV dataset or use one of '
                f'the included datasets: {", ".join(DATASETS.keys())}.'
            )


def normalize_data(
    data: pd.DataFrame, bounds: Iterable[Union[int, float]]
) -> pd.DataFrame:
    """
    Apply normalization.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing columns x and y.
    bounds : Iterable[Union[int, float]]
        An iterable of min/max bounds for normalization.

    Returns
    -------
    pandas.DataFrame
        The normalized data.
    """
    a, b = bounds
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
