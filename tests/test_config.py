"""Verify that the Phase-0 configs folder exists."""

from pathlib import Path


def test_configs_folder_exists() -> None:
    assert Path("configs").is_dir()