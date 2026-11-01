# seo-findings.json schema

Input for `master_report.py`. Only `site` and `findings` are required; everything else improves the report.

```json
{
  "site": "https://www.example.com",
  "business_type": "SaaS",
  "date": "October 30, 2026",
  "overall_score": 68,
  "executive_summary": "Two or three sentences: health, the biggest problem, what fixing it unlocks.",
  "stack": {"framework": "Next.js 15 (App Router)", "hosting": "Vercel", "cms": "Sanity"},
  "metrics": {"pages_crawled": 1840, "indexed_pages": 1512, "organic_clicks_28d": 48210, "mobile_lcp_ms": 2900},
  "categories": [
    {"name": "Technical SEO", "score": 71, "weight": 0.22, "summary": "One line."}
  ],
  "quick_wins": ["TECH-002", "ONP-003"],
  "findings": [
    {
      "id": "TECH-002",
      "severity": "critical",
      "category": "Technical SEO",
      "title": "Staging noindex header leaks onto /collections/*",
      "detail": "What is wrong and why it matters.",
      "evidence": "Exact observation: header, tag, metric or script output.",
      "confidence": "Confirmed",
      "pages": ["https://www.example.com/collections/shirts"],
      "files_hint": ["middleware.ts", "next.config.js"],
      "fix": "The exact change to make.",
      "code": "Optional reference snippet.",
      "effort": "low",
      "impact": "Restores 312 category pages to the index.",
      "verify": "How to confirm the fix worked."
    }
  ]
}
```

## Field rules

| Field | Rule |
|---|---|
| `severity` | `critical`, `high`, `medium` or `low` (anything else becomes `medium`) |
| `id` | Stable prefix by area: `TECH`, `ONP`, `CNT`, `SCH`, `CWV`, `IMG`, `GEO`, `LOC`, `LNK`, `INT`; auto-filled as `F-001` if missing |
| `overall_score` | 0 to 100; if missing it is the weighted mean of `categories` |
| `categories[].weight` | Defaults from `seo-audit`: Technical 0.22, Content 0.23, On-page 0.20, Schema 0.10, Performance 0.10, AI readiness 0.10, Images 0.05 |
| `metrics` | Raw numbers, not formatted strings; the script applies US formatting. Up to 8 are shown |
| `quick_wins` | Finding IDs; if missing, Critical or High findings with `effort: low` are used |
| `effort` | `low`, `medium` or `high` |
| `pages` | Full URLs; the PDF shows 6 and the prompts 10, then a count |
| `files_hint` | Repo-relative paths when the stack makes them likely; leave empty rather than guess wildly |
| `confidence` | `Confirmed`, `Likely` or `Hypothesis` (see `../../seo/references/llm-audit-rubric.md`) |

## Mapping from audit-data.json

When only the older `audit-data.json` envelope exists: `summary.health_score` becomes `overall_score`, `summary.business_type` becomes `business_type`, each `categories[].findings[]` item becomes a finding with `category` set to the parent name, `description` becomes `detail`, `recommendation` becomes `fix`. `Info` severity findings are dropped from the prompts.

## Explained-report fields (optional, recommended)

These turn the output into a fully explained report (`FULL-AUDIT-REPORT.md`, `ACTION-PLAN.md` and the matching PDF sections). Write them in plain language a founder can follow.

| Field | Where it shows |
|---|---|
| `method` | One line under the title: agents run, pages sampled, sitemap URLs checked |
| `root_cause` | "The score is held down by one root problem: ..." in the executive summary. Name the single cause behind most findings |
| `top_issues` | List of `{"title", "why"}`; defaults to the first 5 Critical and High findings |
| `supplementary_scores` | Scores outside the weighted total, for example `{"SXO Gap": "41/100"}` |
| `categories[].works` | "Works:" line: what is already right in that category |
| `categories[].notes` | Short narrative for the category (falls back to `summary`) |
| `categories[].target` | Expected score after Phases 1 and 2; feeds the "Expected score movement" table |
| `findings[].phase` | 1 Remove risk (week 1), 2 Earn rankings (weeks 2 to 3), 3 Authority and coverage (month 2), 4 Hygiene (ongoing); inferred from severity and effort if missing |
| `findings[].unblocks` / `depends_on` | What the fix makes possible, or which finding must land first |
| `findings[].failure_check` | The observation that proves the fix did not work |
| `findings[].leading_indicator` | What to watch before rankings move (a Search Console report, a count, a CTR) |
| `plan_context` | Bullets under "What this means" at the top of the action plan |
| `limitations` | What was not measured and why (API quota, no Search Console, sampled pages) |
