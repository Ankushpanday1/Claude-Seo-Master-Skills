# Merge Report

How five MIT-licensed SEO skill packs became one plugin. Rule: **union**. A check that exists in several packs is kept once, in the most complete and most current version, with the missing pieces from the other versions woven in. A check that exists in one pack only is added as is. On factual conflicts the most recently maintained guidance wins (INP not FID, FAQ rich results retired May 7 2026, HowTo deprecated, llms.txt optional and ignored by Google Search).

| Source | Commit merged |
|---|---|
| AgriciDaniel/claude-seo (base) | 6be93f4 |
| Bhanunamikaze/Agentic-SEO-Skill | 445c46c |
| zubair-trabzada/geo-seo-claude | 989cae0 |
| Ryze-AI-Adgent/open-seo-mcp-skills | f587b0a |
| leopard627/fire-your-seo-agency | 5f7249f |

## Added as new skills (unique to one pack)

| Skill | Source |
|---|---|
| seo-aeo, seo-article, seo-github, seo-links | Agentic-SEO-Skill |
| seo-citability, seo-ai-crawlers, seo-llmstxt, seo-brand-mentions, seo-ai-platforms, seo-proposal, seo-prospect, seo-compare | geo-seo-claude |
| seo-keywords, seo-rank-tracking, seo-competitor-gap, seo-vs-ads, seo-ai-visibility | open-seo-mcp-skills (need the free Ryze MCP connector) |
| seo-naver | fire-your-seo-agency (NEO lane) |
| seo-report | New: PDF report and fix prompts |

Agents added: seo-verifier, seo-github-analyst, seo-github-benchmark, seo-github-data (Agentic-SEO-Skill); seo-ai-visibility, seo-platform-analysis (geo-seo-claude).

Scripts: Agentic-SEO-Skill scripts live in `scripts/agentic/`, geo-seo-claude scripts in `scripts/geo/`, fire-your-seo-agency's asset optimizer in `scripts/fire/`. All run through the same launcher: `scripts/claude-seo run agentic/<name>.py`.

Not carried over: geo-seo-claude's `geo-update` (self-updater for that repo), duplicate per-repo installers and CI, upstream promo footers.

## Merged into existing skills

`seo-audit` and the `seo` hub were merged by hand: crawler-eye smoke test (fire), evidence rubric and confidence labels plus the fact checker step (Agentic), AI readiness sub-weights and business-type adjustments (geo), Search Console data checks (open-seo), measure-after-fix (fire), and the new PDF and fix-prompt step. The detailed per-item logs follow.


---

## Merge Log: Technical, Sitemap, Hreflang, Images, Performance, Visual

Sources: Agentic = Bhanunamikaze/Agentic-SEO-Skill (agentic-resources), GEO = zubair-trabzada/geo-seo-claude (geo-skills, geo-agents).

| Target file | Added item | Source repo |
|---|---|---|
| skills/seo-technical/SKILL.md | Description extended with server performance, robots.txt, security headers, SSR, TTFB triggers | Agentic, GEO |
| skills/seo-technical/SKILL.md | `agentic/robots_checker.py` call | Agentic |
| skills/seo-technical/SKILL.md | robots.txt common errors (no User-agent group, wildcard over-blocking, site-wide Disallow, Crawl-delay handling) | GEO |
| skills/seo-technical/SKILL.md | Compare Googlebot/bingbot rules with AI crawler rules, report discrepancies | GEO |
| skills/seo-technical/SKILL.md | `X-Robots-Tag` header noindex check plus `agentic/x_robots_header_checker.py` | GEO, Agentic |
| skills/seo-technical/SKILL.md | Common noindex mistakes (paginated, category, landing pages) | GEO |
| skills/seo-technical/SKILL.md | Depth 4+ crawled less; key pages linked from homepage/nav | GEO |
| skills/seo-technical/SKILL.md | Amazonbot row in AI crawler table | GEO |
| skills/seo-technical/SKILL.md | Googlebot and bingbot checked in same pass; blocking either is Critical (Copilot grounds on Bing) | GEO |
| skills/seo-technical/SKILL.md | Legacy tokens (`anthropic-ai`, `cohere-ai`) may be ineffective; verify against vendor docs | Agentic |
| skills/seo-technical/SKILL.md | Canonical on every indexable page; HTML vs HTTP Link header canonical conflict; canonical chains | GEO |
| skills/seo-technical/SKILL.md | `agentic/canonical_checker.py` call | Agentic (script) |
| skills/seo-technical/SKILL.md | HTTP vs HTTPS and trailing-slash duplicate variants; parameter variants need canonical or robots rule | GEO |
| skills/seo-technical/SKILL.md | `agentic/duplicate_content.py` call | Agentic |
| skills/seo-technical/SKILL.md | `<html lang>` check | GEO |
| skills/seo-technical/SKILL.md | Do not noindex paginated pages with unique items | GEO |
| skills/seo-technical/SKILL.md | `agentic/hreflang_checker.py` quick check, defer to seo-hreflang | Agentic |
| skills/seo-technical/SKILL.md | Index bloat estimate: sitemap and indexed counts vs valuable pages | GEO |
| skills/seo-technical/SKILL.md | HTTP 301 to HTTPS, unexpired certificate | GEO |
| skills/seo-technical/SKILL.md | Permissions-Policy header; `agentic/security_headers.py` call | GEO, Agentic |
| skills/seo-technical/SKILL.md | URL hygiene: no session IDs, lowercase, hyphens not underscores, no encoded spaces; `agentic/url_quality.py` | GEO, Agentic (script) |
| skills/seo-technical/SKILL.md | Nesting deeper than 4 levels flagged | GEO |
| skills/seo-technical/SKILL.md | Redirect loops, 302 on permanent move, `agentic/redirect_checker.py` with HTTP-to-HTTPS trace | GEO, Agentic |
| skills/seo-technical/SKILL.md | No fixed-width elements wider than viewport | GEO |
| skills/seo-technical/SKILL.md | WCAG AA contrast 4.5:1 / 3:1; no hover-only essential controls | GEO |
| skills/seo-technical/SKILL.md | `agentic/mobile_render_checker.py` call | Agentic (script) |
| skills/seo-technical/SKILL.md | `agentic/pagespeed.py --strategy mobile` fallback without credentials | Agentic |
| skills/seo-technical/SKILL.md | Pointer to CWV needs-improvement/poor bands | GEO, Agentic |
| skills/seo-technical/SKILL.md | Low/Medium/High CWV risk rating from source when no field data, labelled as estimate | GEO |
| skills/seo-technical/SKILL.md | `lcp_subparts.py` call for LCP phase breakdown | Agentic |
| skills/seo-technical/SKILL.md | `agentic/javascript_render_audit.py` raw vs rendered diff | Agentic (script) |
| skills/seo-technical/SKILL.md | AI crawlers do not execute JS; raw-HTML element checklist (body, H1-H3, nav/links, JSON-LD, head tags) | GEO |
| skills/seo-technical/SKILL.md | CSR shell vs SSR marker signals (`__NEXT_DATA__`, `__NUXT__`, `data-server-rendered`) | GEO |
| skills/seo-technical/SKILL.md | JS-dependency severity ladder (Critical/High/Medium/Low) | GEO |
| skills/seo-technical/SKILL.md | Hydration errors, script lazy-loaded above-fold content, hash routing, noscript-held content | Agentic |
| skills/seo-technical/SKILL.md | Framework mapping: Nuxt for Vue, Angular SSR | GEO |
| skills/seo-technical/SKILL.md | IndexNow: Seznam, Copilot/Bing rationale, key file location, CMS plugins, `agentic/indexnow_checker.py`, `indexnow_submit.py` | GEO, Agentic |
| skills/seo-technical/SKILL.md | New category 10 Server Performance and Page Weight (TTFB curl, page weight, minify/unused, bundle sizes, async/defer, compression, caching, CDN headers, resource hints) | GEO |
| skills/seo-technical/SKILL.md | `agentic/third_party_script_audit.py`, `agentic/critical_request_chain.py`, `agentic/cache_compression_checker.py` calls | Agentic (scripts) |
| skills/seo-technical/SKILL.md | Voice search pointer (HTTPS, TTFB, mobile prerequisites; speakable to seo-aeo) | Agentic |
| skills/seo-technical/SKILL.md | Category status thresholds (80% / 50%) and overall score bands | GEO |
| skills/seo-technical/SKILL.md | Server Performance row, AI Crawler Access table, Rendering Assessment in Output | GEO |
| skills/seo-technical/SKILL.md | Execution Plan (agent mode) with script run order and response-header capture | Agentic, GEO |
| skills/seo-technical/SKILL.md | Reference Files load-on-demand pointer | (structure) |
| skills/seo-technical/references/rendering-and-performance.md (new) | Security header expected values and severity guide | GEO, Agentic |
| skills/seo-technical/references/rendering-and-performance.md | SSR/CSR detection method, severity table, CSR/SSR signals, framework fixes | GEO, Agentic |
| skills/seo-technical/references/rendering-and-performance.md | CWV risk indicators per vital (no field data) | GEO |
| skills/seo-technical/references/rendering-and-performance.md | Common LCP/INP/CLS fixes table (scheduler.yield, content-visibility, size-adjust, preconnect) | GEO, Agentic |
| skills/seo-technical/references/rendering-and-performance.md | Server performance threshold table; `agentic/font_audit.py` | GEO, Agentic (script) |
| skills/seo-sitemap/SKILL.md | Coverage percentage | Agentic |
| skills/seo-sitemap/SKILL.md | Sitemap index child validation | Agentic |
| skills/seo-sitemap/SKILL.md | Helper scripts: `agentic/sitemap_checker.py`, `agentic/broken_links.py`, `agentic/orphan_pages_from_sitemap.py`, `agentic/hreflang_sitemap_validator.py` | Agentic |
| skills/seo-sitemap/SKILL.md | Canonicalized URLs row (High), Missing lastmod row (Medium) | Agentic |
| skills/seo-sitemap/SKILL.md | Hreflang sitemap extension note (xmlns:xhtml, full alternate set) | Agentic |
| skills/seo-sitemap/SKILL.md | Discovery and submission methods (robots.txt, GSC/BWT, IndexNow ping) | Agentic |
| skills/seo-sitemap/SKILL.md | `agentic/sitemap_generator.py` for generation, with `--index` and lastmod caution | Agentic (script) |
| skills/seo-sitemap/SKILL.md | API documentation pages safe at scale; under 40% unique content as penalty risk with `duplicate_content.py` | Agentic |
| skills/seo-sitemap/SKILL.md | Coverage/missing/extra pages in analysis output | Agentic |
| skills/seo-hreflang/SKILL.md | Helper scripts `agentic/hreflang_checker.py` (incl. `--verify-returns`) and `agentic/hreflang_sitemap_validator.py`, with caveat that base rules win | Agentic |
| skills/seo-images/SKILL.md | Helper scripts `agentic/image_inventory.py` and `agentic/image_weight_audit.py` | Agentic (scripts) |
| skills/seo-images/SKILL.md | JPEG XL lossless JPEG recompression (about 20%) benefit | Agentic |
| skills/seo/references/cwv-thresholds.md | LCP subpart heuristic budget (100/700/50ms), labelled non-Google | Agentic |
| skills/seo/references/cwv-thresholds.md | INP fixes: scheduler.yield, web workers, content-visibility, will-change | GEO, Agentic |
| skills/seo/references/cwv-thresholds.md | GSC custom chart annotations and social-channel data (late 2025) | Agentic |
| agents/seo-technical.md | Response-header capture, html lang, meta robots directives, "Home"/"Untitled" title note | GEO |
| agents/seo-technical.md | Redirect rules (loops, HTTP to HTTPS, 301 vs 302) | Agentic |
| agents/seo-technical.md | CWV risk rating, SSR as highest-priority AI check, AI crawler validation step, server performance step | GEO, Agentic |
| agents/seo-technical.md | Available Scripts table (11 agentic scripts) | Agentic |
| agents/seo-technical.md | Delegation to seo-geo, seo-agentic, seo-aeo | Agentic, GEO |
| agents/seo-technical.md | Output: AI crawler table, rendering assessment, CWV risk table; category 10; Seznam | GEO |
| agents/seo-sitemap.md | Step 8 sitemap index validation | Agentic |
| agents/seo-sitemap.md | Available Scripts table (7 scripts) | Agentic |
| agents/seo-sitemap.md | >50MB, canonicalized URLs, missing lastmod rows | Agentic |
| agents/seo-sitemap.md | API docs safe; UGC; editorial review; under 40% unique risk | Agentic |
| agents/seo-sitemap.md | Sitemap index and extension note, Discovery Methods, coverage %, Cross-Skill Delegation | Agentic |
| agents/seo-performance.md | LCP subparts table with heuristic budget | Agentic |
| agents/seo-performance.md | Fixes per issue, large DOM for LCP, impact ranking | Agentic |
| agents/seo-performance.md | INP checklist (will-change, content-visibility, sync XHR, workers) | Agentic |
| agents/seo-performance.md | Scripts: `agentic/pagespeed.py`, `lcp_subparts.py`, `agentic/parse_html.py`, `agentic/critical_request_chain.py`, `agentic/third_party_script_audit.py`, `agentic/font_audit.py` | Agentic |
| agents/seo-performance.md | Output: actual values, LCP bottleneck subpart, impact levels; Cross-Skill Delegation | Agentic |
| agents/seo-visual.md | Step 6 SSR/CSR DOM diff; `analyze_visual.py` and `agentic/javascript_render_audit.py` calls | Agentic |
| agents/seo-visual.md | Extra viewports (tablet landscape, Android 360x800) as manual pass | Agentic |
| agents/seo-visual.md | Above-fold nav/logo checks and anti-patterns list | Agentic |
| agents/seo-visual.md | Mobile checklist: viewport meta, forms, sticky elements | Agentic |
| agents/seo-visual.md | Visual issue severity table, image checks hand-off, SSR/CSR diff table | Agentic |
| agents/seo-visual.md | Output per viewport, image and SSR notes; Cross-Skill Delegation | Agentic |

Total rows: 86.

## Deliberately NOT merged

- Agentic and GEO claim that FID was removed from Lighthouse, and that Google crawls "exclusively" with mobile Googlebot: base wording is more accurate (kept base).
- GEO: "blocking Google-Extended may reduce presence in AI Overviews": conflicts with base (Google-Extended does not affect Search or AI Overviews).
- GEO: canonicalizing paginated pages to page 1 or a view-all page, and "Bing still uses rel=next/prev": outdated or unverified; base self-canonical guidance kept.
- GEO: configure URL parameters in Search Console: tool retired 2022 (added a note saying so instead).
- GEO: "ChatGPT uses Bing's index": not verifiable; kept the Copilot/Bing rationale only.
- GEO: Prerender.io/Rendertron as SSR solutions: dynamic rendering is flagged as technical debt in base; Rendertron is archived. Angular Universal replaced by Angular SSR wording.
- GEO: IndexNow key at `/.well-known/indexnow-key.txt`: incorrect; replaced with the protocol default `/<key>.txt` or `keyLocation`.
- GEO: fixed point weights per category (15/12/10...) and the agent's 25% SSR weighting: base scoring is "share of measured checks"; added only status thresholds and score bands.
- GEO Category 9 / Step 10 (RFC 8288 Link headers, Markdown content negotiation): already owned by `seo-agentic` (discovery-and-markdown reference); added a delegation line instead.
- GEO: title 50-60 chars, description 150-160 chars, OG/Twitter tag audit: on-page scope owned by `seo-page`.
- GEO: 44x44px touch target: conflicts with base (WCAG 24x24 minimum, 48x48 comfortable).
- Agentic: redirect chains up to 3 hops OK: conflicts with base (max 1 hop).
- Agentic: x-default "Required"/High severity and `zh` "without region" ambiguity: base is more precise.
- Agentic: Voice search statistics (90% of answers from snippets, 46% local, 80% mobile) and platform table (Siri on Bing): unsourced or outdated.
- Agentic: "~3-5% of websites use AI-specific robots.txt rules": unsourced, dated.
- Agentic: image sitemap example with `<image:title>`: deprecated tag since 2022.
- Agentic: ">100 sitemaps in index is unusual": no basis (index allows 50,000 children).
- Agentic CWV ref: "Dec 2025 core update weighted mobile CWV more", Oct 2025 pass rates, Lighthouse 13 "updated scoring weights", Soft Navigations as origin trial: speculative or superseded by base.
- Agentic: PSI and CrUX curl examples with `key=` in the URL: base uses header-based key handling via scripts.
- Agentic: inline Playwright screenshot code: duplicate of `capture_screenshot.py`.
- Agentic: `llm-audit-rubric.md` chain-of-thought scoring reference: not part of this plugin's scope.
- Agentic: "Intrusive interstitial (Google penalizes this on mobile)" wording: base page-experience framing kept; listed only as an anti-pattern.
- hreflang and images alternates otherwise duplicated the base nearly word for word.

---

## Merge Log: Content & Schema Scope

Base: AgriciDaniel/claude-seo. Sources: Agentic-SEO-Skill (agentic), geo-seo-claude (geo), open-seo-mcp-skills (Ryze).

## Added Items

| Target file | Added item | Source repo |
|---|---|---|
| skills/seo-content/SKILL.md | Workflow section (fetch, inventory of word count/headings/lists/tables/images/links/byline/dates, scoring order) | geo-seo-claude (geo-content skill + agent) |
| skills/seo-content/SKILL.md | Optional script table: agentic/eeat_signal_checker, readability, article_seo, citation_readiness, answer_block_scanner, freshness_checker, entity_checker, duplicate_content, competitor_gap; geo/citability_scorer | Agentic-SEO-Skill, geo-seo-claude |
| skills/seo-content/SKILL.md | Word count floors for About, FAQ/Q&A and Pillar pages | geo-seo-claude, Agentic-SEO-Skill (agent) |
| skills/seo-content/SKILL.md | Readability: <30 / >80 guardrails, FK grade by audience, 40-80 word paragraphs, >150 word wall-of-text flag, passive voice <15%, jargon defined, manual Flesch formula with approximation caveat | geo-seo-claude, Agentic-SEO-Skill (agent) |
| skills/seo-content/SKILL.md | Structure: exactly one H1, no skipped levels, descriptive and question-phrased headings, heading density, one idea per paragraph lead-with-claim | geo-seo-claude |
| skills/seo-content/SKILL.md | Internal linking: orphan pages rarely cited, hub-and-spoke pillar linking | geo-seo-claude |
| skills/seo-content/SKILL.md | Extra low-quality AI markers (listicle-heavy, stock transitions, hedging overload, no voice) | Agentic-SEO-Skill (agent), geo-seo-claude |
| skills/seo-content/SKILL.md | Passage-level optimization (self-contained H2/H3 blocks, 100-200 words, answer in first 40-50 words, list 5-9 items, table <=4 cols) | Agentic-SEO-Skill (skill + agent) |
| skills/seo-content/SKILL.md | Freshness: specific dates, schema date consistency, time-dependent phrasing, evergreen | geo-seo-claude |
| skills/seo-content/SKILL.md | Output: topical authority modifier, content metrics table, pages analyzed and freshness tables, most/least citable passages, AI content likelihood, prioritized recommendations (quick wins, content gaps, E-E-A-T steps) | geo-seo-claude |
| skills/seo-content/references/eeat-signal-checklist.md (new) | Per-factor signal checklists with weak-signal flags (mapped to base 20/25/25/30 weights) | geo-seo-claude, Agentic-SEO-Skill (agent) |
| skills/seo-content/references/eeat-signal-checklist.md (new) | AI-content low/high quality signal tables and likelihood labels | geo-seo-claude |
| skills/seo-content/references/eeat-signal-checklist.md (new) | Freshness tiers (3/6/12/24 months), YMYL weighting, evergreen rules | geo-seo-claude |
| skills/seo-content/references/eeat-signal-checklist.md (new) | Topical authority assessment and +10/-5 modifier | geo-seo-claude |
| agents/seo-content.md | Step 9 (passage readiness, topical authority) and pre-scoring inventory | geo-seo-claude |
| agents/seo-content.md | Available Scripts table (launcher form) | Agentic-SEO-Skill, geo-seo-claude |
| agents/seo-content.md | E-E-A-T evidence signal checklist per factor | Agentic-SEO-Skill, geo-seo-claude |
| agents/seo-content.md | Pillar page row and word count bands (thin/short/standard/long/deep-dive) | Agentic-SEO-Skill, geo-seo-claude |
| agents/seo-content.md | Readability targets table with audience adjustments | Agentic-SEO-Skill |
| agents/seo-content.md | Extra AI markers and likelihood labels, "never claim definitively" rule | Agentic-SEO-Skill, geo-seo-claude |
| agents/seo-content.md | Answer & Citation Readiness section (40-55 word answer, question headings, list/table snippet formats) | Agentic-SEO-Skill |
| agents/seo-content.md | Cross-skill delegation to entity_checker, seo-plan 4.5, seo-cluster | Agentic-SEO-Skill |
| agents/seo-content.md | Output: llm-audit-rubric scoring, metrics table, heading tree, AI assessment, topical authority, freshness, priority levels | Agentic-SEO-Skill, geo-seo-claude |
| agents/seo-content.md | Important Notes (approximation caveats, crawl limits, YMYL freshness, 2-year flag) | geo-seo-claude |
| skills/seo-schema/SKILL.md | Microdata itemtype / RDFa vocab, multiple blocks, high-priority JSON-LD migration flag | geo-seo-claude |
| skills/seo-schema/SKILL.md | WebFetch strips head warning, use parse_html/render_page | geo-seo-claude |
| skills/seo-schema/SKILL.md | Validation additions: https context, invalid JSON, misspelled props, enumerations, duplicate blocks, author as string, recommended props, nesting, sameAs/URL resolution, VideoObject.contentUrl, self-serving reviews, rendering method | geo-seo-claude, Agentic-SEO-Skill (agent) |
| skills/seo-schema/SKILL.md | Optional script checks agentic/schema_required_props.py, agentic/rich_results_guard.py (with FAQ wording caveat) | Agentic-SEO-Skill |
| skills/seo-schema/SKILL.md | Recipe added to ACTIVE list | Agentic-SEO-Skill (agent), geo-seo-claude (agent) |
| skills/seo-schema/SKILL.md | AI crawlers generally do not execute JS, client-injected JSON-LD may be invisible | geo-seo-claude (agent) |
| skills/seo-schema/SKILL.md | Generation rules: always-generate set, @graph, @id, server-rendered placement | geo-seo-claude |
| skills/seo-schema/SKILL.md | agentic/validate_schema.py post-edit / pre-commit check | Agentic-SEO-Skill |
| skills/seo-schema/SKILL.md | Output: page/format/rich-result-eligible columns, sameAs audit table, implementation notes (Rich Results Test + Schema.org Validator) | geo-seo-claude |
| skills/seo-schema/references/entity-graph-geo.md (new) | Entity-clarity recommended properties per type, `identifier` | geo-seo-claude, Agentic-SEO-Skill (agent) |
| skills/seo-schema/references/entity-graph-geo.md (new) | sameAs priority list (14 platforms) and 5-step audit; entity_checker.py | geo-seo-claude, Agentic-SEO-Skill |
| skills/seo-schema/references/entity-graph-geo.md (new) | speakable example (marked beta) | geo-seo-claude, Agentic-SEO-Skill (agent) |
| skills/seo-schema/references/entity-graph-geo.md (new) | Optional 0-100 entity-graph scoring rubric | geo-seo-claude |
| skills/seo-schema/references/entity-graph-geo.md (new) | Organization template with full entity signals (@id, founder, knowsAbout, Wikidata) | geo-seo-claude |
| agents/seo-schema.md | Block/format/type inventory, WebFetch warning, entity assessment step | geo-seo-claude (agent) |
| agents/seo-schema.md | Available Scripts table (parse_html, schema_required_props, validate_schema, entity_checker) | Agentic-SEO-Skill |
| agents/seo-schema.md | ClaimReview, VehicleListing, Practice Problem in never-recommend list | Agentic-SEO-Skill (base skill already had these) |
| agents/seo-schema.md | Checklist items 8-10 (sameAs valid, author object, no duplicate blocks) | Agentic-SEO-Skill, geo-seo-claude |
| agents/seo-schema.md | Rich result eligibility table, Entity SEO properties (about, mentions, identifier, knowsAbout) | Agentic-SEO-Skill, geo-seo-claude |
| agents/seo-schema.md | Output: deprecated warnings, entity assessment, delivery method risk, ranked opportunities, [REPLACE: ...] placeholders, priority actions; cross-skill delegation | Agentic-SEO-Skill, geo-seo-claude |
| skills/seo/references/schema-types.md | Recipe row in Active table | Agentic-SEO-Skill (agent) |
| schema/templates.json | New templates: BlogPosting, Article, Organization, LocalBusiness, BreadcrumbList, WebSite (base kept on ProductGroup conflict; em dashes removed; WebSite and BreadcrumbList descriptions corrected to base facts) | Agentic-SEO-Skill |
| skills/seo-page/SKILL.md | llm-audit-rubric pointer (single-page scope) | Agentic-SEO-Skill |
| skills/seo-page/SKILL.md | Execution Plan: fetch_page, parse_html, agentic/readability, pagespeed_check, agentic/article_seo | Agentic-SEO-Skill |
| skills/seo-page/SKILL.md | Output files FULL-AUDIT-REPORT.md, ACTION-PLAN.md, SEO-REPORT.html via agentic/generate_report.py | Agentic-SEO-Skill |
| skills/seo-plan/SKILL.md | agentic/competitor_gap.py for data-driven content gaps | Agentic-SEO-Skill |
| skills/seo-plan/SKILL.md | Section 4.5 Topical Authority Cluster Planning (hub diagram, pillar/cluster specs, 5-step process, industry cluster table) | Agentic-SEO-Skill |
| skills/seo-plan/SKILL.md | agentic/topical_cluster_mapper.py for coverage tracking | Agentic-SEO-Skill (script) |
| skills/seo-plan/SKILL.md | TOPIC-CLUSTERS.md deliverable, Topical Coverage % KPI | Agentic-SEO-Skill |
| skills/seo-content-brief/SKILL.md | Cannibalization check (expand an existing half-covering page instead) | open-seo-mcp-skills (Ryze) |
| skills/seo-content-brief/SKILL.md | Record SERP features (FS, PAA, video, local pack) | open-seo-mcp-skills (Ryze) |
| skills/seo-content-brief/SKILL.md | Table stakes vs the opening (differentiating angle) | open-seo-mcp-skills (Ryze) |
| skills/seo-content-brief/SKILL.md | "Questions to Answer" output section (PAA + question keywords) | open-seo-mcp-skills (Ryze) |
| skills/seo-content-brief/SKILL.md | Optional "Live Data via Ryze MCP" path (setup, DataForSEO SERP via connector, Google Ads keyword ideas + volumes, GSC existing foothold) | open-seo-mcp-skills (Ryze) |

Total: 58 rows.

## Deliberately Not Merged

- **seo-plan/assets/*.md vs agentic templates**: base is newer on every difference (FAQ retired, GBP Q&A API, AI Overview local coverage, site reputation abuse EEA rule, Merchant listing props); agentic adds nothing new. Unchanged.
- **seo-programmatic, seo-competitor-pages**: agentic versions are older subsets of base (only em dash formatting and outdated pagination/rel=next, faceted noindex, 50k-only sitemap rule). Unchanged.
- **eeat-framework.md, quality-gates.md**: agentic adds "December 2025 watershed / E-E-A-T for all competitive queries" and industry traffic-drop percentages, which base explicitly rejects as unsourced. Agentic scoring bands already live in base `eeat-scoring-guide.md`. Unchanged.
- **schema-types.md outdated claims**: FAQPage gov/health restriction, Dataset "retired", "~2.5x AI answer uplift", SearchAction sitelinks search box, PerformingArtsEvent as a v29.4 addition. Base kept.
- **Keyword density 1-3%** (agentic seo-content, seo-page): base says no target density.
- **E-E-A-T equal 25/25/25/25 weights** (agentic skill, geo) and geo's 15%-per-dimension composite (with metrics/AI/topical/freshness components): conflict with base 20/25/25/30 model. Signals merged, weights not.
- **FAQPage "use for GEO / non-Google AI"**, **HowTo "still useful for AI parsing"**, **FAQPage restricted to gov/health**: superseded by the May 7, 2026 retirement.
- **llms.txt as a GEO content requirement** (agentic agent): conflicts with base's citation of Google's gen-AI guide (no AI files needed); llms.txt belongs to seo-agentic.
- **speakable as a "direct GEO signal" recommended for all pages** (geo): kept only as optional, beta, per base schema-types.md.
- **"AI Mode has zero organic blue links"** and "AI Mode launched May 2025 in 180+ countries" (agentic seo-content): base deliberately avoids version- and stat-tied AI Mode claims.
- **Pillar page word count 2,000 minimum** (geo) vs **3,000-5,000** (agentic): both kept, framed as floor vs typical range.
- **Ryze setup page URL with utm tracking parameters**: dropped the tracking link; connector URL and `claude mcp add` command kept.
- **geo fetch_page.py `~/.claude/skills/geo/...` invocation**: replaced by base parse_html.py / render_page.py launcher calls.

## Notes

- `skills/seo-content/references/content-operations-pipeline.md` is 277 lines (pre-existing, over the 200-line reference limit); not in this scope, left untouched.
- `agentic/rich_results_guard.py` still carries the pre-May-2026 FAQPage wording; the skill tells readers the status list wins.

---

## Merge log: GEO, backlinks, ecommerce, local

| Target file | Added item | Source repo |
|---|---|---|
| skills/seo-geo/SKILL.md | "Deeper Sub-Skills" routing table: /seo citability, ai-crawlers, llmstxt, brands, ai-platforms, aeo, ai-visibility, agentic | Task brief (combined plugin) |
| skills/seo-geo/SKILL.md | Pointers to references/geo-lane-playbook.md and references/llmo.md | fire-your-seo-agency |
| skills/seo-geo/SKILL.md | Scripted Checks table: geo/citability_scorer.py, geo/brand_scanner.py | geo-seo-claude |
| skills/seo-geo/SKILL.md | Scripted Checks: agentic/citation_readiness.py, answer_block_scanner.py, entity_checker.py, ai_crawler_policy_matrix.py | Agentic-SEO-Skill |
| skills/seo-geo/SKILL.md | Use on-site brand name, not domain, for mention scans | geo-seo-claude (geo-ai-visibility agent) |
| skills/seo-geo/SKILL.md | Passage-Level Rules: self-contained H2 blocks, no pronoun openings, answer in first sentence | Agentic-SEO-Skill (seo-geo.md) |
| skills/seo-geo/SKILL.md | Primary Source lane: own-computed figures on stable URLs, subject + number + as-of date + method paragraphs, crawler policy by purpose (training / search index / live fetch), quarterly roster recheck, Bing index check | fire-your-seo-agency (geo.md) |
| skills/seo-geo/SKILL.md | LLMO lane: identical brand spelling, name-collision check, sameAs, factual wiki pages, permanent permalinks and 301s, update all surfaces together | fire-your-seo-agency (llmo.md) |
| skills/seo-geo/SKILL.md | Verification loop (search-mode citation check with diagnosis order; browsing-off model test, quarterly log) | fire-your-seo-agency |
| skills/seo-geo/SKILL.md | Output items 11-12: citation-ready/unlikely passages, verification log; pointer to full-site workflow | geo-seo-claude, fire-your-seo-agency |
| skills/seo-geo/references/geo-audit-workflow.md (new) | 3-phase audit orchestration (discovery, parallel agents, synthesis) | geo-seo-claude (geo hub) |
| skills/seo-geo/references/geo-audit-workflow.md | Site-level 6-category GEO composite with weights and score bands | geo-seo-claude (geo hub) |
| skills/seo-geo/references/geo-audit-workflow.md | Business-type detection table with GEO emphasis | geo-seo-claude (geo hub) |
| skills/seo-geo/references/geo-audit-workflow.md | Crawl quality gates (50 pages, 30 s timeout, 1 s delay, 5 concurrent, skip >80% similar) and quick mode | geo-seo-claude (geo hub) |
| skills/seo-geo/references/geo-audit-workflow.md | Passage indexing rules, passage vs full-page table, Speakable (with beta / news / US-English caveat) | Agentic-SEO-Skill |
| agents/seo-geo.md | Per-block 5-dimension passage scoring, >70 / <30 flags, page score = mean of top 5 | geo-seo-claude (geo-ai-visibility) |
| agents/seo-geo.md | Crawler status Allowed/Blocked/Restricted/Unknown; secondary crawlers (Amazonbot, Meta); broad Disallow, Crawl-delay, missing Sitemap checks; ai_crawler_policy_matrix.py | geo-seo-claude, Agentic-SEO-Skill |
| agents/seo-geo.md | Content-Signal non-scored flag; llms-full.txt and llms.txt format validation (no score) | geo-seo-claude (geo-ai-visibility) |
| agents/seo-geo.md | Wikipedia API check (not site: search), entity_checker.py, Present/Minimal/Absent per platform incl. G2/Trustpilot/Capterra | geo-seo-claude, Agentic-SEO-Skill |
| agents/seo-geo.md | Platform readiness rubric with sub-score points for AIO, ChatGPT, Perplexity, Gemini, Copilot; strongest/weakest, synergies, concrete actions; score bands in output | geo-seo-claude (geo-platform-analysis) |
| agents/seo-geo.md | Evidence rules (no fabrication, "unverifiable from external analysis"); 12-month recency for Perplexity community signals | geo-seo-claude (geo-platform-analysis) |
| skills/seo-backlinks/SKILL.md | Optional Ryze MCP source (DataForSEO summary/referring_domains/anchors, ahrefs/semrush fallback, never fabricate) | open-seo-mcp-skills (backlink-check) |
| skills/seo-backlinks/SKILL.md | GSC "Top linking sites" as free source | Agentic-SEO-Skill (seo-links.md) |
| skills/seo-backlinks/SKILL.md | GA4 referral cross-check of linking domains | open-seo-mcp-skills |
| skills/seo-backlinks/SKILL.md | Naked-URL <5% unnatural signal; repeated exact-match commercial anchors; same anchor across one domain | Agentic-SEO-Skill (link-building.md), open-seo-mcp-skills |
| skills/seo-backlinks/SKILL.md | Own outbound links: agentic/external_link_quality.py, agentic/link_profile.py | Agentic-SEO-Skill |
| skills/seo-backlinks/SKILL.md | Extra toxic signals: no organic traffic or deindexed, 200+ outbound links, scraper sites, new domains with many outlinks, velocity spike on low-authority profile | Agentic-SEO-Skill, open-seo-mcp-skills |
| skills/seo-backlinks/SKILL.md | agentic/redirect_backlink_reclaim.py for 404 and long-chain link targets from an export | Agentic-SEO-Skill |
| skills/seo-backlinks/SKILL.md | Outreach list fields and Ryze competitor diff; verdict-first output with index-estimate labels | open-seo-mcp-skills |
| skills/seo-backlinks/references/link-acquisition.md (new) | Digital PR, journalist platforms, broken link building, unlinked mentions, disavow scope rules, manual-action recovery steps, anchor_text_audit.py hand-off | Agentic-SEO-Skill (link-building.md) |
| agents/seo-backlinks.md | Optional Ryze tier, GA4 referral check, supporting agentic scripts | open-seo-mcp-skills, Agentic-SEO-Skill |
| skills/seo-ecommerce/SKILL.md | agentic/product_schema_checker.py and agentic/review_schema_checker.py in product workflow | Agentic-SEO-Skill |
| skills/seo-ecommerce/SKILL.md | Raw-HTML (non-JS) Product JSON-LD check | Agentic-SEO-Skill (templates/ecommerce.md) |
| skills/seo-ecommerce/SKILL.md | Content items (use cases, fit guide, care); Variants block (ProductGroup variesBy/hasVariant, hasCertification) | Agentic-SEO-Skill (templates/ecommerce.md) |
| skills/seo-ecommerce/SKILL.md | New section 1b: collection_page_checker.py, faceted_nav_audit.py, category checklist, content priority order, `/seo ecommerce category` command, output block | Agentic-SEO-Skill |
| skills/seo-ecommerce/SKILL.md | seo-geo cross-skill row: consistent product entity data across site, Merchant Center, marketplaces | Agentic-SEO-Skill (templates/ecommerce.md) |
| skills/seo-local/SKILL.md | agentic/local_seo_checker.py scripted pass | Agentic-SEO-Skill |
| skills/seo-local/SKILL.md | GBP: video verification readiness, messaging channel after chat shutdown, SAB area rule (no whole states or countries) | Agentic-SEO-Skill (templates/local-service.md) |
| skills/seo-local/SKILL.md | Location-page uniqueness sources, service/location URL architecture, build order | Agentic-SEO-Skill (templates/local-service.md) |
| skills/seo-local/SKILL.md | Schema by page type (Service, ContactPage); local GEO checks; tracking plan output item | Agentic-SEO-Skill (templates/local-service.md) |

## Deliberately not merged

| Item | Source | Reason |
|---|---|---|
| Whole content of citability, crawlers, llms.txt, brand-mention, platform, AEO, AI-visibility skills | geo-seo-claude, open-seo-mcp-skills | Already standalone skills; seo-geo now links to them |
| llms.txt score (10% of AI Visibility) and "llms.txt first" in diagnosis order | geo-seo-claude, fire | Conflicts with base: llms.txt carries no weight and is ignored by Google Search |
| "AI crawlers do NOT execute JavaScript", 134-167 and 100-200 word passage rules, "156% higher selection" | Agentic-SEO-Skill | Base has more accurate, hedged versions |
| GPTBot = ChatGPT search, ClaudeBot = Claude web features, anthropic-ai row | Agentic-SEO-Skill, geo-seo-claude | Outdated; base separates training and search bots (tests enforce this) |
| GEO market size, 4.4x conversion, Gartner -50%, 23% of marketers, 1.5B AIO users | geo-seo-claude | Unverified or superseded third-party stats |
| Recommending FAQPage or HowTo schema for AIO | geo-seo-claude | FAQ rich results retired 7 May 2026; HowTo rich results retired |
| /geo prospect, proposal, compare, report-pdf, update commands and PDF pipeline | geo-seo-claude | Outside this scope (agency and CRM features, separate skills) |
| rel=next/prev and "canonical to main category" pagination advice | Agentic-SEO-Skill (ecommerce, programmatic) | Outdated; replaced with self-canonical paginated pages and crawlable links |
| Anchor targets branded 40-50%, exact <=5%; DR >=40/60 targets; "Qwoted (formerly HARO)" | Agentic-SEO-Skill | Base anchor table kept on conflict; DR targets kept only as a heuristic; HARO claim inaccurate |
| "Disavow takes 3-6 months", "2-8 week review", "5-15% conversion" figures | Agentic-SEO-Skill | Unsourced numbers softened to qualitative guidance |
| Location page word counts (600/500/800) and 40% unique for service-area pages | Agentic-SEO-Skill (local-service.md) | Conflicts with base (>60-70% unique, swap test) |
| "Business hours top-5 factor", AIO 0.14% local stat, 30/50 location page gates | Agentic-SEO-Skill | Already in base |
| Internal link health, orphan pages, broken links from seo-links.md | Agentic-SEO-Skill | Belongs to standalone seo-links skill |

## Flags for the orchestrator

- skills/seo-geo/references/llmo.md and geo-lane-playbook.md (copied in earlier, outside my edit scope) contain em dashes (U+2014) and should be cleaned.
- Pre-existing test failures not caused by these files: manifest counts, sub-skill and subagent lists, maxTurns and early-write instruction missing on newly added agents (seo-ai-visibility, seo-platform-analysis, seo-github-analyst, seo-verifier), skills/seo-content/references/content-operations-pipeline.md over 200 lines.
