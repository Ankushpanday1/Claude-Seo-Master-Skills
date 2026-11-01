# Audit Extensions

Load on demand from `seo-audit`. Merged from geo-seo-claude (business-type adjustments, AI readiness breakdown) and open-seo-mcp-skills (search-data checks).

## Search data checks (Google Search Console or Ryze MCP)

Run only when real Search Console data is available (`seo-google`, or the Ryze MCP connector at `https://connector.get-ryze.ai/mcp`). Never replace the site's own data with third-party estimates. Compare the last 90 days with the previous 90; Search Console lags about 2 days, so never include today.

| Check | Rule | Typical fix |
|---|---|---|
| Decaying pages | Clicks down more than 30% period over period | Refresh content, check intent shift, check lost links |
| CTR anomalies | Average position 5 or better but CTR under 2% | Rewrite title and meta description; check SERP features taking the click |
| Striking distance | Position 8 to 20 with high impressions | Strengthen the page: internal links, section for the query, title match |
| Cannibalization | Same query, two or more ranking URLs splitting clicks | Merge, differentiate intent, or canonicalize |
| Indexation | Large or rising "Crawled, currently not indexed" or excluded counts | Quality and internal linking review of the affected templates |
| AI referrals | Sessions from chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com | Report the trend; note which landing pages AI engines send traffic to |

For the 3 to 5 worst pages, inspect the URL (canonical chosen by Google, indexing state, last crawl). A page can hold rankings but lose revenue: cross-check organic sessions and conversions by landing page when analytics is connected.

## AI Search Readiness breakdown

The AI Search Readiness category (10% of the SEO Health Score) is scored from these sub-weights so it lines up with `/seo geo`:

| Sub-area | Weight | Measured by |
|---|---|---|
| AI citability | 25% | `geo/citability_scorer.py`, answer-first passages, quotable facts |
| Brand authority | 20% | `/seo brands`: third-party mentions, entity signals |
| Content E-E-A-T | 20% | `seo-content` findings |
| Technical GEO | 15% | AI crawler access, rendering without JavaScript, speed |
| Structured data | 10% | Organization, Person, Article, Product markup quality |
| Platform optimization | 10% | `/seo ai-platforms` per-engine readiness |

Rating bands: 90 to 100 Excellent, 75 to 89 Good, 60 to 74 Fair, 40 to 59 Poor, 0 to 39 Critical.

Severity hints for AI readiness: all AI search crawlers blocked, or content only visible after JavaScript with no server rendering, is Critical. Blocking the main AI search crawlers (OAI-SearchBot, PerplexityBot, Claude-SearchBot) is High. A missing llms.txt is at most Low: it is optional and ignored by Google Search.

## Business-type adjustments

| Type | Look harder at | Key schema |
|---|---|---|
| SaaS | Feature comparison tables, integration pages, docs and changelog structure, knowledge base | SoftwareApplication, Organization |
| Local business | NAP consistency, Google Business Profile, service area pages, review markup | LocalBusiness, GeoCoordinates, OpeningHoursSpecification |
| E-commerce | Product description quality, buying guides, faceted navigation, review aggregation | Product, Offer, AggregateRating, BreadcrumbList |
| Publisher | Author credentials, source citations, freshness, original research | Article or NewsArticle, Person, ClaimReview |
| Agency or services | Case studies with numbers, team expertise, industry pages | Organization, Service, Person, Review |

Do not recommend HowTo schema (deprecated) or new FAQPage markup for Google rich results (retired for all sites May 7, 2026).

## Crawl quality gates

- Canonicalize URLs before fetching (http vs https, www vs non-www, trailing slash) and skip duplicates.
- Analyze HTML only; skip PDFs, images and other binaries.
- Log failed fetches and keep going; list them in the report appendix.
