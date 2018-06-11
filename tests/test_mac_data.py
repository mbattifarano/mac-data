#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `mac_data` package."""
from click.testing import CliRunner
from mac_data import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert ('Command line tool for data collection from web APIs'
            in result.output)
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
