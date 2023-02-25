"""Test shape classes."""

import pytest

from data_morph.data.dataset import Dataset
from data_morph.shapes.bases.shape import Shape
from data_morph.shapes.factory import ShapeFactory


@pytest.fixture(scope='module')
def shape_factory(sample_data):
    """Fixture for a ShapeFactory of sample data."""
    return ShapeFactory(Dataset('sample', sample_data))


def test_shape_factory(shape_factory):
    """Test the ShapeFactory class."""
    for shape_name, shape_type in shape_factory.AVAILABLE_SHAPES.items():
        shape = shape_factory.generate_shape(shape_name)
        assert isinstance(shape, shape_type)
        assert shape_name == str(shape)

    with pytest.raises(ValueError, match='No such shape'):
        _ = shape_factory.generate_shape('does not exist')


def test_shape_abc():
    """Test that Shape class can't be instantiated directly."""
    with pytest.raises(TypeError):
        _ = Shape()

    class NewShape(Shape):
        def distance(self):
            return super().distance(0, 0)

    with pytest.raises(NotImplementedError):
        NewShape().distance()


def test_circle(shape_factory):
    """Test the Circle class."""
    circle = shape_factory.generate_shape('circle')
    assert circle.distance(20, 50) == 20.0


def test_bullseye(shape_factory):
    """Test the Bullseye class."""
    bullseye = shape_factory.generate_shape('bullseye')
    assert bullseye.distance(20, 50) == 8.0


def test_dots(shape_factory):
    """Test the Dots class."""
    dots = shape_factory.generate_shape('dots')
    assert dots.distance(20, 50) == 0.0


def test_scatter(shape_factory):
    """Test the Scatter class."""
    scatter = shape_factory.generate_shape('scatter')
    assert scatter.distance(20, 50) == 0.0
    assert scatter.distance(20, 8) == 22.0


def test_lines(shape_factory):
    """Test the Lines class."""
    x_lines = shape_factory.generate_shape('x')

    # test a point on the line
    assert x_lines.distance(30, 50) == 0.0

    # test a point off the line
    assert pytest.approx(x_lines.distance(0, 0)) == 80.622577

    # test lines that are very small
    assert x_lines._distance_point_to_line((30, 50), [(0, 0), (0, 0)]) == 9999


@pytest.mark.parametrize(
    ['shape', 'expected'],
    [
        ['new_shape', '<NewShape>'],
        [
            'dots',
            (
                '<Dots>\n  dots=\n       (11.0, 50.0)\n       '
                '(11.0, 50.0)\n       (11.0, 77.0)'
            ),
        ],
        [
            'x',
            (
                '<XLines>\n  lines=\n        '
                '[[10, 50], [30, 80]]\n        [[10, 80], [30, 50]]'
            ),
        ],
        ['circle', '<Circle cx=20.0 cy=60.0 r=30>'],
        [
            'bullseye',
            (
                '<Bullseye>\n  circles=\n          '
                '<Circle cx=20.0 cy=60.0 r=18>\n          '
                '<Circle cx=20.0 cy=60.0 r=37>'
            ),
        ],
    ],
)
def test_reprs(shape_factory, shape, expected):
    """Test that the __repr__() method is working."""
    if shape != 'new_shape':
        value = repr(shape_factory.generate_shape(shape))
        if shape == 'dots':
            assert value.startswith(expected)
        else:
            assert value == expected
    else:

        class NewShape(Shape):
            def distance(self, x, y):
                return x, y

        new_shape = NewShape()
        assert repr(new_shape) == expected
