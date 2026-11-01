"""
Tests for Cloudflare managed robots.txt detection in fetch_page.py.

Cloudflare can prepend a managed block to a site's robots.txt that disallows
AI crawlers. The block only exists in the live response, so site owners who
check their own file on the server never see it.
"""

import sys
import importlib.util
from pathlib import Path
from unittest.mock import MagicMock, patch

_geo_fetch_path = Path(__file__).resolve().parents[2] / "scripts" / "geo" / "fetch_page.py"
_spec = importlib.util.spec_from_file_location("geo_fetch_page", _geo_fetch_path)
geo_fetch_page = importlib.util.module_from_spec(_spec)
sys.modules["geo_fetch_page"] = geo_fetch_page
_spec.loader.exec_module(geo_fetch_page)
fetch_robots_txt = geo_fetch_page.fetch_robots_txt


CLOUDFLARE_MANAGED_ROBOTS = """# BEGIN Cloudflare Managed content

User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

# END Cloudflare Managed Content

User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
"""

PLAIN_ROBOTS = """User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
"""


def _fetch_with_robots(text: str, status_code: int = 200) -> dict:
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.text = text
    with patch.object(geo_fetch_page.requests, "get", return_value=mock_resp):
        return fetch_robots_txt("https://example.com/")


class TestCloudflareManagedRobots:
    def test_detects_cloudflare_managed_block(self):
        result = _fetch_with_robots(CLOUDFLARE_MANAGED_ROBOTS)
        assert result["cloudflare_managed"] is True
        assert result["ai_crawler_status"]["GPTBot"] == "BLOCKED"
        assert result["ai_crawler_status"]["ClaudeBot"] == "BLOCKED"

    def test_plain_robots_is_not_flagged(self):
        result = _fetch_with_robots(PLAIN_ROBOTS)
        assert result["cloudflare_managed"] is False

    def test_missing_robots_is_not_flagged(self):
        result = _fetch_with_robots("", status_code=404)
        assert result["cloudflare_managed"] is False
