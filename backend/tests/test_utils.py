import os
import tempfile


def temp_dir_relpath(temp_dir: tempfile.TemporaryDirectory) -> str:
    """Return a stable relative path for a TemporaryDirectory."""
    return os.path.relpath(temp_dir.name, ".")
