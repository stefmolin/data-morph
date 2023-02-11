"""Utility functions for styling Matplotlib plots."""

from functools import wraps
from importlib.resources import as_file, files
from typing import Any, Callable

import matplotlib.pyplot as plt

from .. import MAIN_DIR


def plot_with_custom_style(plotting_function: Callable) -> Callable:
    """
    Wrap a plotting function with a context manager to set the plot style.

    Parameters
    ----------
    plotting_function : Callable
        The plotting function.

    Returns
    -------
    Callable
        The decorated plotting function.
    """

    @wraps(plotting_function)
    def plot_in_style(*args, **kwargs) -> Any:
        """
        Use a context manager to set the plot style before running
        the plotting function.

        Parameters
        ----------
        *args
            Positional arguments to pass to the plotting function.
        *kwargs
            Keyword arguments to pass to the plotting function.

        Returns
        -------
        any
            Output of calling the plotting function.
        """
        style = files(MAIN_DIR).joinpath('viz/config/plot_style.mplstyle')
        with as_file(style) as style_path:
            with plt.style.context(style_path):
                output = plotting_function(*args, **kwargs)
        return output

    return plot_in_style
