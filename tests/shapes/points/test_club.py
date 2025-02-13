"""Test the club module."""

import pytest

from .bases import PointsModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestClub(PointsModuleTestBase):
    """Test the Club class."""

    shape_name = 'club'
    distance_test_cases = (
        ((19.639387, 73.783711), 0.0),  # top lobe
        ((12.730310, 60.295844), 0.0),  # bottom left lobe
        ((27.630301, 60.920443), 0.0),  # bottom right lobe
        ((20.304761, 55.933333), 0.0),  # top of stem
        ((18.8, 57.076666), 0.0),  # left part of stem
        ((20.933333, 57.823333), 0.0),  # right part of stem
        ((0, 0), 58.717591),
        ((20, 50), 5.941155),
        ((10, 80), 10.288055),
    )
