"""Progress bar using rich."""

from rich.progress import BarColumn, MofNCompleteColumn, Progress, TimeElapsedColumn


class DataMorphProgress(Progress):
    """
    Progress tracker for Data Morph.

    .. note::
        Both the Python interface and CLI provide progress tracking using this class
        automatically. It is unlikely you will need to use this class yourself.

    Parameters
    ----------
    auto_refresh : bool, default ``True``
        Whether to automatically refresh the progress bar. This should be set to ``False``
        for Jupyter Notebooks per the `Rich progress documentation
        <https://rich.readthedocs.io/en/stable/progress.html>`_.

    See Also
    --------
    rich.progress.Progress
        The base class from which all progress bar functionality derives.
    """

    def __init__(self, auto_refresh: bool = True) -> None:
        super().__init__(
            '[progress.description]{task.description}',
            BarColumn(),
            '[progress.percentage]{task.percentage:>3.0f}%',
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            auto_refresh=auto_refresh,
        )
