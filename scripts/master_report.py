#!/usr/bin/env python3
"""Turn an SEO audit findings file into a PDF report and copy-paste fix prompts.

Input is the findings JSON that /seo audit writes (see
skills/seo-report/references/findings-schema.md). Output, in --output-dir:

  SEO-Report.pdf           the client-facing report
  FIX-PROMPTS.md           every fix prompt for every tool in one file
  fix-prompts/<tool>.md    one file per tool: claude-code, cursor, antigravity, lovable

Numbers use US formatting (1,234,567 and 12.5K / 3.2M).

Usage:
  master_report.py --data audit/seo-findings.json --output-dir audit/
  master_report.py --demo --output-dir demo-report/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

SKILL_NAME = "Claude SEO Master Skills"
SEVERITIES = ("critical", "high", "medium", "low")
SEVERITY_LABEL = {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}
SEVERITY_HEX = {"critical": "#C62828", "high": "#E8710A", "medium": "#C99A06", "low": "#5F6B7A"}
INK = "#1F2933"
MUTED = "#5F6B7A"
ACCENT = "#0F766E"
RULE = "#D5DBE1"
PANEL = "#F3F5F7"

TOOLS = {
    "claude-code": "Claude Code",
    "cursor": "Cursor",
    "antigravity": "Google Antigravity",
    "lovable": "Lovable",
}
# Lovable works best with short, plain-language requests, so its prompts are
# split into smaller batches than the code-first tools.
BATCH_SIZE = {"claude-code": 12, "cursor": 10, "antigravity": 12, "lovable": 4}


# ---------------------------------------------------------------- formatting

def fmt_number(value) -> str:
    """US thousands separators: 1234567 -> 1,234,567; floats keep one decimal."""
    if isinstance(value, bool) or value is None:
        return str(value)
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:,.0f}" if value.is_integer() else f"{value:,.1f}"
    return str(value)


def fmt_compact(value) -> str:
    """US short form for metric cards: 12,500 -> 12.5K, 3,200,000 -> 3.2M."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return str(value)
    n = float(value)
    if abs(n) < 10_000:
        return fmt_number(value)
    for limit, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(n) >= limit:
            text = f"{n / limit:.1f}".rstrip("0").rstrip(".")
            return f"{text}{suffix}"
    return fmt_number(value)


def score_grade(score: float) -> str:
    for floor, grade in ((90, "A"), (80, "B"), (70, "C"), (55, "D")):
        if score >= floor:
            return grade
    return "F"


def score_hex(score: float) -> str:
    if score >= 80:
        return "#2E7D32"
    if score >= 55:
        return "#C99A06"
    return "#C62828"


def humanize_key(key: str) -> str:
    text = re.sub(r"[_-]+", " ", key).strip().capitalize()
    fixed = {"urls": "URLs", "ms": "(ms)", "kb": "(KB)", "mb": "(MB)", "28d": "(28d)", "7d": "(7d)", "90d": "(90d)"}
    acronyms = r"\b(cms|cdn|seo|cwv|lcp|inp|cls|ttfb|api|html|url|urls|ms|kb|mb|28d|7d|90d)\b"
    return re.sub(acronyms, lambda m: fixed.get(m.group(1).lower(), m.group(1).upper()), text, flags=re.IGNORECASE)


# ---------------------------------------------------------------- data

def load_data(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return normalize(data)


def normalize(data: dict) -> dict:
    data.setdefault("site", data.get("url", ""))
    data.setdefault("domain", re.sub(r"^https?://", "", data["site"]).split("/")[0] or "site")
    data.setdefault("date", date.today().strftime("%B %d, %Y"))
    data.setdefault("categories", [])
    data.setdefault("metrics", {})
    data.setdefault("stack", {})
    # Info-level notes are not actionable, so they stay out of the plan and prompts.
    findings = [f for f in data.get("findings", []) if str(f.get("severity", "")).lower() != "info"]
    data["findings"] = findings
    for i, f in enumerate(findings, 1):
        sev = str(f.get("severity", "medium")).lower()
        f["severity"] = sev if sev in SEVERITIES else "medium"
        f.setdefault("id", f"F-{i:03d}")
        f.setdefault("category", "General")
        f.setdefault("title", "Untitled finding")
        for key in ("detail", "evidence", "fix", "code", "verify", "effort", "impact", "confidence"):
            f.setdefault(key, "")
        f.setdefault("pages", [])
        f.setdefault("files_hint", [])
    order = {s: n for n, s in enumerate(SEVERITIES)}
    findings.sort(key=lambda f: (order[f["severity"]], f["category"], f["id"]))
    if "overall_score" not in data:
        cats = [c for c in data["categories"] if isinstance(c.get("score"), (int, float))]
        if cats:
            total_w = sum(c.get("weight", 1) for c in cats)
            data["overall_score"] = round(sum(c["score"] * c.get("weight", 1) for c in cats) / total_w)
        else:
            data["overall_score"] = 0
    return data


def severity_counts(findings: list[dict]) -> dict:
    counts = {s: 0 for s in SEVERITIES}
    for f in findings:
        counts[f["severity"]] += 1
    return counts


def quick_wins(data: dict) -> list[dict]:
    ids = set(data.get("quick_wins") or [])
    if ids:
        return [f for f in data["findings"] if f["id"] in ids]
    return [f for f in data["findings"]
            if f["severity"] in ("critical", "high") and str(f["effort"]).lower() == "low"][:8]


# ---------------------------------------------------------------- explained report model

PHASES = {
    1: ("Phase 1: Remove risk", "week 1"),
    2: ("Phase 2: Earn rankings", "weeks 2 to 3"),
    3: ("Phase 3: Authority and coverage", "month 2"),
    4: ("Phase 4: Hygiene and monitoring", "ongoing"),
}


def phase_of(f: dict) -> int:
    if str(f.get("phase", "")).isdigit() and int(f["phase"]) in PHASES:
        return int(f["phase"])
    effort = str(f.get("effort", "")).lower()
    if f["severity"] == "critical" or (f["severity"] == "high" and effort != "high"):
        return 1
    if f["severity"] in ("high", "medium") and effort != "high":
        return 2
    if f["severity"] == "low" and effort == "low":
        return 4
    return 3


def weighted_rows(data: dict) -> list[tuple[str, str, int, str]]:
    """(category, weight %, score, weighted points) plus a total row."""
    rows, total = [], 0.0
    cats = [c for c in data["categories"] if isinstance(c.get("score"), (int, float))]
    weight_sum = sum(c.get("weight", 0) for c in cats) or 1
    for c in cats:
        w = c.get("weight", 0) / weight_sum
        pts = c["score"] * w
        total += pts
        rows.append((c["name"], f"{round(w * 100)}%", round(c["score"]), f"{pts:.1f}"))
    return rows


def first_sentence(text: str) -> str:
    m = re.match(r"(.+?[.!?])(\s|$)", text or "")
    return m.group(1) if m else (text or "")


def top_issues(data: dict) -> list[tuple[str, str]]:
    if data.get("top_issues"):
        return [(t.get("title", ""), t.get("why", "")) if isinstance(t, dict) else (t, "")
                for t in data["top_issues"]][:5]
    picks = [f for f in data["findings"] if f["severity"] in ("critical", "high")][:5]
    return [(f["title"], first_sentence(f["detail"]) or first_sentence(f["impact"])) for f in picks]


def wins_explained(data: dict) -> list[tuple[str, str]]:
    return [(f["title"], first_sentence(f["fix"])) for f in quick_wins(data)][:5]


def plan_rows(data: dict) -> dict[int, list[dict]]:
    plan = {p: [] for p in PHASES}
    for f in data["findings"]:
        plan[phase_of(f)].append(f)
    return plan


def _md_cell(text) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ")


def write_markdown(data: dict, out: Path) -> list[Path]:
    """FULL-AUDIT-REPORT.md and ACTION-PLAN.md, explained in plain language."""
    f_all = data["findings"]
    counts = severity_counts(f_all)
    L = [f"# SEO Audit: {data['domain']}", "",
         " | ".join(x for x in (f"Audit date: {data['date']}",
                                f"Business type: {data.get('business_type', 'Not detected')}",
                                f"Method: {data['method']}" if data.get("method") else "") if x), "",
         f"## SEO Health Score: {data['overall_score']} / 100", ""]
    rows = weighted_rows(data)
    if rows:
        L += ["| Category | Weight | Score | Weighted |", "|---|---|---|---|"]
        L += [f"| {n} | {w} | {s} | {p} |" for n, w, s, p in rows]
        L += [f"| **Total** | | | **{data['overall_score']}** |", ""]
    if data.get("supplementary_scores"):
        L += ["Supplementary scores (not in the weighted total): "
              + ", ".join(f"{k} {v}" for k, v in data["supplementary_scores"].items()) + ".", ""]
    L += ["## Executive Summary", ""]
    if data.get("executive_summary"):
        L += [data["executive_summary"], ""]
    if data.get("root_cause"):
        L += [f"The score is held down by one root problem: **{data['root_cause']}**", ""]
    L += [f"Findings: {counts['critical']} critical, {counts['high']} high, {counts['medium']} medium, "
          f"{counts['low']} low.", "", "### Top 5 critical issues"]
    L += [f"{i}. **{t}.** {w}".rstrip() for i, (t, w) in enumerate(top_issues(data), 1)]
    L += ["", "### Top 5 quick wins"]
    L += [f"{i}. **{t}.** {w}".rstrip() for i, (t, w) in enumerate(wins_explained(data), 1)]
    if data["metrics"]:
        L += ["", "### Key metrics", "", "| Metric | Value |", "|---|---|"]
        L += [f"| {humanize_key(k)} | {fmt_number(v)} |" for k, v in data["metrics"].items()]
    for cat in data["categories"]:
        items = [f for f in f_all if f["category"] == cat["name"]]
        L += ["", f"## {cat['name']} ({round(cat.get('score', 0))})", ""]
        if cat.get("works"):
            L += ["**Works:** " + ", ".join(cat["works"]) + ".", ""]
        if cat.get("notes") or cat.get("summary"):
            L += [cat.get("notes") or cat.get("summary"), ""]
        if items:
            L += ["| Finding | Severity | Fix |", "|---|---|---|"]
            L += [f"| {_md_cell(f['title'])} ({f['id']}) | {SEVERITY_LABEL[f['severity']]} | "
                  f"{_md_cell(first_sentence(f['fix']))} |" for f in items]
    if data.get("limitations"):
        L += ["", "## Limitations", ""] + [f"- {x}" for x in data["limitations"]]
    L += ["", "Evidence, code and checks for every finding: `SEO-Report.pdf`. Fix prompts: `FIX-PROMPTS.md`."]
    full = out / "FULL-AUDIT-REPORT.md"
    full.write_text("\n".join(L) + "\n", encoding="utf-8")

    A = [f"# Action Plan: {data['domain']}", "",
         f"SEO Health Score: {data['overall_score']}/100 ({data['date']}).", ""]
    if data.get("plan_context"):
        A += ["## What this means", ""] + [f"- {x}" for x in data["plan_context"]] + [""]
    A += ["Each action lists what it unblocks or depends on, how you would know it failed, and a leading "
          "indicator to watch.", ""]
    n = 0
    for p, items in plan_rows(data).items():
        if not items:
            continue
        name, when = PHASES[p]
        A += [f"## {name} ({when})", "",
              "| # | Action | Unblocks / depends on | Failure check | Leading indicator |", "|---|---|---|---|---|"]
        for f in items:
            n += 1
            link = f.get("unblocks") or (f"Depends on {f['depends_on']}" if f.get("depends_on") else f["impact"])
            A.append(f"| {n} | **{_md_cell(f['title'])}** ({f['id']}). {_md_cell(f['fix'])} | {_md_cell(link)} | "
                     f"{_md_cell(f.get('failure_check') or f['verify'])} | {_md_cell(f.get('leading_indicator') or '-')} |")
        A.append("")
    targets = [c for c in data["categories"] if c.get("target") is not None]
    if targets:
        A += ["## Expected score movement", "", "| Category | Now | After Phases 1 and 2 (target) |", "|---|---|---|"]
        A += [f"| {c['name']} | {round(c['score'])} | {c['target']} |" for c in targets]
        A += [f"| **Health Score** | **{data['overall_score']}** | **about {expected_total(data)}** |", "",
              "These targets are estimates and depend on the fixes being completed."]
    plan = out / "ACTION-PLAN.md"
    plan.write_text("\n".join(A) + "\n", encoding="utf-8")
    return [full, plan]


def expected_total(data: dict) -> int:
    cats = [c for c in data["categories"] if isinstance(c.get("score"), (int, float))]
    weight_sum = sum(c.get("weight", 0) for c in cats) or 1
    return round(sum(c.get("target", c["score"]) * c.get("weight", 0) for c in cats) / weight_sum)


# ---------------------------------------------------------------- fix prompts

def _stack_line(data: dict) -> str:
    stack = data.get("stack") or {}
    parts = [f"{humanize_key(k)}: {v}" for k, v in stack.items() if v]
    return "; ".join(parts) if parts else "Unknown. Detect it from the project files first."


def _finding_block_code(f: dict, n: int) -> str:
    lines = [f"### {n}. [{SEVERITY_LABEL[f['severity']]}] {f['title']} ({f['id']})"]
    if f["detail"]:
        lines.append(f"Problem: {f['detail']}")
    if f["evidence"]:
        lines.append(f"Evidence from the live site: {f['evidence']}")
    if f["pages"]:
        lines.append("Affected URLs: " + ", ".join(f["pages"][:10])
                     + (f" (and {fmt_number(len(f['pages']) - 10)} more)" if len(f["pages"]) > 10 else ""))
    if f["files_hint"]:
        lines.append("Likely files: " + ", ".join(f"`{p}`" for p in f["files_hint"]))
    if f["fix"]:
        lines.append(f"Required change: {f['fix']}")
    if f["code"]:
        lines.append("Reference implementation (adapt to the project's conventions):")
        lines.append("```\n" + f["code"].strip("\n") + "\n```")
    if f["verify"]:
        lines.append(f"Done when: {f['verify']}")
    return "\n".join(lines)


def _finding_block_lovable(f: dict, n: int) -> str:
    where = ", ".join(f["pages"][:5]) if f["pages"] else "the whole site"
    lines = [f"{n}. {f['title']}", f"   Where: {where}", f"   Change: {f['fix'] or f['detail']}"]
    if f["code"]:
        lines.append("   Use exactly this markup where it applies:")
        lines.append("```\n" + f["code"].strip("\n") + "\n```")
    if f["verify"]:
        lines.append(f"   Check: {f['verify']}")
    return "\n".join(lines)


def _intro(tool: str, data: dict, part: int, parts: int, sev_label: str) -> str:
    site = data["site"]
    if tool == "lovable":
        return (f"I ran an SEO audit on my site {site}. Please make these {sev_label} SEO fixes "
                f"(part {part} of {parts}). Do not change the design, layout or copy beyond what each item "
                "asks. After the changes, tell me which pages you edited.")
    agent = TOOLS[tool]
    mode = {
        "claude-code": "Work in this repository. Read the relevant files before editing.",
        "cursor": "Use Agent mode in this workspace. Open each file you change and keep diffs minimal.",
        "antigravity": "Plan the work as a task list in the Agent Manager, then execute it in this workspace.",
    }[tool]
    return (f"You are fixing SEO issues found by an audit of {site} (part {part} of {parts}, {sev_label}).\n"
            f"Tech stack: {_stack_line(data)}\n{mode}\n\n"
            "Rules:\n"
            "- Fix only the items below. Do not refactor unrelated code or change visible design.\n"
            "- Server-render every SEO tag (title, meta, canonical, JSON-LD) so it is in the HTML without JavaScript.\n"
            "- Keep structured data truthful: JSON-LD must match what is visible on the page.\n"
            "- If an item does not apply to this codebase, say so instead of guessing.\n"
            f"- Using {agent}: when done, list every file changed and how you verified each item.")


def _outro(tool: str, data: dict) -> str:
    site = data["site"]
    if tool == "lovable":
        return "When you are done, publish a preview and list the pages you changed."
    return ("Verification after all items:\n"
            f"1. Build the project and fix any build or type errors.\n"
            f"2. Fetch the built pages without JavaScript (for example `curl -sL {site}`) and confirm each new tag is in the raw HTML.\n"
            "3. Validate any JSON-LD at https://validator.schema.org and https://search.google.com/test/rich-results.\n"
            "4. Re-run `/seo audit` (Claude SEO Master Skills) and confirm these finding IDs no longer appear.")


def build_prompts(data: dict, tool: str) -> list[str]:
    groups = [("critical and high priority", [f for f in data["findings"] if f["severity"] in ("critical", "high")]),
              ("medium priority", [f for f in data["findings"] if f["severity"] == "medium"]),
              ("low priority", [f for f in data["findings"] if f["severity"] == "low"])]
    size = BATCH_SIZE[tool]
    batches = []
    for label, items in groups:
        for start in range(0, len(items), size):
            batches.append((label, items[start:start + size]))
    prompts = []
    for part, (label, items) in enumerate(batches, 1):
        render = _finding_block_lovable if tool == "lovable" else _finding_block_code
        body = "\n\n".join(render(f, n) for n, f in enumerate(items, 1))
        prompts.append(f"{_intro(tool, data, part, len(batches), label)}\n\n{body}\n\n{_outro(tool, data)}")
    return prompts


def write_prompts(data: dict, out: Path) -> list[Path]:
    folder = out / "fix-prompts"
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    combined = [f"# SEO fix prompts for {data['site']}",
                f"Generated by {SKILL_NAME} on {data['date']}. "
                f"{fmt_number(len(data['findings']))} findings. Paste the prompts for your tool in order, "
                "one at a time, and check the result before the next one.\n"]
    for tool, name in TOOLS.items():
        prompts = build_prompts(data, tool)
        how = {
            "claude-code": "Open a terminal in your project folder, run `claude`, and paste each prompt.",
            "cursor": "Open the project in Cursor, start a new Agent chat (Ctrl/Cmd+I), and paste each prompt.",
            "antigravity": "Open the project in Antigravity, start a new agent task in the Agent Manager, and paste each prompt.",
            "lovable": "Open your project in Lovable and paste each prompt into the chat, one at a time.",
        }[tool]
        lines = [f"# {name}: SEO fix prompts", f"Site: {data['site']}  |  {how}\n"]
        for i, p in enumerate(prompts, 1):
            lines.append(f"## Prompt {i} of {len(prompts)}\n\n````text\n{p}\n````\n")
        text = "\n".join(lines)
        path = folder / f"{tool}.md"
        path.write_text(text, encoding="utf-8")
        written.append(path)
        combined += [text, "\n---\n"]
    all_path = out / "FIX-PROMPTS.md"
    all_path.write_text("\n".join(combined), encoding="utf-8")
    return [all_path, *written]


# ---------------------------------------------------------------- PDF

def build_pdf(data: dict, path: Path) -> None:
    try:
        from reportlab.graphics.shapes import Circle, Drawing, Rect, String, Wedge
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas as pdfcanvas
        from reportlab.platypus import (
            KeepTogether,
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
            XPreformatted,
        )
    except ImportError:
        sys.exit("reportlab is required for the PDF. Run `/seo setup`, or `pip install reportlab`.")

    c = colors.HexColor
    W, H = A4
    margin = 18 * mm
    body_w = W - 2 * margin

    styles = {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26, leading=31, textColor=c(INK)),
        "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=13, leading=18, textColor=c(MUTED)),
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17, leading=22, textColor=c(INK),
                             spaceBefore=4, spaceAfter=8),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=c(INK),
                             spaceBefore=10, spaceAfter=4),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=c(INK)),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=c(MUTED)),
        "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8.5, leading=11.5, textColor=c(MUTED)),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.8, leading=11.5, textColor=c(INK)),
        "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=8.8, leading=11.5, textColor=c(INK)),
        "code": ParagraphStyle("code", fontName="Courier", fontSize=7.6, leading=9.6, textColor=c(INK),
                               backColor=c(PANEL), borderPadding=5, leftIndent=5, rightIndent=5),
        "metric": ParagraphStyle("metric", fontName="Helvetica-Bold", fontSize=17, leading=20,
                                 textColor=c(INK), alignment=TA_CENTER),
        "metric_l": ParagraphStyle("metric_l", fontName="Helvetica", fontSize=8, leading=10,
                                   textColor=c(MUTED), alignment=TA_CENTER),
    }

    def P(text, style="body"):
        return Paragraph(escape(str(text)).replace("\n", "<br/>"), styles[style])

    class NumberedCanvas(pdfcanvas.Canvas):
        """Two-pass canvas so every page footer can say 'Page X of Y'."""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved = []

        def showPage(self):
            self._saved.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            total = len(self._saved)
            for state in self._saved:
                self.__dict__.update(state)
                self._decorate(total)
                super().showPage()
            super().save()

        def _decorate(self, total):
            page = self._pageNumber
            if page == 1:
                return
            self.setStrokeColor(c(RULE))
            self.setLineWidth(0.6)
            self.line(margin, H - 13 * mm, W - margin, H - 13 * mm)
            self.line(margin, 13 * mm, W - margin, 13 * mm)
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(c(ACCENT))
            self.drawString(margin, H - 11 * mm, SKILL_NAME)
            self.setFont("Helvetica", 8)
            self.setFillColor(c(MUTED))
            self.drawRightString(W - margin, H - 11 * mm, f"SEO Audit Report: {data['domain']}")
            self.drawString(margin, 9 * mm, f"Generated {data['date']}")
            self.drawRightString(W - margin, 9 * mm, f"Page {page} of {total}")

    def gauge(score: float, size: float = 120):
        d = Drawing(size, size)
        cx = cy = size / 2
        r = size / 2 - 4
        d.add(Circle(cx, cy, r, fillColor=c(PANEL), strokeColor=None))
        d.add(Wedge(cx, cy, r, 90 - 360 * max(0, min(score, 100)) / 100, 90,
                    fillColor=c(score_hex(score)), strokeColor=None))
        d.add(Circle(cx, cy, r - 12, fillColor=colors.white, strokeColor=None))
        d.add(String(cx, cy - 2, f"{round(score)}", fontName="Helvetica-Bold", fontSize=size / 4,
                     fillColor=c(INK), textAnchor="middle"))
        d.add(String(cx, cy - size / 6.5, f"Grade {score_grade(score)}", fontName="Helvetica",
                     fontSize=size / 13, fillColor=c(MUTED), textAnchor="middle"))
        return d

    def category_bars(cats):
        row_h, label_w, bar_w = 20, 150, body_w - 150 - 40
        d = Drawing(body_w, row_h * len(cats) + 6)
        for i, cat in enumerate(cats):
            y = d.height - (i + 1) * row_h
            s = float(cat.get("score", 0))
            d.add(String(0, y + 6, str(cat["name"])[:30], fontName="Helvetica", fontSize=8.8, fillColor=c(INK)))
            d.add(Rect(label_w, y + 3, bar_w, 11, fillColor=c(PANEL), strokeColor=None))
            d.add(Rect(label_w, y + 3, bar_w * max(0, min(s, 100)) / 100, 11,
                       fillColor=c(score_hex(s)), strokeColor=None))
            d.add(String(label_w + bar_w + 8, y + 6, f"{round(s)}", fontName="Helvetica-Bold",
                         fontSize=9, fillColor=c(INK)))
        return d

    def severity_chip(sev):
        t = Table([[Paragraph(f"<font color='white'><b>{SEVERITY_LABEL[sev].upper()}</b></font>", styles["cell"])]],
                  colWidths=[20 * mm])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), c(SEVERITY_HEX[sev])),
                               ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
        return t

    def grid(rows, widths, header=True):
        t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
        style = [("VALIGN", (0, 0), (-1, -1), "TOP"),
                 ("LINEBELOW", (0, 0), (-1, -1), 0.4, c(RULE)),
                 ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                 ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
        if header:
            style += [("BACKGROUND", (0, 0), (-1, 0), c(PANEL)), ("LINEBELOW", (0, 0), (-1, 0), 0.8, c(INK))]
        t.setStyle(TableStyle(style))
        return t

    findings = data["findings"]
    counts = severity_counts(findings)
    story = []

    # Cover
    story += [Spacer(1, 30 * mm),
              Paragraph(f"<font color='{ACCENT}'><b>{SKILL_NAME.upper()}</b></font>", styles["label"]),
              Spacer(1, 6), P("SEO Audit Report", "title"), Spacer(1, 4), P(data["site"], "subtitle"),
              Spacer(1, 14 * mm)]
    cover = Table([[gauge(data["overall_score"], 150),
                    [P("Overall SEO health score", "h2"),
                     P(data.get("summary") or "Weighted score across every audited category. "
                       "Details and the fix plan follow.", "body"),
                     Spacer(1, 8),
                     P(f"Audit date: {data['date']}", "small"),
                     P(f"Business type: {data.get('business_type', 'Not detected')}", "small"),
                     P(f"Findings: {fmt_number(len(findings))} "
                       f"({counts['critical']} critical, {counts['high']} high, "
                       f"{counts['medium']} medium, {counts['low']} low)", "small")]]],
                  colWidths=[60 * mm, body_w - 60 * mm])
    cover.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    inside = [[P(n, "cellb"), P(t, "cell")] for n, t in (
        ("1", "Executive summary: weighted score, the root problem, top 5 issues and top 5 quick wins"),
        ("2", "Category by category: what works, what is wrong and the fix"),
        ("3", "Action plan by phase: what each fix unblocks, how you would know it failed, what to watch"),
        ("4", "Detailed findings: evidence, affected pages, code and how to confirm each fix"),
        ("5", "Limitations, and how to apply the fixes with Claude Code, Cursor, Antigravity or Lovable"))]
    toc = Table(inside, colWidths=[10 * mm, body_w - 10 * mm])
    toc.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.4, c(RULE)), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                             ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story += [cover, Spacer(1, 18 * mm), P("Inside this report", "h2"), toc, PageBreak()]

    # Executive summary
    story.append(P("Executive summary", "h1"))
    if data.get("method"):
        story += [P(f"Method: {data['method']}", "small"), Spacer(1, 6)]
    if data.get("executive_summary"):
        story += [P(data["executive_summary"]), Spacer(1, 6)]
    if data.get("root_cause"):
        story += [Paragraph("The score is held down by one root problem: <b>" + escape(data["root_cause"])
                            + "</b>", styles["body"]), Spacer(1, 8)]
    wrows = weighted_rows(data)
    if wrows:
        rows = [[P("Category", "cellb"), P("Weight", "cellb"), P("Score", "cellb"), P("Weighted", "cellb")]]
        for n, w, sc, pts in wrows:
            rows.append([P(n, "cell"), P(w, "cell"),
                         Paragraph(f"<font color='{score_hex(sc)}'><b>{sc}</b></font>", styles["cell"]),
                         P(pts, "cell")])
        rows.append([P("Total", "cellb"), P("", "cell"), P("", "cell"), P(str(data["overall_score"]), "cellb")])
        t = grid(rows, [body_w - 75 * mm, 25 * mm, 25 * mm, 25 * mm])
        t.setStyle(TableStyle([("LINEABOVE", (0, -1), (-1, -1), 0.8, c(INK))]))
        story += [P("SEO health score by category", "h2"), t]
    if data.get("supplementary_scores"):
        story += [Spacer(1, 4), P("Supplementary scores (not in the weighted total): "
                                  + ", ".join(f"{k} {v}" for k, v in data["supplementary_scores"].items()) + ".",
                                  "small")]
    story.append(Spacer(1, 8))
    sev_row = [[Paragraph(f"<font size=18 color='{SEVERITY_HEX[s]}'><b>{fmt_number(counts[s])}</b></font>",
                          styles["metric"]) for s in SEVERITIES],
               [P(SEVERITY_LABEL[s] + " issues", "metric_l") for s in SEVERITIES]]
    sev_t = Table(sev_row, colWidths=[body_w / 4] * 4)
    sev_t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), c(PANEL)),
                               ("LINEAFTER", (0, 0), (-2, -1), 2, colors.white),
                               ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [sev_t]

    def numbered(title, items):
        if not items:
            return []
        out = [P(title, "h2")]
        for i, (head, why) in enumerate(items, 1):
            out.append(Paragraph(f"{i}. <b>{escape(head)}.</b> {escape(why)}", styles["body"]))
            out.append(Spacer(1, 3))
        return out

    story += numbered("Top 5 critical issues", top_issues(data))
    story += numbered("Top 5 quick wins", wins_explained(data))

    if data["metrics"]:
        items = list(data["metrics"].items())[:8]
        cells = [[Paragraph(fmt_compact(v), styles["metric"]) for _, v in items],
                 [P(humanize_key(k), "metric_l") for k, _ in items]]
        per = min(len(items), 4)
        rows = []
        for start in range(0, len(items), per):
            rows.append(cells[0][start:start + per] + [""] * (per - len(cells[0][start:start + per])))
            rows.append(cells[1][start:start + per] + [""] * (per - len(cells[1][start:start + per])))
        mt = Table(rows, colWidths=[body_w / per] * per)
        mt.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, c(RULE)),
                                ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
        story += [KeepTogether([P("Key metrics", "h2"), mt])]

    # Category by category
    if data["categories"]:
        story += [PageBreak(), P("Category by category", "h1"), category_bars(data["categories"]), Spacer(1, 6)]
        for cat in data["categories"]:
            items = [f for f in findings if f["category"] == cat["name"]]
            block = [Paragraph(f"{escape(cat['name'])} <font color='{score_hex(cat.get('score', 0))}'>"
                               f"({round(cat.get('score', 0))})</font>", styles["h2"])]
            if cat.get("works"):
                block += [Paragraph("<b>Works:</b> " + escape(", ".join(cat["works"])) + ".", styles["body"]),
                          Spacer(1, 3)]
            if cat.get("notes") or cat.get("summary"):
                block += [P(cat.get("notes") or cat.get("summary")), Spacer(1, 4)]
            if items:
                rows = [[P("Finding", "cellb"), P("Severity", "cellb"), P("Fix", "cellb")]]
                rows += [[P(f"{f['title']} ({f['id']})", "cell"),
                          Paragraph(f"<font color='{SEVERITY_HEX[f['severity']]}'><b>"
                                    f"{SEVERITY_LABEL[f['severity']]}</b></font>", styles["cell"]),
                          P(first_sentence(f["fix"]), "cell")] for f in items]
                block.append(grid(rows, [70 * mm, 20 * mm, body_w - 90 * mm]))
            story += [KeepTogether(block)]

    # Action plan by phase
    story += [PageBreak(), P("Action plan", "h1")]
    if data.get("plan_context"):
        story += [P("What this means", "h2")]
        story += [Paragraph("&#9632; " + escape(x), styles["body"]) for x in data["plan_context"]]
        story.append(Spacer(1, 6))
    story += [P("Each action lists what it unblocks or depends on, how you would know it failed, and a "
                "leading indicator to watch.", "small")]
    n = 0
    for ph, items in plan_rows(data).items():
        if not items:
            continue
        name, when = PHASES[ph]
        rows = [[P("#", "cellb"), P("Action", "cellb"), P("Unblocks / depends on", "cellb"),
                 P("Failure check", "cellb"), P("Leading indicator", "cellb")]]
        for f in items:
            n += 1
            link = f.get("unblocks") or (f"Depends on {f['depends_on']}" if f.get("depends_on") else f["impact"])
            rows.append([P(str(n), "cell"),
                         Paragraph(f"<b>{escape(f['title'])}</b> ({escape(f['id'])}). {escape(first_sentence(f['fix']))}",
                                   styles["cell"]),
                         P(link or "-", "cell"), P(f.get("failure_check") or f["verify"] or "-", "cell"),
                         P(f.get("leading_indicator") or "-", "cell")])
        story += [P(f"{name} ({when})", "h2"),
                  grid(rows, [8 * mm, body_w - 128 * mm, 38 * mm, 42 * mm, 40 * mm])]
    targets = [cat for cat in data["categories"] if cat.get("target") is not None]
    if targets:
        rows = [[P("Category", "cellb"), P("Now", "cellb"), P("After Phases 1 and 2 (target)", "cellb")]]
        rows += [[P(cat["name"], "cell"), P(str(round(cat["score"])), "cell"), P(str(cat["target"]), "cell")]
                 for cat in targets]
        rows.append([P("Health Score", "cellb"), P(str(data["overall_score"]), "cellb"),
                     P(f"about {expected_total(data)}", "cellb")])
        story += [KeepTogether([P("Expected score movement", "h2"),
                                grid(rows, [body_w - 90 * mm, 30 * mm, 60 * mm]), Spacer(1, 4),
                                P("These targets are estimates and depend on the fixes being completed.",
                                  "small")])]

    # Detailed findings
    story += [PageBreak(), P("Detailed findings", "h1"),
              P("Every finding with the evidence seen on the live site, the exact change and how to "
                "confirm it.", "small"), Spacer(1, 6)]
    for f in findings:
        head = Table([[severity_chip(f["severity"]),
                       Paragraph(f"<b>{escape(f['id'])}  {escape(f['title'])}</b>", styles["body"])]],
                     colWidths=[24 * mm, body_w - 24 * mm])
        head.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
        block = [head, Spacer(1, 3), P(f"Category: {f['category']}"
                                       + (f"   |   Effort: {str(f['effort']).capitalize()}" if f["effort"] else "")
                                       + (f"   |   Impact: {f['impact']}" if f["impact"] else "")
                                       + (f"   |   Confidence: {f['confidence']}" if f["confidence"] else ""),
                                       "small")]
        for label, key in (("What is wrong", "detail"), ("Evidence", "evidence"), ("How to fix", "fix")):
            if f[key]:
                block += [Spacer(1, 3), P(label, "label"), P(f[key])]
        if f["pages"]:
            shown = f["pages"][:6]
            more = len(f["pages"]) - len(shown)
            block += [Spacer(1, 3), P("Affected pages", "label"),
                      P("\n".join(shown) + (f"\n+ {fmt_number(more)} more" if more > 0 else ""), "small")]
        if f["code"]:
            wrapped = "\n".join(textwrap.fill(line, 92, subsequent_indent="  ", replace_whitespace=False) or line
                                for line in f["code"].strip("\n")[:2500].splitlines())
            block += [Spacer(1, 4), XPreformatted(escape(wrapped), styles["code"])]
        if f["verify"]:
            block += [Spacer(1, 3), P("How to confirm it is fixed", "label"), P(f["verify"])]
        block.append(Spacer(1, 12))
        story.append(KeepTogether(block[:6]))
        story += block[6:]

    if data.get("limitations"):
        story += [PageBreak(), P("Limitations", "h1")]
        story += [Paragraph("&#9632; " + escape(x), styles["body"]) for x in data["limitations"]]
    # How to apply
    story += [Spacer(1, 10), P("Apply the fixes with an AI coding tool", "h1"),
              P("This audit also produced ready-to-paste prompts in FIX-PROMPTS.md and in the fix-prompts/ "
                "folder. Each prompt carries the evidence, the exact change and a check, batched by priority.")]
    rows = [[P("Tool", "cellb"), P("File", "cellb"), P("How to use", "cellb")],
            [P("Claude Code", "cell"), P("fix-prompts/claude-code.md", "cell"),
             P("Run `claude` in the project folder and paste prompt 1, then the next.", "cell")],
            [P("Cursor", "cell"), P("fix-prompts/cursor.md", "cell"),
             P("Open the project, start an Agent chat, paste one prompt at a time.", "cell")],
            [P("Antigravity", "cell"), P("fix-prompts/antigravity.md", "cell"),
             P("Start an agent task in the Agent Manager and paste one prompt at a time.", "cell")],
            [P("Lovable", "cell"), P("fix-prompts/lovable.md", "cell"),
             P("Paste each short prompt into the project chat and check the preview.", "cell")]]
    story += [Spacer(1, 8), grid(rows, [30 * mm, 50 * mm, body_w - 80 * mm]), Spacer(1, 10),
              P("After applying fixes, run /seo audit again to confirm the finding IDs are gone and to "
                "track the score change.", "small")]

    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=margin, rightMargin=margin,
                            topMargin=20 * mm, bottomMargin=20 * mm,
                            title=f"SEO Audit Report: {data['domain']}", author=SKILL_NAME,
                            subject="SEO audit", creator=SKILL_NAME)
    doc.build(story, canvasmaker=NumberedCanvas)


# ---------------------------------------------------------------- demo data

def demo_data() -> dict:
    return normalize({
        "site": "https://www.example-store.com",
        "business_type": "E-commerce",
        "stack": {"framework": "Next.js 15 (App Router)", "hosting": "Vercel", "cms": "Shopify (headless)"},
        "executive_summary": "The store is crawlable and fast on desktop, but product pages ship without "
                             "Product schema, 1,240 URLs have duplicate titles, and mobile LCP fails on "
                             "category pages. Fixing the 2 critical items should unblock rich results and "
                             "recover lost impressions.",
        "metrics": {"pages_crawled": 18452, "indexed_pages": 12870, "organic_clicks_28d": 48210,
                    "impressions_28d": 3215400, "avg_position": 18.4, "mobile_lcp_ms": 3900},
        "categories": [
            {"name": "Technical SEO", "score": 71, "weight": 0.22, "summary": "Redirect chains and 404s in sitemap."},
            {"name": "Content quality", "score": 64, "weight": 0.23, "summary": "Thin category copy, no author pages."},
            {"name": "On-page SEO", "score": 58, "weight": 0.2, "summary": "Duplicate titles and missing metas."},
            {"name": "Schema", "score": 35, "weight": 0.1, "summary": "No Product or BreadcrumbList markup."},
            {"name": "Performance (CWV)", "score": 52, "weight": 0.1, "summary": "Mobile LCP 3.9s on categories."},
            {"name": "AI search readiness", "score": 61, "weight": 0.1, "summary": "GPTBot blocked, weak citability."},
            {"name": "Images", "score": 77, "weight": 0.05, "summary": "Missing alt text on 9% of images."},
        ],
        "findings": [
            {"id": "SCH-001", "severity": "critical", "category": "Schema", "effort": "medium",
             "title": "Product pages have no Product structured data",
             "detail": "None of the 9,800 product URLs output Product JSON-LD, so they cannot show price, "
                       "stock or review rich results.",
             "evidence": "0 application/ld+json blocks of type Product on /products/* (sampled 50 URLs).",
             "pages": ["https://www.example-store.com/products/linen-shirt"],
             "files_hint": ["app/products/[handle]/page.tsx"],
             "fix": "Render a Product JSON-LD block server-side on every product page using live price, "
                    "currency, availability and aggregateRating when reviews exist.",
             "code": '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"Product",'
                     '"name":"Linen Shirt","image":["https://www.example-store.com/img/linen.jpg"],'
                     '"offers":{"@type":"Offer","price":"49.00","priceCurrency":"USD",'
                     '"availability":"https://schema.org/InStock"}}\n</script>',
             "verify": "Rich Results Test shows a valid Product item for 3 sampled product URLs."},
            {"id": "TECH-002", "severity": "critical", "category": "Technical SEO", "effort": "low",
             "title": "Staging noindex header leaks onto /collections/*",
             "detail": "Collection pages send X-Robots-Tag: noindex, removing 312 category pages from Google.",
             "evidence": "curl -I https://www.example-store.com/collections/shirts returns x-robots-tag: noindex",
             "files_hint": ["next.config.js", "middleware.ts"],
             "fix": "Remove the noindex header for production and keep it only when VERCEL_ENV is preview.",
             "verify": "curl -I on 3 collection URLs shows no x-robots-tag header."},
            {"id": "ONP-003", "severity": "high", "category": "On-page SEO", "effort": "low",
             "title": "1,240 pages share duplicate title tags",
             "detail": "Filtered and paginated product listings reuse the parent title.",
             "fix": "Generate unique titles: '{Collection} - Page {n} | Example Store', and canonicalize "
                    "filter URLs to the unfiltered collection.",
             "verify": "Crawl shows 0 duplicate titles among indexable URLs."},
            {"id": "CWV-004", "severity": "high", "category": "Performance (CWV)", "effort": "medium",
             "title": "Mobile LCP is 3.9s on category pages",
             "detail": "The hero banner is a 1.2MB PNG loaded lazily.",
             "files_hint": ["components/CollectionHero.tsx"],
             "fix": "Serve the hero as AVIF/WebP at the rendered size, remove loading=lazy, add fetchpriority=high.",
             "verify": "PageSpeed Insights mobile LCP under 2.5s for /collections/shirts."},
            {"id": "GEO-005", "severity": "medium", "category": "AI search readiness", "effort": "low",
             "title": "robots.txt blocks OAI-SearchBot and PerplexityBot",
             "fix": "Allow OAI-SearchBot and PerplexityBot (search crawlers) while keeping training bots "
                    "blocked if you prefer.",
             "code": "User-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /",
             "verify": "robots.txt tester allows / for both user agents."},
            {"id": "IMG-006", "severity": "low", "category": "Images", "effort": "low",
             "title": "9% of product images have empty alt text",
             "fix": "Use the product name plus the variant (color) as alt text.",
             "verify": "Image audit reports under 1% empty alt on product pages."},
        ],
    })


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, help="findings JSON written by /seo audit")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--demo", action="store_true", help="build a sample report from bundled demo data")
    parser.add_argument("--no-pdf", action="store_true", help="only write the fix prompts")
    args = parser.parse_args(argv)
    if not args.demo and not args.data:
        parser.error("--data is required unless --demo is set")
    data = demo_data() if args.demo else load_data(args.data)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    if args.demo:
        (out / "seo-findings.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    written = write_markdown(data, out) + write_prompts(data, out)
    if not args.no_pdf:
        pdf = out / "SEO-Report.pdf"
        build_pdf(data, pdf)
        written.insert(0, pdf)
    print(json.dumps({"written": [str(p) for p in written], "findings": len(data["findings"]),
                      "overall_score": data["overall_score"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
