"""Test shape classes."""

import re

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
    for shape_name, shape_type in shape_factory._SHAPE_MAPPING.items():
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
        def distance(self, x, y):
            return super().distance(x, y)

        def plot(self, ax=None):
            return super().plot(ax)

    with pytest.raises(NotImplementedError):
        NewShape().distance(0, 0)

    with pytest.raises(NotImplementedError):
        NewShape().plot()


def test_circle(shape_factory):
    """Test the Circle class."""
    circle = shape_factory.generate_shape('circle')
    assert pytest.approx(circle.distance(20, 50)) == 10.490381


def test_bullseye(shape_factory):
    """Test the Bullseye class."""
    bullseye = shape_factory.generate_shape('bullseye')
    assert pytest.approx(bullseye.distance(20, 50)) == 3.660254


def test_dots(shape_factory):
    """Test the Dots class."""
    dots = shape_factory.generate_shape('dots')
    assert dots.distance(20, 50) == 0.0


@pytest.mark.parametrize(['x', 'y'], [(20, 50), (0, 0)])
def test_scatter(shape_factory, x, y):
    """Test the Scatter class."""
    scatter = shape_factory.generate_shape('scatter')
    assert scatter.distance(x, y) == 0.0


def test_lines(shape_factory):
    """Test the Lines class."""
    x_lines = shape_factory.generate_shape('x')

    # test a point on the line
    assert pytest.approx(x_lines.distance(*x_lines.lines[0][1])) == 0.0

    # test a point off the line
    assert pytest.approx(x_lines.distance(0, 0)) == 83.384650

    # test lines that are very small
    assert x_lines._distance_point_to_line((30, 50), [(0, 0), (0, 0)]) == 9999


def test_point_collection(shape_factory):
    """Test the PointCollection class."""
    parabola = shape_factory.generate_shape('up_parab')

    # test a point on the curve
    assert pytest.approx(parabola.distance(*parabola.points[0])) == 0.0

    # test a point off the curve
    assert pytest.approx(parabola.distance(0, 0)) == 53.774155


@pytest.mark.parametrize(
    ['shape', 'expected'],
    [
        ['new_shape', '<NewShape>'],
        ['dots', '<DotsGrid of 9 points>'],
        [
            'x',
            (
                '<XLines>\n  lines=\n        '
                '[[8.0, 47.0], [32.0, 83.0]]\n        [[8.0, 83.0], [32.0, 47.0]]'
            ),
        ],
        ['circle', r'^<Circle cx=(\d+\.*\d*) cy=(\d+\.*\d*) r=(\d+\.*\d*)>$'],
        [
            'bullseye',
            (
                r'^<Bullseye>\n'
                r'  circles=\n'
                r'          <Circle cx=(\d+\.*\d*) cy=(\d+\.*\d*) r=(\d+\.*\d*)>\n'
                r'          <Circle cx=(\d+\.*\d*) cy=(\d+\.*\d*) r=(\d+\.*\d*)>$'
            ),
        ],
        ['down_parab', '<DownParabola of 100 points>'],
    ],
    ids=['new shape', 'dots', 'x', 'circle', 'bullseye', 'down parabola'],
)
def test_reprs(shape_factory, shape, expected):
    """Test that the __repr__() method is working."""
    if shape != 'new_shape':
        value = repr(shape_factory.generate_shape(shape))
        if shape == 'x':
            assert value == expected
        else:
            assert re.match(expected, value)
    else:

        class NewShape(Shape):
            def distance(self, x, y):  # pragma: no cover
                return x, y

            def plot(self, ax):  # pragma: no cover
                return ax

        new_shape = NewShape()
        assert repr(new_shape) == expected
