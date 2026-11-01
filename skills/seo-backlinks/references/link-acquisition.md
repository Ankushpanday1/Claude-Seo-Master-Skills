# Link Acquisition and Manual-Action Recovery

Load on demand from `seo-backlinks` when recommending how to earn links or when a
site has a manual action for unnatural links. Merged from Agentic-SEO-Skill
(`references/link-building.md`). Toxic patterns, anchor benchmarks and the
disavow file format live in `${CLAUDE_PLUGIN_ROOT}/skills/seo/references/backlink-quality.md`; this
file does not repeat them.

## What Google devalues

Google's spam policies (expanded in March 2024) target link schemes: private
blog networks, paid or exchanged links at scale, mass-produced exact-match
anchors, and repurposing expired domains to pass their old reputation. Most of
these links are now ignored automatically rather than penalized.

## What still earns links

### Digital PR and linkable assets

- Original data studies: surveys, analysis of a proprietary dataset
- Industry benchmarks ("State of [Industry] [Year]")
- Calculators and free tools that solve a real problem
- Well-researched counterintuitive takes

Use an authority proxy (Moz DA, Ahrefs DR, DataForSEO rank) to shortlist target
publications; aim higher as the site matures. Treat any DR or DA cut-off as a
planning heuristic, not a Google signal.

### Journalist request platforms

- Examples: Qwoted, SourceBottle, ResponseSource, Featured. The HARO and
  Connectively brands have changed hands and format since 2024; confirm a
  platform is live before recommending it.
- Reply format: credentials first, a direct 2-3 sentence quote, data if you have it.
- Speed matters: answer within hours of the request posting.

### Broken link building

1. Find authoritative pages in the niche that link to dead URLs.
2. Build or point to content that matches the dead page's intent.
3. Email the page owner with a polite replacement suggestion.

Pair with `agentic/redirect_backlink_reclaim.py` for the site's own dead targets:
reclaiming links to your own 404s is faster than earning new ones.

### Unlinked brand mentions

- Monitor mentions (Google Alerts, Mention, Ahrefs or Brand24 alerts, or
  `/seo brands`).
- Ask the author to turn the mention into a link. Expect a low single-digit to
  low double-digit conversion rate.

## Disavow scope rules (additions to backlink-quality.md)

- Do not disavow as a precaution; Google ignores most spam on its own.
- Low authority alone is not toxic.
- Prefer `domain:` lines; use a URL line only when one page on an otherwise
  fine site is the problem.
- Do not resubmit domains already in the existing file; download the current
  file first and append.
- Expect effects to take months, not days, as Google recrawls the linking pages.
- Submit through the Search Console disavow links tool for the property.

## Manual action recovery (unnatural links)

1. Export the full link list from Search Console (Links report) plus any
   third-party index you have.
2. Audit each linking domain: toxic, acceptable, or unsure.
3. Ask webmasters to remove toxic links first, and log every attempt (date,
   contact, reply).
4. Disavow what you could not remove.
5. File a reconsideration request (Search Console, Manual actions): what you
   found, what you removed or disavowed, and what changed so it will not recur.
6. Reviews typically take weeks. If rejected, clean up more aggressively and
   resubmit with fuller documentation.

## Internal equity hand-off

Orphan pages, nofollow on internal links, and click depth are internal-link
issues. Route them to `/seo links` (runs `agentic/internal_links.py`). For
internal anchor diversity run
`"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run agentic/anchor_text_audit.py <url> --json`.
