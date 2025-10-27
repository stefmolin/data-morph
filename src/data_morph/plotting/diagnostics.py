"""Diagnostic plot to visualize a shape superimposed on the dataset."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..plotting.style import plot_with_custom_style

if TYPE_CHECKING:
    from numbers import Number

    from matplotlib.axes import Axes

    from ..data.dataset import Dataset
    from ..shapes.bases.shape import Shape


@plot_with_custom_style
def plot_shape_on_dataset(
    dataset: Dataset,
    shape: Shape,
    show_bounds: bool = False,
    alpha: Number = 0.25,
) -> Axes:
    """
    Plot a shape superimposed on a dataset to evaluate heuristics.

    Parameters
    ----------
    dataset : Dataset
        The dataset that ``shape`` was instantiated with.
    shape : Shape
        The shape that was instantiated with ``dataset``.
    show_bounds : bool, default ``False``
        Whether to include the dataset's bounds in the plot.
    alpha : Number, default ``0.25``
        The transparency to use for the dataset's points.

    Returns
    -------
    matplotlib.axes.Axes
        The :class:`~matplotlib.axes.Axes` object containing the plot.

    Examples
    --------

    .. plot::
       :scale: 75
       :include-source:
       :caption:
            Visualization of the :class:`.Star` shape when calculated based on the
            music :class:`.Dataset`, with the dataset's bounds.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.lines import Star

        dataset = DataLoader.load_dataset('music')
        shape = Star(dataset)
        plot_shape_on_dataset(dataset, shape, show_bounds=True, alpha=0.1)

    .. plot::
       :scale: 75
       :include-source:
       :caption:
            Visualization of the :class:`.Heart` shape when calculated based on the
            music :class:`.Dataset`, without the dataset's bounds.

        from data_morph.data.loader import DataLoader
        from data_morph.plotting.diagnostics import plot_shape_on_dataset
        from data_morph.shapes.points import Heart

        dataset = DataLoader.load_dataset('music')
        shape = Heart(dataset)
        plot_shape_on_dataset(dataset, shape, alpha=0.1)
    """
    ax = dataset.plot(show_bounds=show_bounds, title=None, alpha=alpha)
    shape.plot(ax=ax)
    return ax
