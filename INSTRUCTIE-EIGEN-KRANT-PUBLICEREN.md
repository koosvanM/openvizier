# Instructie voor "Eigen Krant Publiceren"

Datum: 2 juli 2026
Van: Computer (namens Jacobus)

## Wat er is gebeurd

Drie pagina's op openvizier.org waren stuk:
- `nl/stemgedrag.html`
- `en/vote-impact.html`
- `de/wahlfolgen.html`

Symptomen: het bovenmenu stond als opsomming onder elkaar, en de pagina laadde traag omdat de zware iframe-app (React/Vite chunks: PersonaFlow 685 KB, pdf 393 KB, button 537 KB) direct al bij het openen van de pagina werd opgehaald.

## Wat Computer heeft opgelost

1. **CSS-fout** — De pagina's linkten naar een niet-bestaand `./_shared.css` (404). Vervangen door `../assets/style.css` (de bestaande huisstijl).
2. **Paginaspecifieke stijlen** (masthead-row, langswitch, datumregel, formule-blok, landen-tegels, footer) staan nu inline in de `<style>`-blok van elk van de drie pagina's — geen extern `_shared.css` meer nodig.
3. **Iframe verwijderd**. In plaats daarvan staat er onderaan een **tegel-raster met de landen** (Nederland / Deutschland / Malta). Elke tegel linkt naar de bijbehorende app (`stemgedrag-app/`, `wahlfolgen-app/`, `vote-impact-app/`). De zware app-chunks worden pas geladen als iemand een tegel klikt — dus de pagina laadt nu binnen seconden.
4. **Landen zijn uitbreidbaar**. In het `<div class="landen__grid">` blok kun je gewoon extra `<a class="land-tegel">…</a>` toevoegen — één per nieuw land.

## Wat "Eigen Krant Publiceren" moet doen

Op elk van de drie pagina's staat op de plek waar het bovenmenu hoort een placeholder-comment:

```html
<!-- NAV_MENU: bovenmenu wordt gegenereerd door "Eigen Krant Publiceren" — niet met de hand invullen -->
```

**Vervang deze comment door het huidige, actuele bovenmenu** (dezelfde `<nav class="nav">…</nav>` structuur die op de andere openvizier-pagina's staat, met de meest recente edities en menu-items). De klasse `.nav` / `.nav__inner` / `.nav__links` bestaat al in `assets/style.css`, dus zolang je die klassen gebruikt is het menu automatisch horizontaal gestyled.

## Structuur waar het menu weer moet komen (per pagina)

### nl/stemgedrag.html
Volgorde:
1. `<header class="masthead">` met langswitch (NL/EN/DE) — **blijft staan**
2. **[Hier het bovenmenu invullen]** ← placeholder-comment vervangen
3. `<article>` met de artikeltekst — **blijft staan**
4. `<section class="landen">` met landen-tegels — **blijft staan**
5. `<footer>` — **blijft staan**

Idem voor `en/vote-impact.html` en `de/wahlfolgen.html`, elk in de eigen taal.

## Actieve link markeren

Als je de landspagina's in het menu opneemt, markeer dan de actieve pagina met `class="active"`:
- Op `nl/stemgedrag.html`: `<li><a href="/nl/stemgedrag" class="active">Stemgedrag</a></li>`
- Op `en/vote-impact.html`: `<li><a href="/en/vote-impact" class="active">Vote Impact</a></li>`
- Op `de/wahlfolgen.html`: `<li><a href="/de/wahlfolgen" class="active">Wahlfolgen</a></li>`

## Bestandslocaties in repo

- Repo: `github.com/koosvanM/openvizier`
- Branch: `main` (Netlify auto-deploy)
- Bestanden: `nl/stemgedrag.html`, `en/vote-impact.html`, `de/wahlfolgen.html`
