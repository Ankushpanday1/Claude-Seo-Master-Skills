"""Make the Agentic-SEO-Skill script pack importable for its tests."""
import sys
from pathlib import Path

_agentic_path = str(Path(__file__).resolve().parents[2] / "scripts" / "agentic")
if _agentic_path not in sys.path:
    sys.path.append(_agentic_path)
