"""Make the geo-seo-claude script pack importable for its tests."""
import sys
from pathlib import Path

_geo_path = str(Path(__file__).resolve().parents[2] / "scripts" / "geo")
if _geo_path not in sys.path:
    sys.path.append(_geo_path)
