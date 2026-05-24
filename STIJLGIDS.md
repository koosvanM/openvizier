# Gamma-stijl sjabloon voor Het Open Vizier

Elk artikel volgt dit slide-patroon. Gebruik dezelfde HTML-structuur als nl/editie-1/voorwoord.html.

## Slide-types beschikbaar in CSS

1. **slide slide--split** — hero met tekst links + beeld rechts (artikel-illustratie)
2. **slide slide--split slide--split-reverse** — beeld links + tekst rechts
3. **slide** (standaard) — full-width met grid-2, grid-3, steps, stat-row, timeline, dossier-card
4. **discussion** — discussievak (Giscus)

## Vaste elementen per artikel

- Top-band, masthead, nav
- Slide 1: HERO (split) — tag + slide__title + slide__lead + slide__meta + illustratie
- Slide 2-N: inhoudsslides — afwisseling van layouts
- Discussion-sectie met Giscus
- Article-nav (vorige/volgende)
- Footer

## Componenten

- `<span class="slide__tag">KICKER</span>` — kleine label bovenaan
- `<h2 class="slide__heading">Titel</h2>` — sectiekop
- `<p class="slide__lead">...</p>` — lead-paragraaf, groter
- `<p class="slide__body">...</p>` — body-tekst
- `<div class="callout"><h3>...</h3><p>...</p></div>` — donkerblauw kader voor citaten/highlights
- `<div class="grid-2/3">...</div>` met `<div>` of `<div class="dossier-card">` items
- `<div class="steps"><div class="step"><div class="step__num">01</div><div class="step__title">...</div><div class="step__desc">...</div></div></div>`
- `<div class="stat-row"><div><div class="stat__number">...</div><div class="stat__label">...</div><div class="stat__desc">...</div></div></div>` — drie grote cijfers
- `<div class="timeline"><div class="timeline__phase"><div class="timeline__num">1</div><div class="timeline__title">...</div><div class="timeline__period">0-12 mnd</div><div class="timeline__desc">...</div></div></div>` — fase-tijdlijn
- `<table class="dossier-table">` — risico-tabel of vergelijking

## Stijl-richtlijnen

- Italic in titel via `<em>...</em>` voor sleutelwoord (bv. "Drie *dimensies* zijn te weinig")
- Niet meer dan 5-7 slides per artikel
- Variatie tussen layouts (niet allemaal hetzelfde)
- Discussion-sectie en article-nav identiek aan voorwoord.html
- Compacte spacing (zoals nu in CSS)
