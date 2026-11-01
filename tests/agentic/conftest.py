"""Make the Agentic-SEO-Skill script pack importable for its tests."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "agentic"))
