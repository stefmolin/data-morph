"""Run Data Morph CLI from start shape to end shape preserving summary statistics."""

from __future__ import annotations

import argparse
import itertools
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING

from . import __version__
from .data.loader import DataLoader
from .morpher import DataMorpher
from .progress import DataMorphProgress
from .shapes.factory import ShapeFactory

if TYPE_CHECKING:
    from collections.abc import Sequence

    from rich.progress import TaskID

ARG_DEFAULTS = {
    'output_dir': 'morphed_data',
    'decimals': 2,
    'min_shake': 0.3,
    'iterations': 100_000,
    'freeze': 0,
    'workers': 2,
}


def generate_parser() -> argparse.ArgumentParser:
    """
    Generate an argument parser for the CLI.

    Returns
    -------
    argparse.argparse.ArgumentParser
        Argument parser class for the CLI.
    """

    parser = argparse.ArgumentParser(
        prog='data-morph',
        description=(
            'Morph an input dataset of 2D points into select shapes, while '
            'preserving the summary statistics to a given number of decimal '
            'points through simulated annealing.'
        ),
        epilog=(
            'Source code available at https://github.com/stefmolin/data-morph.'
            ' CLI reference and examples are at '
            'https://stefaniemolin.com/data-morph/stable/cli.html.'
        ),
    )

    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '-w',
        '--workers',
        type=int,
        default=ARG_DEFAULTS['workers'],
        help=(
            f'The number of workers. Default {ARG_DEFAULTS["workers"]}. '
            'Pass 0 to use as many as possible.'
        ),
    )

    shape_config_group = parser.add_argument_group(
        'Shape Configuration (required)',
        description='Specify the start and target shapes.',
    )
    shape_config_group.add_argument(
        '--start',
        '--start-shape',
        dest='start_shape',
        required=True,
        nargs='+',
        help=(
            'The starting shape(s). A valid starting shape could be any of '
            f'{DataLoader.AVAILABLE_DATASETS} or a path to a CSV file, '
            "in which case it should have two columns 'x' and 'y'. "
            'See the documentation for visualizations of the built-in datasets.'
        ),
    )
    shape_config_group.add_argument(
        '--target',
        '--target-shape',
        dest='target_shape',
        required=True,
        nargs='+',
        help=(
            'The shape(s) to convert to. If multiple shapes are provided, the starting shape '
            'will be converted to each target shape separately. Valid target shapes are '
            f"""'{"', '".join(ShapeFactory.AVAILABLE_SHAPES)}'. Use 'all' to convert to """
            'all target shapes in a single run.'
            ' See the documentation for visualizations of the available target shapes.'
        ),
    )

    morph_config_group = parser.add_argument_group(
        'Morph Configuration', description='Configure the morphing process.'
    )
    morph_config_group.add_argument(
        '--decimals',
        default=ARG_DEFAULTS['decimals'],
        type=int,
        choices=range(0, 6),
        help=(
            'The number of decimal places to preserve equality. '
            f'Defaults to {ARG_DEFAULTS["decimals"]}.'
        ),
    )
    morph_config_group.add_argument(
        '--iterations',
        default=ARG_DEFAULTS['iterations'],
        type=int,
        help=(
            'The number of iterations to run. '
            f'Defaults to {ARG_DEFAULTS["iterations"]:,d}. '
            'Datasets with more observations may require more iterations.'
        ),
    )
    morph_config_group.add_argument(
        '--scale',
        default=None,
        type=float,
        help=(
            'Scale the data on both x and y by dividing by a scale factor. '
            'For example, ``--scale 10`` divides all x and y values by 10. '
            'Datasets with large values will morph faster after scaling down.'
        ),
    )
    morph_config_group.add_argument(
        '--seed',
        default=None,
        type=int,
        help='Provide a seed for reproducible results.',
    )
    morph_config_group.add_argument(
        '--shake',
        default=ARG_DEFAULTS['min_shake'],
        type=float,
        help=(
            'The standard deviation for the random movement applied in each '
            'direction, which will be sampled from a normal distribution with '
            'a mean of zero. Note that morphing initially sets the shake to 1, '
            'and then decreases the shake value over time toward the minimum value '
            f'defined here, which defaults to {ARG_DEFAULTS["min_shake"]}. Datasets '
            'with large values may benefit from scaling (see ``--scale``) '
            'or increasing this towards 1, along with increasing the number of '
            'iterations (see ``--iterations``).'
        ),
    )

    file_group = parser.add_argument_group(
        'Output File Configuration',
        description='Customize where files are written to and which types of files are kept.',
    )
    file_group.add_argument(
        '--keep-frames',
        default=False,
        action='store_true',
        help=(
            'Whether to keep individual frame images in the output directory.'
            " If you don't pass this, the frames will be deleted after the GIF file"
            ' is created.'
        ),
    )
    file_group.add_argument(
        '-o',
        '--output-dir',
        default=ARG_DEFAULTS['output_dir'],
        metavar='DIRECTORY',
        help=(
            'Path to a directory for writing output files. '
            f'Defaults to ``{ARG_DEFAULTS["output_dir"]}``.'
        ),
    )
    file_group.add_argument(
        '--write-data',
        default=False,
        action='store_true',
        help='Whether to write CSV files to the output directory with the data for each frame.',
    )

    frame_group = parser.add_argument_group(
        'Animation Configuration', description='Customize aspects of the animation.'
    )
    frame_group.add_argument(
        '--ease',
        default=False,
        action='store_true',
        help=(
            'Whether to slow down the transition near the start and end of the '
            'transformation. This is a shortcut for --ease-in --ease-out. This only '
            'affects the frames selected, not the algorithm.'
        ),
    )
    frame_group.add_argument(
        '--ease-in',
        default=False,
        action='store_true',
        help=(
            'Whether to slowly start the transition from input to target in the '
            'animation. This only affects the frames selected, not the algorithm.'
        ),
    )
    frame_group.add_argument(
        '--ease-out',
        default=False,
        action='store_true',
        help=(
            'Whether to slow down the transition from input to target towards the end '
            'of the animation. This only affects the frames selected, not the algorithm.'
        ),
    )
    frame_group.add_argument(
        '--forward-only',
        default=False,
        action='store_true',
        help=(
            'By default, this module will create an animation that plays '
            'first forward (applying the transformation) and then rewinds, '
            'playing backward to undo the transformation. Pass this argument '
            'to only play the animation in the forward direction before looping.'
        ),
    )
    frame_group.add_argument(
        '--freeze',
        default=ARG_DEFAULTS['freeze'],
        type=int,
        metavar='NUM_FRAMES',
        help=(
            'Number of frames to freeze at the first and final frame of the transition '
            'in the animation. This only affects the frames selected, not the algorithm. '
            f'Defaults to {ARG_DEFAULTS["freeze"]}.'
        ),
    )

    return parser


def _morph(
    data: str,
    shape: str,
    args: argparse.Namespace,
    progress: multiprocessing.DictProxy,
    task_id: TaskID,
) -> None:
    """
    Run the morphing algorithm.

    Parameters
    ----------
    data : str
        The dataset to use. This can be the name of a built-in dataset or a path to a
        CSV file containing the data.
    shape : str
        The name of the target shape.
    args : argparse.Namespace
        Command line arguments.
    progress : multiprocessing.DictProxy
        The state of all task progresses.
    task_id : TaskID
        The task ID assigned by the progress tracker.

    Notes
    -----
    This should only be used with :func:`._parallelize`.
    """
    progress[task_id] = {'progress': 0, 'total': args.iterations}

    dataset = DataLoader.load_dataset(data, scale=args.scale)
    shape = ShapeFactory(dataset).generate_shape(shape)

    morpher = DataMorpher(
        decimals=args.decimals,
        output_dir=args.output_dir,
        write_data=args.write_data,
        seed=args.seed,
        keep_frames=args.keep_frames,
        forward_only_animation=args.forward_only,
        num_frames=100,
        in_notebook=False,
    )

    _ = morpher.morph(
        start_shape=dataset,
        target_shape=shape,
        iterations=args.iterations,
        min_shake=args.shake,
        ease_in=args.ease_in or args.ease,
        ease_out=args.ease_out or args.ease,
        freeze_for=args.freeze,
        progress=progress,
        task_id=task_id,
    )


def _parallelize(
    total_jobs: int,
    workers: int,
    args: argparse.Namespace,
    target_shapes: Sequence[str],
) -> None:
    """
    Run morphing algorithm in parallel.

    Parameters
    ----------
    total_jobs : int
        The total number of morphing jobs that need to be run.
    workers : int
        The number of worker processes to use.
    args : argparse.Namespace
        The command line arguments.
    target_shapes : Sequence[str]
        The target shapes for morphing (datasets are in ``args.start_shape``).
    """
    only_show_running = total_jobs > workers

    with (
        DataMorphProgress() as progress_tracker,
        multiprocessing.Manager() as manager,
    ):
        task_progress = manager.dict()
        overall_progress_task = progress_tracker.add_task('[green]Overall progress')

        with ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(
                    _morph,
                    dataset,
                    shape,
                    args,
                    task_progress,
                    progress_tracker.add_task(
                        f'{Path(dataset).stem} to {shape}', visible=False, start=False
                    ),
                )
                for dataset, shape in itertools.product(args.start_shape, target_shapes)
            ]

            while True:
                finished_jobs = sum(future.done() for future in futures)
                progress_tracker.update(
                    overall_progress_task,
                    completed=sum(task['progress'] for task in task_progress.values()),
                    total=total_jobs * args.iterations,
                )
                for task_id, update_data in task_progress.items():
                    latest = update_data['progress']
                    total = update_data['total']

                    if not latest:
                        # hack to make the elapsed time accurate for ones that start later on
                        # this is necessary because rich.progress.Progress is not pickleable
                        progress_tracker.start_task(task_id)

                    progress_tracker.update(
                        task_id,
                        completed=latest,
                        total=total,
                        visible=latest < total
                        if only_show_running
                        else latest <= total,
                    )
                if finished_jobs == total_jobs:
                    break

            for future in futures:
                future.result()


def _serialize(args: argparse.Namespace, target_shapes: Sequence[str]) -> None:
    """
    Run the morphing algorithm serially.

    Parameters
    ----------
    args : argparse.Namespace
        The command line arguments.
    target_shapes : Sequence[str]
        The target shapes for morphing (datasets are in ``args.start_shape``).
    """
    for start_shape in args.start_shape:
        dataset = DataLoader.load_dataset(start_shape, scale=args.scale)

        shape_factory = ShapeFactory(dataset)
        morpher = DataMorpher(
            decimals=args.decimals,
            output_dir=args.output_dir,
            write_data=args.write_data,
            seed=args.seed,
            keep_frames=args.keep_frames,
            forward_only_animation=args.forward_only,
            num_frames=100,
            in_notebook=False,
        )

        for target_shape in target_shapes:
            _ = morpher.morph(
                start_shape=dataset,
                target_shape=shape_factory.generate_shape(target_shape),
                iterations=args.iterations,
                min_shake=args.shake,
                ease_in=args.ease_in or args.ease,
                ease_out=args.ease_out or args.ease,
                freeze_for=args.freeze,
            )


def main(argv: Sequence[str] | None = None) -> None:
    """
    Run Data Morph as a script.

    Parameters
    ----------
    argv : Sequence[str] | None, optional
        Makes it possible to pass in options without running on
        the command line.
    """

    args = generate_parser().parse_args(argv)

    target_shapes = (
        ShapeFactory.AVAILABLE_SHAPES
        if args.target_shape == 'all' or 'all' in args.target_shape
        else set(args.target_shape).intersection(ShapeFactory.AVAILABLE_SHAPES)
    )
    if not target_shapes:
        raise ValueError(
            'No valid target shapes were provided. Valid options are '
            f"""'{"', '".join(ShapeFactory.AVAILABLE_SHAPES)}'."""
        )

    total_jobs = len(args.start_shape) * len(target_shapes)

    max_workers = multiprocessing.cpu_count()
    workers = max_workers if not args.workers else min(args.workers, max_workers)

    if total_jobs > 1 and workers > 1:
        _parallelize(total_jobs, workers, args, target_shapes)
    else:
        _serialize(args, target_shapes)
