"""Module containing data morphing logic."""

from __future__ import annotations

from collections.abc import MutableSequence
from functools import partial
from numbers import Number
from pathlib import Path

import numpy as np
import pandas as pd
import tqdm

from .bounds.bounding_box import BoundingBox
from .data.dataset import Dataset
from .data.stats import Statistics, SummaryStatistics
from .plotting.animation import (
    ease_in_out_quadratic,
    ease_in_out_sine,
    ease_in_sine,
    ease_out_sine,
    linear,
    stitch_gif_animation,
)
from .plotting.static import plot
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
    num_frames : int, default 100
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

        self._looper = tqdm.tnrange if in_notebook else tqdm.trange

    def _select_frames(
        self, iterations: int, ramp_in: bool, ramp_out: bool, freeze_for: int
    ) -> list:
        """
        Identify the frames to capture for the animation.

        Parameters
        ----------
        iterations : int
            The number of iterations.
        ramp_in : bool
            Whether to more slowly transition in the beginning.
        ramp_out : bool
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

        if ramp_in and not ramp_out:
            easing_function = ease_in_sine
        elif ramp_out and not ramp_in:
            easing_function = ease_out_sine
        elif ramp_out and ramp_in:
            easing_function = ease_in_out_sine
        else:
            easing_function = linear

        # add transition frames
        frames.extend(
            [
                int(round(easing_function(x) * iterations))
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
        count: int,
        frame_number: int,
    ) -> int:
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
        count : int
            The number of frames to record with the data.
        frame_number : int
            The starting frame number.

        Returns
        -------
        int
            The next frame number available for recording.
        """
        if self.write_images or self.write_data:
            is_start = frame_number == 0
            for _ in range(count):
                if self.write_images:
                    plot(
                        data,
                        save_to=(
                            self.output_dir
                            / f'{base_file_name}-image-{frame_number:03d}.png'
                        ),
                        decimals=self.decimals,
                        x_bounds=bounds.x_bounds,
                        y_bounds=bounds.y_bounds,
                        dpi=150,
                    )
                if (
                    self.write_data and not is_start
                ):  # don't write data for the initial frame (input data)
                    data.to_csv(
                        self.output_dir
                        / f'{base_file_name}-data-{frame_number:03d}.csv',
                        index=False,
                    )

                frame_number += 1
        return frame_number

    def _is_close_enough(
        self,
        item1: SummaryStatistics,
        item2: SummaryStatistics,
        /,
    ) -> bool:
        """
        Check whether the statistics are within the acceptable bounds.

        Parameters
        ----------
        item1 : SummaryStatistics
            The first summary statistic.

        item2 : SummaryStatistics
            The second summary statistic.

        Returns
        -------
        bool
            Whether the values are the same to :attr:`decimals`.
        """
        return np.all(
            np.abs(
                np.subtract(
                    np.floor(np.array(item1) * 10**self.decimals),
                    np.floor(np.array(item2) * 10**self.decimals),
                )
            )
            == 0
        )

    def _perturb(
        self,
        x: MutableSequence[Number],
        y: MutableSequence[Number],
        target_shape: Shape,
        *,
        shake: Number,
        allowed_dist: Number,
        temp: Number,
        bounds: BoundingBox,
    ) -> tuple[int, MutableSequence[Number], MutableSequence[Number]]:
        """
        Perform one round of perturbation.

        Parameters
        ----------
        x : MutableSequence[Number]
            The ``x`` part of the dataset.
        y : MutableSequence[Number]
            The ``y`` part of the dataset.
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
        tuple[int, MutableSequence[Number], MutableSequence[Number]]
            The index and input dataset with one point perturbed.
        """
        row = self._rng.integers(0, len(x))
        initial_x = x[row]
        initial_y = y[row]

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

        x[row] = new_x
        y[row] = new_y

        return row, x, y

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
        ramp_in: bool = False,
        ramp_out: bool = False,
        freeze_for: int = 0,
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
        ramp_in : bool, default ``False``
            Whether to more slowly transition in the beginning.
            This only affects the frames, not the algorithm.
        ramp_out : bool, default ``False``
            Whether to slow down the transition at the end.
            This only affects the frames, not the algorithm.
        freeze_for : int, default 0
            The number of frames to freeze at the beginning and end.
            This only affects the frames, not the algorithm. Must be in the
            interval [0, 50].

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

        morphed_data = start_shape.df.copy()

        # iteration numbers that we will end up writing to file as frames
        frame_numbers = self._select_frames(
            iterations=iterations,
            ramp_in=ramp_in,
            ramp_out=ramp_out,
            freeze_for=freeze_for,
        )

        base_file_name = f'{start_shape.name}-to-{target_shape}'
        record_frames = partial(
            self._record_frames,
            base_file_name=base_file_name,
            bounds=start_shape.plot_bounds,
        )
        frame_number = record_frames(
            data=morphed_data,
            count=max(freeze_for, 1),
            frame_number=0,
        )

        def _tweening(
            frame: int, *, min_value: Number, max_value: Number
        ) -> Number:  # numpydoc ignore=PR01,RT01
            """Determine the next value with tweening."""
            return (max_value - min_value) * ease_in_out_quadratic(
                (iterations - frame) / iterations
            ) + min_value

        get_current_temp = partial(
            _tweening,
            min_value=min_temp,
            max_value=max_temp,
        )
        get_current_shake = partial(
            _tweening,
            min_value=min_shake,
            max_value=max_shake,
        )

        x, y = (
            start_shape.df['x'].to_numpy(copy=True),
            start_shape.df['y'].to_numpy(copy=True),
        )

        # the starting dataset statistics
        stats = Statistics(x, y)

        # the summary statistics of the above
        summary_stats = stats.perturb(0, 0, 0)

        for i in self._looper(
            iterations, leave=True, ascii=True, desc=f'{target_shape} pattern'
        ):
            index, *perturbed_data = self._perturb(
                np.copy(x),
                np.copy(y),
                target_shape=target_shape,
                shake=get_current_shake(i),
                allowed_dist=allowed_dist,
                temp=get_current_temp(i),
                bounds=start_shape.morph_bounds,
            )

            new_summary_stats = stats.perturb(
                index,
                perturbed_data[0][index] - x[index],
                perturbed_data[1][index] - y[index],
            )

            if self._is_close_enough(summary_stats, new_summary_stats):
                summary_stats = stats.perturb(
                    index,
                    perturbed_data[0][index] - x[index],
                    perturbed_data[1][index] - y[index],
                    update=True,
                )
                x, y = perturbed_data
                morphed_data = pd.DataFrame({'x': x, 'y': y})

            frame_number = record_frames(
                data=morphed_data,
                count=frame_numbers.count(i),
                frame_number=frame_number,
            )

        if self.write_images:
            stitch_gif_animation(
                self.output_dir,
                start_shape.name,
                target_shape=target_shape,
                keep_frames=self.keep_frames,
                forward_only_animation=self.forward_only_animation,
            )

        if self.write_data:
            morphed_data.to_csv(
                self.output_dir / f'{base_file_name}-data-{frame_number:03d}.csv',
                index=False,
            )

        return morphed_data
