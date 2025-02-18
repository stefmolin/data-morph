"""Test the static module."""

import filecmp

import matplotlib.pyplot as plt
import pytest

from data_morph.plotting.style import plot_with_custom_style, style_context

pytestmark = pytest.mark.plotting


def save_plot(filepath):
    """Save a generic plot to a filepath for testing."""
    fig, ax = plt.subplots()
    ax.plot([0, 1])
    fig.savefig(filepath)
    plt.close()


@pytest.mark.parametrize('as_decorator', [False, True])
def test_style_context_manager(tmp_path, as_decorator):
    """Test that style_context() can be used as a context manager."""
    no_style = tmp_path / 'original.png'
    styled = tmp_path / 'styled.png'

    save_plot(no_style)

    if as_decorator:

        @style_context()
        def style_plot():
            """Generate a generic plot using the style context manager."""
            return save_plot(styled)

        style_plot()
    else:
        with style_context():
            save_plot(styled)

    assert not filecmp.cmp(no_style, styled, shallow=False)


def test_plot_with_custom_style(tmp_path):
    """Test that the plot_with_custom_style decorator is working."""
    no_style = tmp_path / 'original.png'
    styled = tmp_path / 'styled.png'

    save_plot(no_style)

    @plot_with_custom_style
    def style_plot():
        """Generate a generic plot using the style context manager and wraps."""
        return save_plot(styled)

    style_plot()

    assert plot_with_custom_style.__doc__ != style_plot.__doc__
    assert not filecmp.cmp(no_style, styled, shallow=False)
