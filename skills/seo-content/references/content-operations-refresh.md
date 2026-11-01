# Content Operations Pipeline (part 2: refresh, links, distribution, measurement)

Continues `content-operations-pipeline.md`. Source: leopard627/fire-your-seo-agency (MIT).

## 5. Refresh & pruning - content decays

Publishing isn't the end. Stale posts lose citations; wrong posts cost trust.

**Refresh triggers** - any one sets `status: refresh-needed`:
- The underlying data changed (earnings release, price change, policy change)
- 28-day impressions down 30%+ versus 60 days earlier
- The query's wording shifted in search data (e.g. "2025" → "2026")
- A factual error found or reported

**Refresh rules**:
- [ ] `dateModified` bumps **only when the content actually changed** - date-only bumps are
      detectable and backfire (`references/aeo.md`, E-E-A-T)
- [ ] One change-log line at the bottom of the post: "Updated 2026-10-30: Q3 results added" -
      a trust signal and a record
- [ ] A refreshed post goes back through the publish gate (including a fresh IndexNow ping)

**Merge & delete**:
- [ ] Two posts on the same question: **301 + canonical** to the stronger one, the weaker gets
      `status: merged`. Duplicates split rankings between themselves
- [ ] Deletion is the last resort: refresh or 301 first. If you truly remove a post, return 410
      and drop it from the sitemap
- [ ] If a URL must change, keep the 301 forever (`references/llmo.md` §3 - the address the model remembers)

**Quarterly inventory review**: counts by status (published / refresh-needed / merged) plus a
decision on every zero-impression post.

## 6. Internal link structure

Past a few dozen posts, link structure *is* crawl priority:

- **Hub → spoke → data**: topic hub (e.g. `/blog/earnings`) → question posts → the ledger data page
- [ ] Per post: 1 link up (hub) + 2 sideways (related questions) + a link to the data page
- [ ] Anchor text is the question or noun itself (never "here" or "this post") - the anchor is
      the target page's topic signal
- [ ] Zero orphans: a post that's only in the sitemap and linked from nowhere gets the lowest
      crawl priority
- [ ] If a hub is thin (just a list of links), give the hub its own direct answer, overview and
      table so it stands as a page
- [ ] BreadcrumbList LD + visible breadcrumbs declare the hierarchy to machines too

## 7. Distribution - cross-posting

Your domain is the ledger; everything external is a satellite. **Order matters**: distribute
externally only after indexing on your own domain is confirmed (1–3 days) - if you don't claim
the original first, a copy gets treated as the original.

| Surface | What goes there | Don't |
|---|---|---|
| Naver Blog (inside) | Summary + perspective + 1–2 links to your data pages | Paste the whole body; link-spam (`references/neo-naver.md` §3–4) |
| Medium · Brunch · velog | Full text if canonical can be set, otherwise summary + link | Full copies with no canonical |
| Threads · X · LinkedIn | One key number + link (this is both an LLMO surface and a traffic source) | The same phrasing on every post |
| GitHub README · build log | How you built it, measured - factual register | Promotional tone |

- [ ] **Check whether the editor renders Markdown first**: the Naver Blog editor does not. Paste a
      Markdown draft and `#`, `**` and `|` show up as literal characters - rebuild headings, bold
      and tables with the editor's own tools, then check the published post on mobile for leaked symbols
- [ ] Log distribution timing in the inventory - this is where you learn which channel actually drives traffic

## 8. Measurement - "N posts a month" is not a metric

An agency report's "12 posts published this month" is output, not outcome. This skill's metrics:

- **Share of posts that get seen or cited**: of published posts, how many have 28-day impressions > 0 / are cited by AI
- Per-post 28-day impressions, clicks and average position (inventory refreshed monthly)
- AI-citation O/X on the 5–10 target questions (Perplexity, ChatGPT search, Naver AI Briefing)
- Backlog burn rate vs. inflow - an empty backlog means it's time to re-read the query data

Signal → next action:

| Signal | Action |
|---|---|
| Impressions up, clicks down | Title and description (`references/seo.md` §3) |
| Zero impressions 14 days after publishing | Check indexing: sitemap, noindex, SSR, IndexNow |
| Stuck at position 5–15 | Strengthen the direct answer, table, as-of dates; add internal links |
| Impressions but no AI citation | Check for a competing original source, paragraph self-containment, llms.txt listing |
| Impressions down 30% | Refresh trigger (section 5) |

Reports add a **per-post line** to the format in `references/measure.md` §5:

```
[Content] published 6 · refreshed 3 · merged 1 | seen 5/6 · AI-cited 2/6 | backlog remaining 14
```
