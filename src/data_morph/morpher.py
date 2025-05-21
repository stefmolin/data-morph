"""Module containing data morphing logic."""

from __future__ import annotations

from contextlib import nullcontext
from functools import partial
from numbers import Number
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from .data.stats import get_summary_statistics
from .plotting.animation import (
    ease_in_out_quadratic,
    ease_in_out_sine,
    ease_in_sine,
    ease_out_sine,
    linear,
    stitch_gif_animation,
)
from .plotting.static import plot
from .progress import DataMorphProgress

if TYPE_CHECKING:
    import multiprocessing

    import pandas as pd
    from rich.progress import TaskID

    from .bounds.bounding_box import BoundingBox
    from .data.dataset import Dataset
    from .shapes.bases.shape import Shape


class DataMorpher:
    """
    Class for morphing a dataset into a target shape, preserving summary statistics.

    Parameters
    ----------
    decimals : int
        The number of decimals to which summary statistics should be the preserved.
    in_notebook : bool
        Whether this is running in a notebook.
    output_dir : str or pathlib.Path, optional
        The directory to write output files (CSV, PNG, GIF).
    write_images : bool, default ``True``
        Whether to write image files to :attr:`output_dir`.
        This must be ``True`` for animation.
    write_data : bool, default ``False``
        Whether to write data files to :attr:`output_dir`.
    seed : int, optional
        Provide an integer seed to the random number generator.
    num_frames : int, default ``100``
        The number of frames to record out of the morphing process.
    keep_frames : bool, default ``False``
        Whether to keep image files written to :attr:`output_dir` after
        stitching the GIF animation.
    forward_only_animation : bool, default ``False``
        Whether to generate the animation in the forward direction only.
        By default, the animation will play forward and then reverse.
    """

    def __init__(
        self,
        *,
        decimals: int,
        in_notebook: bool,
        output_dir: str | Path | None = None,
        write_images: bool = True,
        write_data: bool = False,
        seed: int | None = None,
        num_frames: int = 100,
        keep_frames: bool = False,
        forward_only_animation: bool = False,
    ) -> None:
        self._rng = np.random.default_rng(seed)

        self.forward_only_animation = forward_only_animation
        """bool: Whether to generate the animation in the forward direction only.
        By default, the animation will play forward and then reverse. This has no
        effect unless :attr:`write_images` is ``True``."""

        self.keep_frames = keep_frames
        """bool: Whether to keep image files written to :attr:`output_dir` after
        stitching the GIF animation. This has no effect unless :attr:`write_images`
        is ``True``."""

        self.write_images = write_images
        """bool: Whether to write image files to :attr:`output_dir`."""

        self.write_data = write_data
        """bool: Whether to write data files to :attr:`output_dir`."""

        self.output_dir = output_dir if output_dir is None else Path(output_dir)
        """pathlib.Path: The directory to write output files (CSV, PNG, GIF)."""

        if (self.write_images or self.write_data) and self.output_dir is None:
            raise ValueError(
                'output_dir cannot be None if write_images or write_data is True.'
            )

        if (
            isinstance(decimals, bool)
            or not isinstance(decimals, int)
            or decimals < 0
            or decimals > 5
        ):
            raise ValueError(
                'decimals must be a non-negative integer less than or equal to 5.'
            )
        self.decimals = decimals
        """int: The number of decimals to which summary statistics should be the preserved."""

        if (
            isinstance(num_frames, bool)
            or not isinstance(num_frames, int)
            or num_frames <= 0
            or num_frames > 100
        ):
            raise ValueError(
                'num_frames must be a positive integer less than or equal to 100.'
            )
        self.num_frames = num_frames
        """int: The number of frames to capture. Must be > 0 and <= 100."""

        self._in_notebook = in_notebook

        self._ProgressTracker = partial(DataMorphProgress, not self._in_notebook)

    def _select_frames(
        self, iterations: int, ease_in: bool, ease_out: bool, freeze_for: int
    ) -> list:
        """
        Identify the frames to capture for the animation.

        Parameters
        ----------
        iterations : int
            The number of iterations.
        ease_in : bool
            Whether to more slowly transition in the beginning.
        ease_out : bool
            Whether to slow down the transition at the end.
        freeze_for : int
            The number of frames to freeze at the beginning and end. Must be in the
            interval [0, 50].

        Returns
        -------
        list
            The list of frame numbers to include in the animation.
        """
        if (
            isinstance(iterations, bool)
            or not isinstance(iterations, int)
            or iterations <= 0
        ):
            raise ValueError('iterations must be a positive integer.')

        if (
            isinstance(freeze_for, bool)
            or not isinstance(freeze_for, int)
            or freeze_for < 0
            or freeze_for > 50
        ):
            raise ValueError(
                'freeze_for must be a non-negative integer less than or equal to 50.'
            )

        # freeze initial frame
        frames = [0] * freeze_for

        if ease_in and not ease_out:
            easing_function = ease_in_sine
        elif ease_out and not ease_in:
            easing_function = ease_out_sine
        elif ease_out and ease_in:
            easing_function = ease_in_out_sine
        else:
            easing_function = linear

        # add transition frames
        frames.extend(
            [
                round(easing_function(x) * iterations)
                for x in np.arange(0, 1, 1 / (self.num_frames - freeze_for // 2))
            ]
        )

        # freeze final frame
        frames.extend([iterations] * freeze_for)

        return frames

    def _record_frames(
        self,
        data: pd.DataFrame,
        bounds: BoundingBox,
        base_file_name: str,
        frame_number: str,
    ) -> None:
        """
        Record frame data as a plot and, when :attr:`write_data` is ``True``, as a CSV file.

        Parameters
        ----------
        data : pandas.DataFrame
            The DataFrame of the data for morphing.
        bounds : BoundingBox
            The plotting limits.
        base_file_name : str
            The prefix to the file names for both the PNG and GIF files.
        frame_number : str
            The frame number with padding zeros added already.
        """
        if self.write_images:
            plot(
                data,
                save_to=self.output_dir / f'{base_file_name}-image-{frame_number}.png',
                decimals=self.decimals,
                x_bounds=bounds.x_bounds,
                y_bounds=bounds.y_bounds,
                dpi=150,
            )
        if (
            self.write_data and int(frame_number) > 0
        ):  # don't write data for the initial frame (input data)
            data.to_csv(
                self.output_dir / f'{base_file_name}-data-{frame_number}.csv',
                index=False,
            )

    def _is_close_enough(self, df1: pd.DataFrame, df2: pd.DataFrame) -> bool:
        """
        Check whether the statistics are within the acceptable bounds.

        Parameters
        ----------
        df1 : pandas.DataFrame
            The original DataFrame.
        df2 : pandas.DataFrame
            The DataFrame after the latest perturbation.

        Returns
        -------
        bool
            Whether the values are the same to :attr:`decimals`.
        """
        return np.all(
            np.abs(
                np.subtract(
                    *(
                        np.floor(
                            np.array(get_summary_statistics(data)) * 10**self.decimals
                        )
                        for data in [df1, df2]
                    )
                )
            )
            == 0
        )

    def _perturb(
        self,
        data: pd.DataFrame,
        target_shape: Shape,
        *,
        shake: Number,
        allowed_dist: Number,
        temp: Number,
        bounds: BoundingBox,
    ) -> pd.DataFrame:
        """
        Perform one round of perturbation.

        Parameters
        ----------
        data : pandas.DataFrame
            The data to perturb.
        target_shape : Shape
            The shape to morph the data into.
        shake : numbers.Number
            The standard deviation of random movement applied in each direction,
            sampled from a normal distribution with a mean of zero.
        allowed_dist : numbers.Number
            The farthest apart the perturbed points can be from the target shape.
        temp : numbers.Number
            The temperature for simulated annealing. The higher the temperature
            the more we are willing to accept perturbations that might be worse than
            what we had before. The goal is to avoid local optima.
        bounds : BoundingBox
            The minimum/maximum x/y values.

        Returns
        -------
        pandas.DataFrame
            The input dataset with one point perturbed.
        """
        row = self._rng.integers(0, len(data))
        initial_x, initial_y = data.to_numpy()[row]

        # this is the simulated annealing step, if "do_bad", then we are willing to
        # accept a new state which is worse than the current one
        do_bad = self._rng.random() < temp

        done = False
        while not done:
            jitter_x, jitter_y = self._rng.normal(loc=0, scale=shake, size=2)
            new_x = initial_x + jitter_x
            new_y = initial_y + jitter_y

            old_dist = target_shape.distance(initial_x, initial_y)
            new_dist = target_shape.distance(new_x, new_y)

            close_enough = new_dist < old_dist or new_dist < allowed_dist or do_bad
            within_bounds = [new_x, new_y] in bounds
            done = close_enough and within_bounds

        data.loc[row, 'x'] = new_x
        data.loc[row, 'y'] = new_y

        return data

    def morph(
        self,
        start_shape: Dataset,
        target_shape: Shape,
        *,
        iterations: int = 100_000,
        max_temp: Number = 0.4,
        min_temp: Number = 0,
        min_shake: Number = 0.3,
        max_shake: Number = 1,
        allowed_dist: Number = 2,
        ease_in: bool = False,
        ease_out: bool = False,
        freeze_for: int = 0,
        progress: multiprocessing.DictProxy | None = None,
        task_id: TaskID | None = None,
    ) -> pd.DataFrame:
        """
        Morph a dataset into a target shape by perturbing it
        with simulated annealing.

        Parameters
        ----------
        start_shape : Dataset
            The dataset for the starting shape.
        target_shape : Shape
            The shape we want to morph into.
        iterations : int
            The number of iterations to run simulated annealing for.
        max_temp : numbers.Number
            The maximum temperature for simulated annealing (starting temperature).
        min_temp : numbers.Number
            The minimum temperature for simulated annealing (ending temperature).
        min_shake : numbers.Number
            The standard deviation of random movement applied in each direction,
            sampled from a normal distribution with a mean of zero. Value will start
            at ``max_shake`` and move toward ``min_shake``.
        max_shake : numbers.Number
            The standard deviation of random movement applied in each direction,
            sampled from a normal distribution with a mean of zero. Value will start
            at ``max_shake`` and move toward ``min_shake``.
        allowed_dist : numbers.Number
            The farthest apart the perturbed points can be from the target shape.
        ease_in : bool, default ``False``
            Whether to more slowly transition in the beginning.
            This only affects the frames, not the algorithm.
        ease_out : bool, default ``False``
            Whether to slow down the transition at the end.
            This only affects the frames, not the algorithm.
        freeze_for : int, default ``0``
            The number of frames to freeze at the beginning and end.
            This only affects the frames, not the algorithm. Must be in the
            interval ``[0, 50]``.
        progress : multiprocessing.DictProxy | ``None``, optional
            The state of all task progresses when parallelizing work (for use by the CLI).
        task_id : TaskID | ``None``, optional
            The task ID assigned by the progress tracker (for use by the CLI).

        Returns
        -------
        pandas.DataFrame
            The morphed data.

        See Also
        --------
        :class:`.DataLoader`
            The initial state for the morphing process is a :class:`.Dataset`.
            Available built-in options can be found here.
        :class:`.ShapeFactory`
            The target state for the morphing process is a :class:`.Shape`.
            Options for the target can be found here.

        Notes
        -----
        This method saves data to disk at :attr:`output_dir`, which
        includes frames and/or animation (see :attr:`write_images`
        and :attr:`keep_frames`) and, depending on :attr:`write_data`,
        CSV files for each frame.
        """
        for name, value in [
            ('max_temp', max_temp),
            ('min_temp', min_temp),
            ('min_shake', min_shake),
            ('max_shake', max_shake),
        ]:
            if (
                isinstance(value, bool)
                or not isinstance(value, Number)
                or not 0 <= value <= 1
            ):
                raise ValueError(f'{name} must be a number >= 0 and <= 1.')

        for name, min_value, max_value in [
            ('temp', min_temp, max_temp),
            ('shake', min_shake, max_shake),
        ]:
            if min_value >= max_value:
                raise ValueError(f'max_{name} must be greater than min_{name}.')

        if (
            isinstance(allowed_dist, bool)
            or not isinstance(allowed_dist, Number)
            or allowed_dist < 0
        ):
            raise ValueError('allowed_dist must be a non-negative numeric value.')

        morphed_data = start_shape.data.copy()

        # iteration numbers that we will end up writing to file as frames
        frame_numbers = self._select_frames(
            iterations=iterations,
            ease_in=ease_in,
            ease_out=ease_out,
            freeze_for=freeze_for,
        )

        base_file_name = f'{start_shape.name}-to-{target_shape}'
        record_frames = partial(
            self._record_frames,
            base_file_name=base_file_name,
            bounds=start_shape.plot_bounds,
        )

        frame_number_format = f'{{:0{len(str(iterations))}d}}'.format
        record_frames(data=morphed_data, frame_number=frame_number_format(0))

        def _easing(
            frame: int, *, min_value: Number, max_value: Number
        ) -> Number:  # numpydoc ignore=PR01,RT01
            """Determine the next value with easing."""
            return (max_value - min_value) * ease_in_out_quadratic(
                (iterations - frame) / iterations
            ) + min_value

        get_current_temp = partial(
            _easing,
            min_value=min_temp,
            max_value=max_temp,
        )
        get_current_shake = partial(
            _easing,
            min_value=min_shake,
            max_value=max_shake,
        )

        with (nullcontext if progress else self._ProgressTracker)() as progress_tracker:
            if progress_tracker:
                task_id = progress_tracker.add_task(
                    f'{start_shape.name} to {target_shape}'
                )
            for i in range(1, iterations + 1):
                perturbed_data = self._perturb(
                    morphed_data.copy(),
                    target_shape=target_shape,
                    shake=get_current_shake(i),
                    allowed_dist=allowed_dist,
                    temp=get_current_temp(i),
                    bounds=start_shape.morph_bounds,
                )

                if self._is_close_enough(start_shape.data, perturbed_data):
                    morphed_data = perturbed_data

                if frame_numbers.count(i):
                    record_frames(
                        data=morphed_data, frame_number=frame_number_format(i)
                    )

                if progress_tracker:
                    progress_tracker.update(
                        task_id,
                        total=iterations,
                        completed=i,
                        refresh=self._in_notebook and (i) % 500 == 0,
                    )
                else:
                    progress[task_id] = {'progress': i, 'total': iterations}

        if self.write_images:
            stitch_gif_animation(
                self.output_dir,
                start_shape.name,
                frame_numbers=frame_numbers,
                target_shape=target_shape,
                keep_frames=self.keep_frames,
                forward_only_animation=self.forward_only_animation,
            )

        if self.write_data:
            morphed_data.to_csv(
                self.output_dir
                / f'{base_file_name}-data-{frame_number_format(iterations)}.csv',
                index=False,
            )

        return morphed_data
