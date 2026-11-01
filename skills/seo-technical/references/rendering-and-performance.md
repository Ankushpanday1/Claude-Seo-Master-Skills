# Rendering, Security Headers & Performance Detail

Load on demand from `seo-technical`. Thresholds for CWV bands live in
`${CLAUDE_PLUGIN_ROOT}/skills/seo/references/cwv-thresholds.md`.

## Security Header Expected Values

| Header | Expected value | Protects against |
|--------|----------------|------------------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Protocol downgrade |
| `Content-Security-Policy` | Any valid policy restricting sources | XSS |
| `X-Content-Type-Options` | `nosniff` | MIME sniffing |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` (or CSP `frame-ancestors`) | Clickjacking |
| `Referrer-Policy` | `strict-origin-when-cross-origin` or stricter | Referrer leakage |
| `Permissions-Policy` | Restricts unused browser features | Feature abuse |

Severity guide: no HTTPS is Critical; missing HSTS or CSP is Medium; the other
headers are Low. HTTPS is a lightweight ranking signal, so do not let header
gaps outweigh crawl or content problems.

## SSR / CSR Detection

1. Fetch without JavaScript (`fetch_page.py` or `curl -s <url>`) to get raw HTML.
2. Render with Playwright (`render_page.py <url> --mode always --json`, network idle).
3. Compare: `<title>`, meta description, H1, canonical, JSON-LD, main body
   text, navigation and internal links.

| Result | Severity | Action |
|--------|----------|--------|
| Body essentially empty without JS | Critical | Move to SSR or SSG |
| Critical SEO elements JS-only | Critical | Server-render head tags and content |
| Main content present, nav/sections JS-only | High | Server-render navigation and links |
| Secondary or interactive parts JS-only | Medium | Acceptable; confirm links are real `<a href>` |
| Everything present in raw HTML | Pass | None |

CSR signals: a single root node (`<div id="root">`, `<div id="app">`,
`<app-root>`), large `main.js`/`bundle.js` with an empty body, content fetched
by inline `fetch`/XHR calls. SSR signals: `__NEXT_DATA__`, `__NUXT__` or
`__NUXT_DATA__`, `data-reactroot`, `data-server-rendered`, substantial text in
`<body>` before any script runs.

Framework fixes: React to Next.js or React Router v7; Vue to Nuxt; Angular to
Angular SSR; Svelte to SvelteKit; content sites to Astro or another SSG.
Prerendering services are a form of dynamic rendering: technical debt, not a
target state.

## CWV Risk Indicators (no field data)

Static source analysis estimates risk only; always say that field data from
CrUX or PSI is required for a measurement. Rate each vital Low (few
indicators), Medium (some), High (several).

**LCP:** hero image lazy-loaded or missing `fetchpriority="high"`; stylesheets
without `media` and scripts without `async`/`defer` in `<head>`; web fonts
without `font-display: swap` or `optional`; no `preload` for the LCP resource;
TTFB over 800ms.

**INP:** large synchronous script bundles in `<head>`; many synchronous
third-party tags (analytics, ads, widgets); deep or very large DOM (over 1,500
elements); heavy inline event handlers.

**CLS:** images, iframes, or embeds without `width`/`height` or
`aspect-ratio`; ad slots or banners injected above existing content; fonts
without `font-display`.

## Common Fixes

| Vital | Fix |
|-------|-----|
| LCP | WebP/AVIF hero at the right size, `preload` plus `fetchpriority="high"` |
| LCP | Cut TTFB (edge CDN, server caching, fewer redirects) |
| LCP | Remove render-blocking CSS/JS (inline critical CSS, `defer`) |
| LCP | `preconnect` to critical third-party origins |
| INP | Break long tasks (over 50ms) with `scheduler.yield()` or `requestIdleCallback` |
| INP | Debounce/throttle scroll and resize handlers; use `requestAnimationFrame` for visual updates |
| INP | Defer third-party scripts or move them to a web worker |
| INP | `content-visibility: auto` on below-fold sections; `will-change` only on animated elements |
| INP | Replace synchronous XHR and heavy `localStorage` work with async APIs |
| CLS | Explicit `width`/`height` on media; reserve ad and embed space with `min-height` or `aspect-ratio` |
| CLS | `font-display: swap` with `size-adjust` fallback fonts |
| CLS | Never insert content above existing content after load |

## Server Performance Thresholds

| Check | Target | Warning | Critical |
|-------|--------|---------|----------|
| TTFB | 800ms or less (ideally under 200ms) | over 800ms | over 1,800ms (web.dev "poor") |
| Total page weight | under 1MB on critical templates | over 2MB | n/a |
| JS bundle (compressed) | under 200KB | over 200KB | over 500KB |
| Static asset cache | `max-age=31536000` with hashed names | short or missing `max-age` | n/a |
| Compression | brotli or gzip | missing on some assets | missing on HTML |

Font loading detail: `"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" run agentic/font_audit.py <url> --json`.
