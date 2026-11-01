"""Root conftest ensuring scripts/ is first on sys.path."""
import sys
from pathlib import Path

root_scripts = str(Path(__file__).resolve().parent.parent / "scripts")
if root_scripts not in sys.path:
    sys.path.insert(0, root_scripts)
