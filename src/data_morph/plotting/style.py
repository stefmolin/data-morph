"""Utility functions for styling Matplotlib plots."""

from collections.abc import Generator
from contextlib import contextmanager
from functools import wraps
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any, Callable

import matplotlib.pyplot as plt

from .. import MAIN_DIR


@contextmanager
def style_context() -> Generator[None, None, None]:
    """Context manager for plotting in a custom style."""

    style = files(MAIN_DIR).joinpath(
        Path('plotting') / 'config' / 'plot_style.mplstyle'
    )
    with (
        as_file(style) as style_path,
        plt.style.context(['seaborn-v0_8-darkgrid', style_path]),
    ):
        yield


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
    @style_context()
    def plot_in_style(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """
        Use a context manager to set the plot style before running
        the plotting function.

        Parameters
        ----------
        *args
            Positional arguments to pass to the plotting function.
        **kwargs
            Keyword arguments to pass to the plotting function.

        Returns
        -------
        any
            Output of calling the plotting function.
        """
        return plotting_function(*args, **kwargs)

    return plot_in_style
