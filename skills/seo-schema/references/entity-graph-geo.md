# Entity Graph & GEO Schema Properties

Load on demand from the `seo-schema` skill when an audit or generation task
covers entity recognition (AI search, Knowledge Graph, sameAs) rather than only
Google rich-result eligibility.

Structured data is how machines learn what an entity IS and how it connects to
other entities. A complete, consistent entity graph helps search engines and AI
systems identify the brand or author. Do not claim a confirmed AI-citation
uplift from schema without a cited primary source (see
`${CLAUDE_PLUGIN_ROOT}/skills/seo/references/schema-types.md`).

## Recommended Properties Beyond the Minimum

| Type | Add for entity clarity |
|---|---|
| Organization | `@id`, `description` (1-2 sentences), `foundingDate` (ISO 8601), `founder` (Person), `address`, `contactPoint` (telephone, email, contactType), `areaServed`, `numberOfEmployees` (QuantitativeValue), `award`, `knowsAbout` (3+ topics), full `sameAs`; `logo` as ImageObject |
| LocalBusiness | `openingHoursSpecification`, `geo`, `priceRange`, `aggregateRating`, `review`, `hasMap` (map URL) |
| Article / BlogPosting / NewsArticle / TechArticle | `dateModified` (freshness), `author` as a full Person (not a name string), `publisher` with logo, `image`, `about` and `mentions` for topic entities |
| Person (author) | `url` (on-site author page), `sameAs` (LinkedIn, X, personal site, Google Scholar, ORCID), `jobTitle`, `worksFor`, `knowsAbout`, `alumniOf`, `award`, `description`, `image` |
| Product | `brand`, `sku` or `gtin`/`mpn`, `aggregateRating`, `review`, `category`, and `material`, `weight`, `width`, `height` where applicable |
| SoftwareApplication | `applicationCategory`, `operatingSystem`, `offers`, `aggregateRating`, `featureList`, `screenshot`, `softwareVersion`, `releaseNotes` |
| Any entity | `identifier` for official IDs (DUNS, LEI, stock ticker) |

Use Person as a standalone schema on About/Bio pages for personal brands,
authors and thought leaders (or ProfilePage with `mainEntity` Person).

## sameAs Strategy

`sameAs` tells machines that the entity on this site is the same entity as the
listed profiles elsewhere. Recommended links, in priority order:

1. Wikipedia article
2. Wikidata item (`https://www.wikidata.org/wiki/Q...`)
3. LinkedIn (company page or personal profile)
4. YouTube channel
5. X / Twitter profile
6. Facebook page
7. Crunchbase (startups, tech)
8. GitHub (tech)
9. Google Scholar (researchers)
10. ORCID (academics)
11. Instagram
12. Apple App Store / Google Play listings (software)
13. BBB listing (US businesses)
14. Relevant industry directories

### sameAs Audit Process
1. Collect all known web presences for the entity
2. Check that each URL resolves (not 404, not redirected elsewhere)
3. Verify the Organization/Person schema includes all of them
4. Check that name, description and founding date are consistent across platforms
5. Flag platforms where the entity should have a presence but does not

Automated check: `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run agentic/entity_checker.py <url> --json`
(entity presence, sameAs, Knowledge Graph; `--kg-api-key` optional).

## speakable (beta)

`speakable` (SpeakableSpecification with `cssSelector` or `xpath`) marks
passages suited to text-to-speech on Article or WebPage. Google still labels it
beta and subject to change; recommend it only as optional, never as a ranking
or citation lever.

```json
{
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", "#key-takeaway"]
  }
}
```

## Entity Graph Scoring Rubric (0-100, optional)

Use alongside the rich-result validation table when the user asks for an
entity or AI-discoverability score. This is a heuristic, not a Google signal.

| Criterion | Points | How to score |
|---|---|---|
| Organization/Person schema present and complete | 15 | 15 full, 10 basic, 0 none |
| sameAs links | 15 | 3 per valid link, max 15 |
| Article schema with author details | 10 | 10 full Person, 5 name only, 0 none |
| Business-type-specific schema present | 10 | 10 complete, 5 partial, 0 missing |
| WebSite schema on homepage | 5 | 5 present, 0 not |
| BreadcrumbList on inner pages | 5 | 5 present, 0 not |
| JSON-LD format (not Microdata/RDFa) | 5 | 5 JSON-LD, 3 mixed, 0 Microdata/RDFa only |
| Server-rendered (not JS-injected) | 10 | 10 in HTML source, 5 JS in head, 0 dynamic JS |
| speakable on articles (optional, beta) | 5 | 5 present, 0 not |
| Valid JSON + valid Schema.org types | 10 | 10 no errors, 5 minor, 0 major |
| `knowsAbout` on Organization/Person | 5 | 5 with 3+ topics, 0 missing |
| No deprecated types present | 5 | 5 clean, 0 deprecated found |

## Organization Template with Full Entity Signals

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png",
    "width": 600,
    "height": 60
  },
  "description": "Concise description of what the company does.",
  "foundingDate": "2020-01-15",
  "founder": {
    "@type": "Person",
    "name": "Founder Name",
    "sameAs": "https://www.linkedin.com/in/founder"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service",
    "email": "support@example.com"
  },
  "sameAs": [
    "https://en.wikipedia.org/wiki/Company_Name",
    "https://www.wikidata.org/wiki/Q12345",
    "https://www.linkedin.com/company/company-name",
    "https://www.youtube.com/@companyname",
    "https://github.com/companyname",
    "https://www.crunchbase.com/organization/company-name"
  ],
  "knowsAbout": ["Topic 1", "Topic 2", "Topic 3"]
}
```
