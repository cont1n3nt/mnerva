"""Verify that the Phase-0 package folder exists."""

from pathlib import Path


def test_package_folder_exists() -> None:
    assert Path("src/adaptive_memory").is_dir()