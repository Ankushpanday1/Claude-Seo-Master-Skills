# Content Operations - Sub-blog & Content Management

Once the technical base (SEO) and machine readability (AEO·GEO) are in place, one job
remains: **keep producing sentences worth citing, and refresh them when they go stale.**
This is where most of an agency's retainer goes ("N posts per month"). This document turns
that job from intuition into a **pipeline**: collect questions → brief → write → publish
gate → refresh → measure.

Content cuts across all five lanes. What content does for each:

| Lane | Role of content |
|---|---|
| SEO | Number and freshness of indexable pages |
| AEO | The supply line for "one question = one page" |
| GEO | Paragraph-level citation material (subject + number + as-of date + method) |
| LLMO | The record of how you built it = a surface that survives into the training corpus |
| NEO | The inside (Naver blog) half of the two-track strategy |

## 0. Audit - content status

```bash
# Is there a blog, and can crawlers see it?
curl -s -o /dev/null -w '%{http_code}\n' https://example.com/blog
curl -sL https://example.com/blog | grep -c '<article\|<h2'          # is the listing SSR'd?
curl -s -o /dev/null -w '%{http_code}\n' https://example.com/feed.xml # RSS/Atom exists?
curl -sL https://example.com/sitemap.xml | grep -c '/blog/'           # posts in sitemap
curl -sL https://example.com/sitemap.xml | grep -o '<lastmod>[^<]*' | sort | tail -1  # latest publish
# Sample one post: does the first paragraph answer directly, is there Article LD?
curl -sL https://example.com/blog/some-post | grep -o '"@type":"[A-Za-z]*"' | sort | uniq -c
```

- [ ] Build a **content inventory** - one row per post: URL · title · target question · type ·
      published · last modified · 28-day impressions/clicks · status. Without this table, every
      later decision is a guess
- [ ] Count three things in the inventory: ① posts with no target question ② posts not updated
      in 90+ days ③ posts with zero impressions. Those three numbers are the audit result

Scorecard evidence example: "34 posts, 0 mapped to a question, 0 published in 90 days, 21 with zero impressions."

## 1. Where to put it - sub-blog location

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Subdirectory** `example.com/blog` | Domain authority consolidates; sitemap, llms.txt and LD managed in one place | Deploys are coupled to the main app | ✅ Default |
| **Subdomain** `blog.example.com` | Separate stack and deploys | In practice treated close to a separate site; authority splits | Only when the main app cannot SSR |
| **External platform** (Naver Blog, Brunch, Medium, velog) | Platform-native reach and readers | Your ledger of facts lives on someone else's domain; no canonical control; policy risk | Satellite only (section 7) |

Principle: **the ledger of facts (data and question pages) lives on your domain; external
platforms are summary-plus-link satellites.**

Technical requirements for the sub-blog (condensed from `references/seo.md`):

- [ ] SSR/SSG - Markdown → static HTML is the safest path. If you use a CMS, verify the
      rendered output with curl
- [ ] Unique title (50–60 chars), description (150–160 chars) and OG image per post
- [ ] `Article` (or `BlogPosting`) JSON-LD: headline · datePublished · dateModified · author ·
      publisher referencing the global Organization `@id` (never re-declared per page)
- [ ] `BreadcrumbList` LD plus visible breadcrumbs
- [ ] RSS/Atom feed - the shared input for crawlers, readers and IndexNow triggers
- [ ] **Automatic** sitemap inclusion with accurate lastmod (hand-maintained sitemaps always miss)
- [ ] Tag, category and pagination pages: thin listings with fewer than 3 posts get noindex;
      only listings you intend to grow into hubs get indexed. Left alone, hundreds of thin pages
      burn crawl budget
- [ ] Post URLs are slug-only, no dates (`/blog/samsung-earnings-date`) - a refreshed post
      never carries a stale URL

## 2. Content model - metadata for one post

Every post carries the frontmatter (or CMS fields) below. **Generate both the render and the
JSON-LD from this single source** and visible-text/LD mismatches become impossible:

```yaml
---
title: "When is Samsung Electronics' earnings date"   # identical to h1
slug: samsung-earnings-date
question: "samsung earnings date"                      # the exact phrase people type
answer: "Samsung Electronics' next earnings release is October 30, 2026 (tentative)."  # first-paragraph direct answer, ~40 chars in Korean / one short sentence
description: "…"                                       # 150–160 chars, a reason to click
type: question        # question | data | glossary | buildlog | comparison
datePublished: 2026-09-21
dateModified: 2026-09-21                               # bump only on real content changes
data_asof: 2026-09-20                                  # as-of date for the numbers in the body
author: { name: "…", url: "/about" }
sources:
  - { name: "DART (Korean regulatory filings)", url: "https://dart.fss.or.kr/…" }
faq:
  - { q: "Is the release during market hours or after close?", a: "…" }
related: [samsung-dividend-date, earnings-calendar]
status: published     # draft | review | published | refresh-needed | merged
canonical: https://example.com/blog/samsung-earnings-date
---
```

- [ ] An empty `question` blocks publishing - a post that doesn't know which question it answers
      gets extracted as the answer to none
- [ ] `answer` is rendered verbatim as the first paragraph - in metadata only, invisible on
      screen, it counts for nothing
- [ ] `data_asof` is shown next to the numbers in the body ("as of 2026-09-20") - numbers
      without a reference date lose trust points
- [ ] `faq` is the single source for both the visible FAQ section and the FAQPage LD

## 3. Post types - the five that get cited

| Type | Shape | Which lane feeds on it |
|---|---|---|
| **Question page** | One "when / how much / how" question, direct answer + evidence table | AEO·NEO |
| **Data page** | Numbers you compute yourself, stable URL, stated refresh cadence | GEO (the body of primary-source strategy) |
| **Glossary / definition** | One-sentence definition + comparison table + example | AEO (the #1 extractable shape) |
| **Build log / changelog** | What you built, why, how - with measured numbers | LLMO (training surface) + the "Experience" in E-E-A-T |
| **Comparison page** | Table-first, dated, no home-team bias | AEO·GEO |

What you don't make:
- ❌ Rehashed news, summaries of other people's data: the original source takes the citation
      (`references/geo.md` §3)
- ❌ Keyword-variant page farms ("best X", "best X 2026", "X ranking"…): copies of the same
      answer split rankings among themselves, and at scale they fall under "scaled content abuse"
- ❌ Posts with no answer: a post that concludes "it depends" gets cited by no engine

## 4. Pipeline

### 4-1. Question backlog

A content calendar is not "this month's topics" - it's **a queue of questions to answer**.
Sources, in order:

1. Top queries in GSC and Naver Search Advisor that **have no dedicated page** (`references/measure.md` §4)
2. Queries with impressions but average position 5–15 - already candidates, weak on direct
   answer or tables
3. Site search, support tickets, customer questions
4. Autocomplete and related searches (both Naver and Google)

Manage it in `content/backlog.md`:

```markdown
| Question | Evidence | Type | Status | URL |
|---|---|---|---|---|
| samsung dividend record date | GSC 1,240 impressions · pos 11 | question | draft | |
| how to calculate PER | autocomplete · 3 support tickets | glossary | backlog | |
```

Priority: **has impressions and ranks low > has impressions and no dedicated page > estimated
new demand**. Posts written on estimated demand alone sit at the bottom of the backlog.

### 4-2. Brief - one minute before writing

Fill five lines before writing. If you can't, the post isn't ready to be written yet:

```
Question:       (the exact phrase people type)
Direct answer:  (one sentence, with the number/date)
Evidence:       (data for one table + as-of date + source URL)
Sub-questions:  (the 3 that become the FAQ)
Internal links: (1 hub + 2 related posts/data pages)
```

### 4-3. Writing rules - machine readability

Apply the sentence rules of `references/aeo.md` and `geo.md` at the post level:

- [ ] First paragraph = direct answer. No intro, no background, no greeting
- [ ] Self-contained paragraphs: each carries its own subject, number and as-of date
      (no "the figure mentioned above")
- [ ] Think in tables first - three or more numbers means a table, not prose
- [ ] H2s are the sub-questions verbatim (`## Is the release during market hours or after close`)
- [ ] Length is whatever the answer needs. "2,000+ words" rules breed filler, and filler buries
      the direct answer
- [ ] Every number gets a source and an as-of date. If you computed it, one line on the method
- [ ] **AI-draft policy**: drafting with AI is allowed, provided ① every number is checked against
      the original source ② a human reviews and signs as author ③ no mass auto-publishing.
      Search engines judge "was it verified", not "who wrote it" - the problem with unverified AI
      posts isn't their origin, it's wrong numbers and empty conclusions
- [ ] Regulated sectors (finance, health, legal): no predictive or advisory sentences - only what
      the data settles

### 4-4. Publish gate - every item passes or it doesn't ship

- [ ] Frontmatter: `question`, `answer`, `data_asof`, `sources` filled; h1 = title
- [ ] `curl -sL <url>` shows the body, direct answer and table in HTML (no JavaScript)
- [ ] Title and description unique, within length, no duplicates site-wide
- [ ] Article LD present, dateModified = actual date, publisher references the global Organization `@id`
- [ ] Visible FAQ text = FAQPage LD, character for character
- [ ] Internal links: 1 up (hub) + 2 sideways (related) minimum, zero broken links
- [ ] Image alt, width/height, total weight checked
- [ ] In the sitemap with accurate lastmod (verified with curl after deploy)
- [ ] IndexNow ping (consumed by Bing and Naver) - built into the publish pipeline
- [ ] If it's a data page or hub-grade: add an entry to `llms.txt`
- [ ] RSS updated
- [ ] If Naver is a target: request crawling in Search Advisor

### 4-5. After publishing

Record the baseline (publish date, target question, current impressions 0) → schedule a
**re-measurement 14 days out** in the inventory. Run the loop in `references/measure.md` per post.

Continued in `content-operations-refresh.md` (refresh and pruning, internal links, distribution, measurement).
