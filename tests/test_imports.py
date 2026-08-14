"""Verify that the Phase-0 package exists and is importable."""

from pathlib import Path


def test_package_folder_exists() -> None:
    assert Path("src/adaptive_memory").is_dir()


def test_package_is_importable() -> None:
    import adaptive_memory

    assert hasattr(adaptive_memory, "__version__")