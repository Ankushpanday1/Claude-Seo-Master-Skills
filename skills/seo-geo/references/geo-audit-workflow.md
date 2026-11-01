# GEO Full-Site Audit Workflow

Load on demand from `seo-geo` when the request covers a whole domain rather than
one page. Merged from geo-seo-claude (audit orchestration and composite score)
and Agentic-SEO-Skill (passage indexing rules). Page-level scoring still uses
the five dimensions in `SKILL.md`.

## Phase 1: Discovery (sequential)

1. Fetch the homepage with `render_page.py --mode auto --json`.
2. Detect the business type (table below).
3. Collect key pages from `sitemap.xml` or internal links, up to 50.

## Phase 2: Parallel analysis

Spawn these agents at once, each with the same `output_dir`:

| Agent | Covers |
|-------|--------|
| `seo-geo` | Citability, AI crawler access, llms.txt status, brand mentions |
| `seo-ai-platforms` (skill) or the platform section of `seo-geo` | Per-platform readiness |
| `seo-technical` | SSR, Core Web Vitals (LCP, INP, CLS), crawlability, indexability |
| `seo-content` | E-E-A-T, original data, author credentials, readability |
| `seo-schema` | Schema completeness, JSON-LD validation, sameAs |

## Phase 3: Synthesis (sequential)

1. Collect all agent findings.
2. Compute the site-level composite (below) next to the page-level GEO score.
3. Build a prioritized action plan (Critical, High, Medium, Low, with effort).
4. Write `GEO-ANALYSIS.md`.

## Site-Level GEO Composite (0-100)

| Category | Weight | Measured by |
|----------|--------|-------------|
| AI Citability and Visibility | 25% | Passage scores, answer block quality, AI search crawler access |
| Brand Authority Signals | 20% | Mentions on Reddit, YouTube, Wikipedia, LinkedIn; entity presence |
| Content Quality and E-E-A-T | 20% | Expertise signals, original data, author credentials |
| Technical Foundations | 15% | SSR, Core Web Vitals, crawlability, mobile, security |
| Structured Data | 10% | Schema completeness, JSON-LD validity, sameAs coverage |
| Platform Optimization | 10% | Per-platform readiness (AIO, AI Mode, ChatGPT, Perplexity, Copilot) |

Rules carried over from the base skill:

- llms.txt is reported but carries no weight in any category.
- Platform Optimization is a readiness estimate from observable signals unless a
  tool (DataForSEO, SE Ranking, Profound, GA4 via `/seo ai-visibility`)
  measured it; label it accordingly.

Score bands: 0-20 Critical, 21-40 Poor, 41-60 Fair, 61-80 Good, 81-100 Excellent.

## Business-Type Detection

| Type | Signals | GEO emphasis |
|------|---------|--------------|
| SaaS | Pricing page, "Sign up", "Free trial", `/app`, API docs | SoftwareApplication schema, comparison pages |
| Local service | Phone, address, "near me", Maps embed, service area | LocalBusiness schema, GBP (`/seo local`) |
| E-commerce | Product pages, cart, price elements, Product schema | Product schema, review aggregation (`/seo ecommerce`) |
| Publisher | Blog, bylines, dates, Article schema | Original reporting, author entities, freshness |
| Agency | Portfolio, case studies, client logos | Case-study data, named experts |
| Other | None of the above | General GEO practice |

## Crawl Quality Gates

- Max 50 pages per audit.
- 30-second timeout per fetch.
- 1-second delay between requests, max 5 concurrent.
- Always fetch and respect robots.txt.
- Skip pages with more than 80% content similarity to one already scored.

## Quick Mode

For a 60-second snapshot, score only the homepage plus one key page: AI search
crawler access, top 3 passages, entity check, SSR check. Report inline, no file.

## Passage Indexing Rules

Google ranks individual passages independently of the full page, which matters
most for long-form content.

1. **Self-contained sections**: each H2 block fully answers one question without
   needing other sections.
2. **Question then answer**: question-phrased H2/H3, direct answer in the first
   sentence.
3. **No pronoun-heavy openings**: start with the full subject, not "It" or "This".
4. **Length**: keep to the base heuristic (about 130-170 words); Google does not
   require chunking.

| Scenario | Google behavior |
|----------|-----------------|
| Strong page, weak section | The full page ranks |
| Weak page, one excellent section | That passage can rank for a specific query |
| Long Q&A page | Individual Q&A passages can rank on their own |

### Speakable markup (limited)

`speakable` (SpeakableSpecification with `cssSelector`) marks passages for
text-to-speech. Google documents it as beta, for news publishers, in English in
the US, on Google Assistant surfaces. Recommend it only for eligible news
publishers; it is not an AI Overviews or AI Mode signal.

```json
{
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".answer-block", "#key-definition"]
  }
}
```
