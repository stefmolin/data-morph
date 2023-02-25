"""Load data for morphing."""

import os
from importlib.resources import files
from typing import Iterable, Union

import pandas as pd

from .. import MAIN_DIR
from .dataset import Dataset


class DataLoader:
    """Class for loading datasets for morphing."""

    _DATA_PATH: str = 'data/starter_shapes/'
    _DATASETS: dict = {
        'dino': 'dino.csv',
        'panda': 'panda.csv',
    }
    AVAILABLE_DATASETS = list(_DATASETS.keys())

    def __init__(self) -> None:
        raise NotImplementedError

    @classmethod
    def load_dataset(
        cls, dataset: str, bounds: Iterable[Union[int, float]] = None
    ) -> Dataset:
        """
        Load dataset.

        Parameters
        ----------
        dataset : str
            Either one of :attr:`AVAILABLE_DATASETS` or a path to a
            CSV file containing two columns: x and y.
        bounds : Iterable[Union[int, float]], optional
            An iterable of min/max bounds for normalization.

        Returns
        -------
        Dataset
            The starting dataset for morphing.
        """
        try:
            filepath = files(MAIN_DIR).joinpath(
                f'{cls._DATA_PATH}/{cls._DATASETS[dataset]}'
            )
            name = dataset
            df = pd.read_csv(filepath)
        except KeyError:
            try:
                name = os.path.splitext(os.path.basename(dataset))[0]
                df = pd.read_csv(dataset)
            except FileNotFoundError:
                raise ValueError(
                    f'Unknown dataset "{dataset}". '
                    'Provide a valid path to a CSV dataset or use one of '
                    f'the included datasets: {", ".join(cls.AVAILABLE_DATASETS)}.'
                )
        return Dataset(name=name, df=df, bounds=bounds)
