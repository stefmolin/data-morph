"""Functions for loading and preparing data for morphing."""

from importlib.resources import files
import os
from typing import Iterable, Tuple, Union

import pandas as pd

from . import MAIN_DIR


DATASETS = {
    'dino': 'dino.csv',
}

def load_dataset(dataset: str, bounds: Iterable[Union[int, float]]) -> Tuple[str, pd.DataFrame]:
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
    """
    try:
        filepath = files(MAIN_DIR).joinpath(f'data/{DATASETS[dataset]}')
        return (
            dataset,
            pd.read_csv(filepath).pipe(normalize_data, bounds)
        )
    except KeyError:
        try:
            # TODO: for custom datasets we need to scale it to be within the 
            # bounds of the target datasets or find a map to map the logic to
            # target dataset values dynamically
            return (
                os.path.splitext(os.path.basename(dataset))[0],
                pd.read_csv(dataset).pipe(normalize_data, bounds)
            )
        except FileNotFoundError:
            raise ValueError(
                f'Unknown dataset "{dataset}". '
                'Provide a valid path to a CSV dataset or use one of '
                f'the included datasets: {", ".join(DATASETS.keys())}.'
            )

def normalize_data(data: pd.DataFrame, bounds: Iterable[Union[int, float]]) -> pd.DataFrame:
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
    """
    a, b = bounds
    return data.assign(
        x=lambda df: a + (df.x - df.x.min()).multiply(b - a).div(df.x.max() - df.x.min()),
        y=lambda df: a + (df.y - df.y.min()).multiply(b - a).div(df.y.max() - df.y.min()),
    )