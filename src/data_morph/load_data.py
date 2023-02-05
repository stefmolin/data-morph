"""Functions for loading and preparing data for morphing."""

from importlib.resources import files
import os

import pandas as pd

from . import MAIN_DIR


DATASETS = {
    'dino': 'dino.csv',
}

def load_dataset(dataset):
    """Loads the example data sets used in the paper.

    Args:
        name (str): One of 'dino', 'rando', 'slant', or 'big_slant'

    Returns:
        pd.DataFrame: A ``DataFrame`` with ``x`` and ``y`` columns
    """
    try:
        return dataset, pd.read_csv(files(MAIN_DIR).joinpath(f'data/{DATASETS[dataset]}'))
    except KeyError:
        try:
            # TODO: for custom datasets we need to scale it to be within the 
            # bounds of the target datasets or find a map to map the logic to
            # target dataset values dynamically
            return os.path.splitext(os.path.basename(dataset))[0], pd.read_csv(dataset)
        except FileNotFoundError:
            raise ValueError(
                f'Unknown dataset "{dataset}". '
                'Provide a valid path to a CSV dataset or use one of '
                f'the included datasets: {", ".join(DATASETS.keys())}.'
            )