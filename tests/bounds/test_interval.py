"""Test the interval module."""

import pytest

from data_morph.bounds.interval import Interval


@pytest.mark.bounds
class TestInterval:
    """Test the Interval class."""

    def test_init(self):
        """Test that Interval can be initialized."""
        limits, inclusive = [0, 10], True
        bounds = Interval(limits, inclusive)
        assert bounds._bounds == limits
        assert bounds._inclusive == inclusive

    @pytest.mark.input_validation
    @pytest.mark.parametrize(
        'limits',
        [[1, 1], [1.0, 1], [1, -1]],
        ids=['no range', 'no range, float vs. int', 'right <= left bound'],
    )
    def test_invalid(self, limits):
        """Test that Interval requires a valid range."""
        with pytest.raises(ValueError, match='must be strictly greater than'):
            _ = Interval(limits)

    @pytest.mark.parametrize(
        ('limits', 'inclusive', 'value', 'expected'),
        [
            ([0, 10], True, 0, True),
            ([0, 10], True, 10, True),
            ([0, 10], True, 5, True),
            ([0, 10], False, 5, True),
            ([0, 10], False, 0, False),
            ([0, 10], False, 10, False),
        ],
        ids=[
            '0 in [0, 10]',
            '10 in [0, 10]',
            '5 in [0, 10]',
            '5 in (0, 10)',
            '0 not in (0, 10)',
            '10 not in (0, 10)',
        ],
    )
    def test_contains(self, limits, inclusive, value, expected):
        """Test that checking if a value is in the Interval works."""
        bounds = Interval(limits, inclusive)
        assert (value in bounds) == expected

    @pytest.mark.input_validation
    @pytest.mark.parametrize(
        'value',
        [[1, 1], True, (1, -1), {2}, 's', {}, None],
        ids=str,
    )
    def test_contains_invalid(self, value):
        """Test that the __contains__() method requires a numeric value."""
        with pytest.raises(TypeError, match='only supported for numeric values'):
            _ = value in Interval([0, 10])

    @pytest.mark.parametrize(
        ('limits', 'inclusive', 'expected'),
        [
            ([0, 1], True, True),
            ([0, 1], False, False),
            ([-1, 1], True, False),
            ([-1, 1], False, False),
        ],
    )
    def test_eq(self, limits, inclusive, expected):
        """Test that the equality check is working."""
        assert (Interval([0, 1], True) == Interval(limits, inclusive)) == expected

    @pytest.mark.parametrize('other', ['s', [], {}, 7])
    def test_eq_type(self, other):
        """Test that the equality check only works for Interval objects."""
        with pytest.raises(TypeError, match='only defined between Interval objects'):
            _ = Interval([0, 1], True) == other

    def test_getitem(self):
        """Test that the __getitem__() method is working."""
        limits = [0, 1]
        bounds = Interval(limits)
        assert bounds[0] == limits[0]
        assert bounds[1] == limits[1]

    def test_iter(self):
        """Test that the __iter__() method is working."""
        limits = [0, 1]
        for bound, limit in zip(Interval(limits), limits):
            assert bound == limit

    @pytest.mark.parametrize(
        ('inclusive', 'expected'),
        [
            (True, '<Interval inclusive [0, 1]>'),
            (False, '<Interval exclusive (0, 1)>'),
        ],
    )
    def test_repr(self, inclusive, expected):
        """Test that the __repr__() method is working."""
        bounds = Interval([0, 1], inclusive)
        assert repr(bounds) == expected

    @pytest.mark.input_validation
    @pytest.mark.parametrize(
        ('value', 'expected_msg', 'exc_class'),
        [
            (0, 'value must be non-zero', ValueError),
            (None, 'value must be a numeric value', TypeError),
            ('s', 'value must be a numeric value', TypeError),
            (True, 'value must be a numeric value', TypeError),
        ],
    )
    def test_adjust_bounds_input_validation(self, value, expected_msg, exc_class):
        """Test that input validation on the adjust_bounds() method is working."""
        bounds = Interval([10, 90])

        with pytest.raises(exc_class, match=expected_msg):
            bounds.adjust_bounds(value)

    @pytest.mark.parametrize('value', [2, -8])
    def test_adjust_bounds(self, value):
        """Test that the adjust_bounds() method is working."""
        start = [10, 90]
        bounds = Interval(start)
        initial_range = bounds.range

        bounds.adjust_bounds(value)
        assert bounds.range == initial_range + value
        assert bounds[0] == start[0] - value / 2
        assert bounds[1] == start[1] + value / 2

    @pytest.mark.parametrize(
        ('limits', 'inclusive'),
        [
            ([10, 90], True),
            ([10, 90], False),
        ],
        ids=['inclusive', 'exclusive'],
    )
    def test_clone(self, limits, inclusive):
        """Test that the clone() method is working."""
        bounds = Interval(limits, inclusive)
        bounds_clone = bounds.clone()

        # confirm it is a new object
        assert bounds is not bounds_clone

        # confirm equality of values
        assert bounds == bounds_clone

        # confirm deep copy of bounds
        bounds_clone.adjust_bounds(2)
        assert bounds != bounds_clone

    @pytest.mark.parametrize('inclusive', [True, False])
    @pytest.mark.parametrize(
        ('limits', 'expected'),
        [
            ([-10, -5], 5),
            ([-1, 1], 2),
            ([2, 100], 98),
        ],
        ids=str,
    )
    def test_range(self, limits, inclusive, expected):
        """Test that the range property is working."""
        bounds = Interval(limits, inclusive)
        assert bounds.range == expected

    @pytest.mark.parametrize('inclusive', [True, False])
    @pytest.mark.parametrize(
        ('limits', 'expected'),
        [
            ([-10, -5], -7.5),
            ([-1, 1], 0),
            ([2, 100], 51),
        ],
        ids=str,
    )
    def test_center(self, limits, inclusive, expected):
        """Test that the center property is working."""
        bounds = Interval(limits, inclusive)
        assert bounds.center == expected
