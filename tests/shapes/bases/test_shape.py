"""Test the shape module."""

import pytest

from data_morph.shapes.bases.shape import Shape


@pytest.mark.shapes
class TestShapeABC:
    """Test the Shape abstract base class (ABC)."""

    def test_is_abc(self):
        """Test that Shape class can't be instantiated directly."""
        with pytest.raises(TypeError):
            _ = Shape()

        class NewShape(Shape):
            """A test shape."""

            def distance(self, x, y):
                """Calculate the distance from the shape to the point."""
                return super().distance(x, y)

            def plot(self, ax=None):
                """Plot the shape."""
                return super().plot(ax)

        with pytest.raises(NotImplementedError):
            NewShape().distance(0, 0)

        with pytest.raises(NotImplementedError):
            NewShape().plot()

    def test_repr(self):
        """Test that the __repr__() method is working."""

        class NewShape(Shape):
            """A test shape."""

            def distance(self, x, y):  # pragma: no cover
                """Calculate the distance from the shape to the point."""
                return x, y

            def plot(self, ax):  # pragma: no cover
                """Plot the shape."""
                return ax

        new_shape = NewShape()
        assert repr(new_shape) == '<NewShape>'
