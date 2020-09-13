#!/usr/bin/env python

"""Tests for `mortgage_simulator` package."""

import pytest


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_command_line_interface():
    """Test the CLI."""
    return True
    # runner = CliRunner()
    # result = runner.invoke(cli.main)
    # assert result.exit_code == 0
    # assert "mortgage_simulator.cli.main" in result.output
    # help_result = runner.invoke(cli.main, ["--help"])
    # assert help_result.exit_code == 0
    # assert "--help  Show this message and exit." in help_result.output
