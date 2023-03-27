"""Test the __main__ module."""

import subprocess

import pytest

pytestmark = pytest.mark.cli


@pytest.mark.parametrize(['flag', 'return_code'], [['--version', 0], ['', 2]])
def test_main_access_cli(flag, return_code):
    """Confirm that CLI can be accessed via __main__."""
    result = subprocess.run(['python', '-m', 'data_morph', flag])
    assert result.returncode == return_code
