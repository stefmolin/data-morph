"""Test the factory module."""

import matplotlib.pyplot as plt
import pytest


@pytest.mark.shapes
class TestShapeFactory:
    """Test the ShapeFactory class."""

    def test_generate_shape(self, shape_factory):
        """Test the generate_shape() method on a valid shape."""
        for shape_name, shape_type in shape_factory._SHAPE_MAPPING.items():
            shape = shape_factory.generate_shape(shape_name)
            assert isinstance(shape, shape_type)
            assert shape_name == str(shape)

    def test_generate_shape_error(self, shape_factory):
        """Test the generate_shape() method on a non-existent shape."""
        with pytest.raises(ValueError, match='No such shape'):
            _ = shape_factory.generate_shape('does not exist')

    @pytest.mark.parametrize('subset', [4, 5, 8, 10, None])
    def test_plot_available_shapes(self, shape_factory, monkeypatch, subset):
        """Test the plot_available_shapes() method."""
        if subset:
            monkeypatch.setattr(
                shape_factory,
                'AVAILABLE_SHAPES',
                shape_factory.AVAILABLE_SHAPES[:subset],
            )

        axs = shape_factory.plot_available_shapes()
        if subset is None or subset > 5:
            assert len(axs) > 1
        else:
            assert len(axs) == axs.size

        populated_axs = [ax for ax in axs.flatten() if ax.get_figure()]
        assert len(populated_axs) == len(shape_factory.AVAILABLE_SHAPES)
        assert all(ax.get_xlabel() == ax.get_ylabel() == '' for ax in populated_axs)
        assert {ax.get_title() for ax in populated_axs} == set(
            shape_factory.AVAILABLE_SHAPES
        )
        plt.close()
