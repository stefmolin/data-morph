"""Test the parabola module."""

import pytest

from .bases import ParabolaTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestDownParabola(ParabolaTestBase):
    """Test the DownParabola class."""

    shape_name = 'down_parab'
    distance_test_cases = (((20, 50), 7.929688), ((30, 60), 3.455534))
    positive_quadratic_term = False
    x_index = 0
    y_index = 1


class TestLeftParabola(ParabolaTestBase):
    """Test the LeftParabola class."""

    shape_name = 'left_parab'
    distance_test_cases = (((50, 20), 46.31798), ((10, 77), 0.0))
    positive_quadratic_term = False
    x_index = 1
    y_index = 0


class TestRightParabola(ParabolaTestBase):
    """Test the RightParabola class."""

    shape_name = 'right_parab'
    distance_test_cases = (((50, 20), 38.58756), ((10, 77), 7.740692))
    positive_quadratic_term = True
    x_index = 1
    y_index = 0


class TestUpParabola(ParabolaTestBase):
    """Test the UpParabola class."""

    shape_name = 'up_parab'
    distance_test_cases = (((0, 0), 53.774155), ((30, 60), 5.2576809))
    positive_quadratic_term = True
    x_index = 0
    y_index = 1
