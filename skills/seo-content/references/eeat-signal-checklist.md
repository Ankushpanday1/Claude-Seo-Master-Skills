# E-E-A-T Signal Checklist & Content Rubrics

Load on demand from the `seo-content` skill when scoring E-E-A-T sub-factors,
AI-content quality, freshness, or topical authority in detail. Scores stay on
this skill's own weights (Experience 20, Expertise 25, Authoritativeness 25,
Trust 30): Google publishes no numeric E-E-A-T weights, only that trust is most
important. These are heuristics, not Google-internal signals.

## Signal Checklist per Factor

Score each signal Strong / Partial / Absent, then map to the factor's maximum.

### Experience (max 20)
| Signal | Strong | Partial |
|---|---|---|
| First-person accounts ("I tested...", "We implemented...") | specific | generic |
| Original research or data not available elsewhere | original data | cites original work |
| Case studies with specific results | numbers, timelines | general |
| Screenshots, photos, artifacts of direct use | authentic | stock/generic |
| Specific examples (names, dates, places, figures) | unique | somewhat specific |
| Process demonstrated, not only the outcome | step-by-step from experience | partial |
| Before/after comparisons with metrics | real metrics | illustrative |
| Failures and lessons learned discussed | present | n/a |

Weak-Experience flags: only summarizes other sources; advice that fits any
situation ("it depends on your needs"); no actual usage or testing; hedging
that implies no direct knowledge ("reportedly", "supposedly", "some say").

### Expertise (max 25)
| Signal | Strong | Partial |
|---|---|---|
| Visible author byline and credentials (degrees, certifications) | full credentials | basic bio |
| Dedicated author page with professional background | dedicated page | brief bio |
| Technical depth appropriate to the topic | thorough | adequate |
| Methodology explained (how conclusions were reached) | clear | some |
| Data-backed claims citing primary sources (not other blogs) | well-sourced | some data |
| Industry terminology used correctly, jargon defined on first use | accurate | basic |
| Edge cases, caveats and limitations addressed | present | partial |
| Person schema for the author; author findable on LinkedIn, industry sites, conferences | both | one |

Weak-Expertise flags: unsupported claims; surface treatment of complex topics;
misused terminology; no author or author without relevant credentials.

### Authoritativeness (max 25)
| Signal | Strong | Partial |
|---|---|---|
| Inbound citations / links from authoritative sources | major sources | some |
| Author or brand quoted in press or media | media | industry mentions |
| Industry awards, certifications, professional memberships | relevant | tangential |
| Speaker credentials (conferences, events) | listed | n/a |
| Published in peer-reviewed or respected outlets | tier-1 | industry outlets |
| Comprehensive topical coverage on the site | thorough | some |
| Wikipedia / encyclopedic reference, Knowledge Panel | Wikipedia or KP | other references |
| About page with history, team, mission; institutional backing | comprehensive | basic |
| Organization `sameAs` to authoritative profiles | present | partial |

Weak-Authoritativeness flags: isolated pages with no topical depth; no external
validation; self-proclaimed "expert" without evidence.

### Trustworthiness (max 30)
| Signal | Strong | Partial |
|---|---|---|
| Contact info (address, phone, email) | full | email only |
| Privacy policy and terms of service | both | one |
| HTTPS with a valid certificate | valid | n/a |
| Editorial standards or corrections policy | documented | implicit |
| Business model, affiliate and sponsorship disclosures | clear | some |
| Reviews/testimonials from real customers | verified, third-party | testimonials only |
| Claims accurate, sources cited inline | all | mostly |
| Clear site ownership | clear | n/a |
| Publish and last-updated dates visible | both | one |
| No deceptive practices (hidden content, misleading headlines) | clean | n/a |

Weak-Trust flags: no contact path for corrections; missing privacy policy;
undisclosed affiliate or sponsored content; verifiably false claims.

## AI-Content Quality Signals

Detection is imprecise: describe the signals observed and give a likelihood,
never a definitive "this is AI" claim.

| Low-quality signal | What it looks like |
|---|---|
| Generic phrasing | "In today's fast-paced world...", "It's important to note that...", "delve into" |
| Lack of specifics | Statements that fit any company, no names, dates, numbers |
| Perfect but empty structure | Well-formatted headings with shallow content beneath |
| Hedging overload | "may", "might", "it depends" without ever taking a position or naming the factors |
| Missing human voice | No opinions, preferences or professional judgment |
| Repetitive conclusions | Each section restates the same thesis |
| Filler | Paragraphs that could be deleted without losing information |
| Listicle-heavy shallow coverage; stock transitions | "In this article", "Let's dive in" |
| Unnatural keyword repetition | Stuffing patterns typical of SEO-only generation |

High-quality signals (regardless of production method): original data
(surveys, experiments, benchmarks); named, specific examples; contrarian or
nuanced views backed by reasoning; first-person experience; current references;
clear expert opinion; specific actionable recommendations; acknowledged
trade-offs ("works for X but not Y because...").

Likelihood labels: Highly Likely Human / Likely Human-Edited AI / Likely AI with
Light Editing / Likely Unedited AI.

## Freshness Tiers

| Last update | Status |
|---|---|
| Within 3 months | Excellent |
| Within 6 months | Good |
| Within 12 months | Acceptable, may need refresh |
| 12-24 months | Warning, review for accuracy |
| No date, or 24+ months | Critical for time-sensitive topics |

Dates must be specific ("January 15, 2026", not "recently") and match
`datePublished` / `dateModified` in structured data. Weight freshness higher for
YMYL (health, finance, legal, safety) and fast-moving topics.

Treat a page as **evergreen** (age matters less) when it covers fundamentals
that do not change, is clearly a reference guide, and contains no
time-dependent claims ("the latest", "currently", "in 2024").

## Topical Authority (site-level modifier)

Assess from the target page, its internal links and navigation; a full audit
needs a crawl. Check breadth (related pages), depth (subtopic pages), clustering
(pillar-cluster or hub-and-spoke with internal links), content gaps versus
competitors, and topic coverage ratio (share of expected subtopics covered).

| Level | Description | Modifier |
|---|---|---|
| Authority | 20+ pages covering the topic, strong clustering | +10 |
| Developing | 10-20 pages, some clustering | +5 |
| Emerging | 5-10 pages, limited clustering | 0 |
| Thin | under 5 pages, no clustering | -5 |

Apply the modifier to the Content Quality Score, capped at 100, and report it
on its own line so the base score stays visible.
