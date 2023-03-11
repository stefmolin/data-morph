"""
Morph an input dataset of 2D points into select shapes, while preserving the summary
statistics to a given number of decimal points through simulated annealing.

.. note::
    This code has been altered by Stefanie Molin to work for other input datasets
    by parameterizing the target shapes with information from the input shape.
    The original code works for a specific dataset called the "dinosaurus" and was created
    for the paper "Same Stats, Different Graphs: Generating Datasets with Varied Appearance and
    Identical Statistics through Simulated Annealing" by Justin Matejka and George Fitzmaurice
    (ACM CHI 2017).

    The paper, video, and associated code and datasets can be found on the
    Autodesk Research website `here <https://www.autodeskresearch.com/publications/samestats>`_.
"""

from functools import partial
from numbers import Number
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd
import pytweening
import tqdm

from .bounds.bounding_box import BoundingBox
from .data.dataset import Dataset
from .data.stats import get_values
from .plotting.animation import stitch_gif_animation
from .plotting.static import plot
from .shapes.bases.shape import Shape


class DataMorpher:
    """
    Class for morphing a dataset into a target shape, preserving summary statistics.

    Parameters
    ----------
    decimals : int
        The number of decimals to which summary statistics should be the same.
    in_notebook : bool
        Whether this is running in a notebook.
    output_dir : str or Path, optional
        The directory to write output files (CSV, PNG, GIF).
    write_images : bool, default True
        Whether to write image files to ``output_dir``.
    write_data : bool, default False
        Whether to write data files to ``output_dir``.
    seed : int, optional
        Provide an integer seed to the random number generator.
    num_frames : int, default 100
        The number of frames to record out of the morphing process.
    keep_frames : bool, default False
        Whether to keep image files written to ``output_dir`` after
        stitching GIF animation.
    forward_only_animation : bool, default False
        Whether to generate the animation in the forward direction only.
        By default, the animation will play forward and then reverse.
    """

    def __init__(
        self,
        *,
        decimals: int,
        in_notebook: bool,
        output_dir: Optional[Union[str, Path]] = None,
        write_images: bool = True,
        write_data: bool = False,
        seed: Optional[int] = None,
        num_frames: int = 100,
        keep_frames: bool = False,
        forward_only_animation: bool = False,
    ) -> None:
        self.keep_frames = keep_frames
        self.write_images = write_images
        self.write_data = write_data
        self.output_dir = output_dir if output_dir is None else Path(output_dir)

        if (self.write_images or self.write_data) and self.output_dir is None:
            raise ValueError(
                'output_dir cannot be None if write_images or write_data is True.'
            )

        self.seed = seed
        self.forward_only_animation = forward_only_animation

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

        self.looper = tqdm.tnrange if in_notebook else tqdm.trange

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
            easing_function = pytweening.easeInSine
        elif ramp_out and not ramp_in:
            easing_function = pytweening.easeOutSine
        elif ramp_out and ramp_in:
            easing_function = pytweening.easeInOutSine
        else:
            easing_function = pytweening.linear

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

    def _is_close_enough(self, df1: pd.DataFrame, df2: pd.DataFrame) -> bool:
        """
        Check whether the statistics are within the acceptable bounds.

        Parameters
        ----------
        df1 : pd.DataFrame
            The original DataFrame.
        df2 : pd.DataFrame
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
                        np.floor(np.array(get_values(data)) * 10**self.decimals)
                        for data in [df1, df2]
                    )
                )
            )
            == 0
        )

    @staticmethod
    def _perturb(
        df: pd.DataFrame,
        target_shape: Shape,
        *,
        shake: float,
        allowed_dist: Number,
        temp: Number,
        bounds: BoundingBox,
    ) -> pd.DataFrame:
        """
        Perform one round of perturbation.

        Parameters
        ----------
        df : pandas.DataFrame
            The data to perturb.
        target_shape : Shape
            The shape to morph the data into.
        shake : float
            The standard deviation of random movement applied in each direction,
            sampled from a normal distribution with a mean of zero.
        allowed_dist : Number
            The farthest apart the perturbed points can be from the target shape.
        temp : Number
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
        row = np.random.randint(0, len(df))
        initial_x = df.at[row, 'x']
        initial_y = df.at[row, 'y']

        # this is the simulated annealing step, if "do_bad", then we are willing to
        # accept a new state which is worse than the current one
        do_bad = np.random.random_sample() < temp

        done = False
        while not done:
            new_x = initial_x + np.random.randn() * shake
            new_y = initial_y + np.random.randn() * shake

            old_dist = target_shape.distance(initial_x, initial_y)
            new_dist = target_shape.distance(new_x, new_y)

            close_enough = new_dist < old_dist or new_dist < allowed_dist or do_bad
            within_bounds = [new_x, new_y] in bounds
            done = close_enough and within_bounds

        df.loc[row, 'x'] = new_x
        df.loc[row, 'y'] = new_y

        return df

    def morph(
        self,
        start_shape: Dataset,
        target_shape: Shape,
        *,
        iterations: int = 100_000,
        max_temp: Number = 0.4,
        min_temp: Number = 0,
        shake: float = 0.3,
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
        max_temp : Number
            The maximum temperature for simulated annealing (starting temperature).
        min_temp : Number
            The minimum temperature for simulated annealing (ending temperature).
        shake : float
            The standard deviation of random movement applied in each direction,
            sampled from a normal distribution with a mean of zero.
        allowed_dist : Number
            The farthest apart the perturbed points can be from the target shape.
        ramp_in : bool, default False
            Whether to more slowly transition in the beginning.
            This only affects the frames, not the algorithm.
        ramp_out : bool, default False
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

        Notes
        -----
        This method saves data to disk to :attr:`output_dir`, which
        includes frames and/or animation and, depending on :attr:`write_data`,
        CSV files for each frame.
        """
        # TODO: input validation and tests
        # max_temp: Number = 0.4, (require > 0 and greater than min_temp)
        # min_temp: Number = 0, (require >= 0 and less than max_temp)
        # shake: float = 0.3, (require shake > 0)
        # allowed_dist: Number = 2, (require > 0)

        if isinstance(max_temp, bool) or not isinstance(max_temp, Number):
            raise ValueError('max_temp must be a number >= 0.')

        if isinstance(min_temp, bool) or not isinstance(min_temp, Number):
            raise ValueError('min_temp must be a number >= 0.')

        if min_temp >= max_temp:
            raise ValueError('max_temp must be greater than min_temp.')

        if (
            isinstance(shake, bool)
            or not isinstance(shake, Number)
            or not 0 <= shake <= 1
        ):
            raise ValueError('shake must be a number >= 0 and <= 1.')

        if (
            isinstance(allowed_dist, bool)
            or not isinstance(allowed_dist, int)
            or allowed_dist < 0
        ):
            raise ValueError('allowed_dist must be a non-negative integer.')

        morphed_data = start_shape.df.copy()

        if self.seed is not None:
            np.random.seed(self.seed)

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
            count=freeze_for,
            frame_number=0,
        )

        for i in self.looper(
            iterations, leave=True, ascii=True, desc=f'{target_shape} pattern'
        ):
            current_temp = (max_temp - min_temp) * pytweening.easeInOutQuad(
                (iterations - i) / iterations
            ) + min_temp

            perturbed_data = self._perturb(
                morphed_data.copy(),
                target_shape=target_shape,
                shake=shake,
                allowed_dist=allowed_dist,
                temp=current_temp,
                bounds=start_shape.morph_bounds,
            )

            if self._is_close_enough(start_shape.df, perturbed_data):
                morphed_data = perturbed_data

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
