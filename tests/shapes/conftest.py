"""Hooks and config for data_morph.shapes tests."""

import pytest

from data_morph.data.dataset import Dataset
from data_morph.shapes.factory import ShapeFactory


def pytest_generate_tests(metafunc):
    """Parametrize test_distance() methods using distance_test_cases class attribute."""
    if metafunc.function.__name__ == 'test_distance':
        metafunc.parametrize(
            ['test_point', 'expected_distance'],
            metafunc.cls.distance_test_cases,
            ids=str,
        )


@pytest.fixture(scope='session')
def shape_factory(sample_data):
    """Fixture for a ShapeFactory of sample data."""
    return ShapeFactory(Dataset('sample', sample_data))
