"""Functions for loading and preparing data for morphing."""

from importlib.resources import files
import os

import pandas as pd

from . import MAIN_DIR


DATASETS = {
    'dino': 'dino.csv',
}

def load_dataset(dataset, bounds):
    """
    Load dataset and apply normalization.

    Parameters
    ----------
    name : str
        Either one of TODO or a path to a CSV file containing two columns: x and y.

    Returns
    -------
    pandas.DataFrame
    """
    try:
        return (
            dataset,
            read_normalize_data(files(MAIN_DIR).joinpath(f'data/{DATASETS[dataset]}'), bounds)
        )
    except KeyError:
        try:
            # TODO: for custom datasets we need to scale it to be within the 
            # bounds of the target datasets or find a map to map the logic to
            # target dataset values dynamically
            return os.path.splitext(os.path.basename(dataset))[0], read_normalize_data(dataset, bounds)
        except FileNotFoundError:
            raise ValueError(
                f'Unknown dataset "{dataset}". '
                'Provide a valid path to a CSV dataset or use one of '
                f'the included datasets: {", ".join(DATASETS.keys())}.'
            )

def read_normalize_data(filepath, bounds):
    
    a, b = bounds
    return pd.read_csv(filepath).assign(
        x=lambda df: a + (df.x - df.x.min()).multiply(b - a).div(df.x.max() - df.x.min()),
        y=lambda df: a + (df.y - df.y.min()).multiply(b - a).div(df.y.max() - df.y.min()),
    )