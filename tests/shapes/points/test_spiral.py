"""Test the spiral module."""

import pytest

from .bases import PointsModuleTestBase

pytestmark = [pytest.mark.shapes, pytest.mark.points]


class TestSpiral(PointsModuleTestBase):
    """Test the Spiral class."""

    shape_name = 'spiral'
    distance_test_cases = (
        ((10.862675, 65.846698), 0),
        ((29.280789, 59.546024), 0),
        ((16.022152, 68.248880), 0),
        ((20.310858, 65.251728), 0),
        ((22.803548, 72.599350), 0),
        ((0, 0), 58.03780546896006),
        ((10, 50), 8.239887412781957),
        ((30, 70), 0.6642518196535838),
        ((25, 65), 1.3042797087884075),
        ((-30, 100), 52.14470630148412),
    )
