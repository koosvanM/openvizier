#!/usr/bin/env python3
"""
Herbouw verkennen.html in alle 8 talen zodat hij in het reguliere Open Vizier-design
past: zelfde masthead, menu, en footer als de andere pagina's. De interactieve
verkenner-canvas wordt ingebed in een normaal pagina-frame.

Aanpak:
- Top-band + masthead + nav (canoniek, taalspecifiek)
- Main met inleidende paragraaf
- Embedded verkenner-canvas (max-width:1200px, hoogte:75vh, donker thema binnen frame)
- Hint en reader behouden binnen frame
- JS uit /tmp/verkennen_script.js (hergebruikt)
- Footer (eenvoudige eindvoet)
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# Het bestaande JS-blok (uit nl/verkennen.html regel 224-720)
JS_PATH = Path("/tmp/verkennen_script.js")
JS_BLOK = JS_PATH.read_text(encoding="utf-8")

# Taalspecifieke teksten + menu
LANGS = {
    "nl": {
        "lang": "nl",
        "title": "Verkennen — Het Open Vizier",
        "meta_desc": "Visueel verkennen van de structuur van Het Open Vizier — klik door de lagen.",
        "topband_kop": "Gratis maandelijkse krant zonder reclame",
        "topband_link": "Schrijf u in zonder verplichting",
        "topband_href": "delen.html",
        "masthead_kicker": "Verkennen · juni 2026",
        "masthead_sub": "Een krant over denken zonder oogkleppen",
        "intro_h1": "Verkennen",
        "intro_lead": "Een visuele structuur van Het Open Vizier. Klik op een blok om dieper te gaan; klik op het centrum om terug te keren.",
        "hint": "Klik op een blok om dieper te gaan · klik op het centrum om terug",
        "loading": "structuur laden…",
        "reader_cta": "→ Lees het artikel",
        "reader_terug": "Terug",
        "footer_lead": "Het Open Vizier · onafhankelijke maandelijkse krant · Jacobus van Merksteijn · Malta · juni 2026",
        "footer_voorpagina": "Voorpagina",
        "menu_items": [
            ("./", "Voorpagina"),
            ("wat-opkomt/", "Wat opkomt"),
            ("verkennen.html", "Verkennen", "active"),
            ("editie-6/", "Editie 6"),
            ("editie-5/", "Editie 5"),
            ("editie-4/", "Editie 4"),
            ("editie-3/", "Editie 3"),
            ("editie-2/", "Editie 2"),
            ("editie-1/", "Editie 1"),
            ("editie-0/", "Editie Europa"),
            ("delen.html", "Delen"),
        ],
        "lang_label": "⌂ Taal",
    },
    "de": {
        "lang": "de",
        "title": "Erkunden — Het Open Vizier",
        "meta_desc": "Visuelles Erkunden der Struktur von Het Open Vizier — klicken Sie sich durch die Schichten.",
        "topband_kop": "Kostenlose monatliche Zeitung ohne Werbung",
        "topband_link": "Jetzt unverbindlich anmelden",
        "topband_href": "teilen.html",
        "masthead_kicker": "Erkunden · Juni 2026",
        "masthead_sub": "Eine Zeitung über das Denken ohne Scheuklappen",
        "intro_h1": "Erkunden",
        "intro_lead": "Eine visuelle Struktur von Het Open Vizier. Klicken Sie auf einen Block, um tiefer zu gehen; klicken Sie auf das Zentrum, um zurückzukehren.",
        "hint": "Auf einen Block klicken, um tiefer zu gehen · auf das Zentrum klicken, um zurückzukehren",
        "loading": "Struktur wird geladen…",
        "reader_cta": "→ Den Artikel lesen",
        "reader_terug": "Zurück",
        "footer_lead": "Het Open Vizier · unabhängige Monatszeitung · Jacobus van Merksteijn · Malta · Juni 2026",
        "footer_voorpagina": "Startseite",
        "menu_items": [
            ("./", "Startseite"),
            ("was-aufkommt/", "Was aufkommt"),
            ("verkennen.html", "Erkunden", "active"),
            ("ausgabe-6/", "Ausgabe 6"),
            ("ausgabe-5/", "Ausgabe 5"),
            ("ausgabe-4/", "Ausgabe 4"),
            ("ausgabe-3/", "Ausgabe 3"),
            ("ausgabe-2/", "Ausgabe 2"),
            ("ausgabe-1/", "Ausgabe 1"),
            ("ausgabe-0/", "Ausgabe Europa"),
            ("teilen.html", "Teilen"),
        ],
        "lang_label": "⌂ Sprache",
    },
    "en": {
        "lang": "en",
        "title": "Explore — The Open Visor",
        "meta_desc": "Visual exploration of the structure of The Open Visor — click through the layers.",
        "topband_kop": "Free monthly newspaper without advertising",
        "topband_link": "Subscribe without obligation",
        "topband_href": "share.html",
        "masthead_kicker": "Explore · June 2026",
        "masthead_sub": "A newspaper about thinking without blinkers",
        "intro_h1": "Explore",
        "intro_lead": "A visual structure of The Open Visor. Click on a block to go deeper; click on the centre to return.",
        "hint": "Click on a block to go deeper · click on the centre to return",
        "loading": "loading structure…",
        "reader_cta": "→ Read the article",
        "reader_terug": "Back",
        "footer_lead": "The Open Visor · independent monthly newspaper · Jacobus van Merksteijn · Malta · June 2026",
        "footer_voorpagina": "Home",
        "menu_items": [
            ("./", "Home"),
            ("what-surfaces/", "What surfaces"),
            ("verkennen.html", "Explore", "active"),
            ("edition-6/", "Edition 6"),
            ("edition-5/", "Edition 5"),
            ("edition-4/", "Edition 4"),
            ("edition-3/", "Edition 3"),
            ("edition-2/", "Edition 2"),
            ("edition-1/", "Edition 1"),
            ("edition-0/", "Edition Europe"),
            ("share.html", "Share"),
        ],
        "lang_label": "⌂ Language",
    },
    "ru": {
        "lang": "ru",
        "title": "Исследовать — Открытое забрало",
        "meta_desc": "Визуальное исследование структуры «Открытого забрала» — пройдите по слоям.",
        "topband_kop": "Бесплатная ежемесячная газета без рекламы",
        "topband_link": "Подпишитесь без обязательств",
        "topband_href": "podelitsya.html",
        "masthead_kicker": "Исследовать · июнь 2026",
        "masthead_sub": "Газета о мышлении без шор",
        "intro_h1": "Исследовать",
        "intro_lead": "Визуальная структура «Открытого забрала». Нажмите на блок, чтобы углубиться; нажмите на центр, чтобы вернуться.",
        "hint": "Нажмите на блок, чтобы углубиться · нажмите на центр, чтобы вернуться",
        "loading": "структура загружается…",
        "reader_cta": "→ Читать статью",
        "reader_terug": "Назад",
        "footer_lead": "Открытое забрало · независимая ежемесячная газета · Jacobus van Merksteijn · Мальта · июнь 2026",
        "footer_voorpagina": "Главная",
        "menu_items": [
            ("./", "Главная"),
            ("chto-vsplyvaet/", "Что всплывает"),
            ("verkennen.html", "Исследовать", "active"),
            ("vypusk-6/", "Выпуск 6"),
            ("vypusk-5/", "Выпуск 5"),
            ("vypusk-4/", "Выпуск 4"),
            ("vypusk-3/", "Выпуск 3"),
            ("vypusk-2/", "Выпуск 2"),
            ("vypusk-1/", "Выпуск 1"),
            ("vypusk-0/", "Выпуск Европа"),
            ("podelitsya.html", "Поделиться"),
        ],
        "lang_label": "⌂ Язык",
    },
    # ES/FR/IT/PT: kort menu (alleen Brussel-laag)
    "es": {
        "lang": "es",
        "title": "Explorar — Het Open Vizier",
        "meta_desc": "Exploración visual de la estructura de Het Open Vizier — recorra las capas.",
        "topband_kop": "Periódico mensual gratuito sin publicidad",
        "topband_link": "Suscríbase sin compromiso",
        "topband_href": "share.html",
        "masthead_kicker": "Explorar · junio 2026",
        "masthead_sub": "Un periódico para pensar sin anteojeras",
        "intro_h1": "Explorar",
        "intro_lead": "Una estructura visual de Het Open Vizier. Haga clic en un bloque para profundizar; haga clic en el centro para volver.",
        "hint": "Haga clic en un bloque para profundizar · haga clic en el centro para volver",
        "loading": "cargando estructura…",
        "reader_cta": "→ Leer el artículo",
        "reader_terug": "Atrás",
        "footer_lead": "Het Open Vizier · periódico mensual independiente · Jacobus van Merksteijn · Malta · junio 2026",
        "footer_voorpagina": "Inicio",
        "menu_items": [
            ("./", "Inicio"),
            ("edicion-0/", "Edición Europa"),
            ("lo-que-emerge/", "Lo que emerge"),
            ("verkennen.html", "Explorar", "active"),
        ],
        "lang_label": "⌂ Idioma",
        "lang_link": "index-talenring.html",
    },
    "fr": {
        "lang": "fr",
        "title": "Explorer — Het Open Vizier",
        "meta_desc": "Exploration visuelle de la structure de Het Open Vizier — parcourez les couches.",
        "topband_kop": "Journal mensuel gratuit sans publicité",
        "topband_link": "Abonnez-vous sans engagement",
        "topband_href": "share.html",
        "masthead_kicker": "Explorer · juin 2026",
        "masthead_sub": "Un journal pour penser sans œillères",
        "intro_h1": "Explorer",
        "intro_lead": "Une structure visuelle de Het Open Vizier. Cliquez sur un bloc pour aller plus profond ; cliquez au centre pour revenir.",
        "hint": "Cliquez sur un bloc pour aller plus profond · cliquez au centre pour revenir",
        "loading": "chargement de la structure…",
        "reader_cta": "→ Lire l'article",
        "reader_terug": "Retour",
        "footer_lead": "Het Open Vizier · journal mensuel indépendant · Jacobus van Merksteijn · Malte · juin 2026",
        "footer_voorpagina": "Accueil",
        "menu_items": [
            ("./", "Accueil"),
            ("edition-0/", "Édition Europe"),
            ("ce-qui-emerge/", "Ce qui émerge"),
            ("verkennen.html", "Explorer", "active"),
        ],
        "lang_label": "⌂ Langue",
        "lang_link": "index-talenring.html",
    },
    "it": {
        "lang": "it",
        "title": "Esplorare — Het Open Vizier",
        "meta_desc": "Esplorazione visiva della struttura di Het Open Vizier — attraversa gli strati.",
        "topband_kop": "Giornale mensile gratuito senza pubblicità",
        "topband_link": "Iscriviti senza impegno",
        "topband_href": "share.html",
        "masthead_kicker": "Esplorare · giugno 2026",
        "masthead_sub": "Un giornale per pensare senza paraocchi",
        "intro_h1": "Esplorare",
        "intro_lead": "Una struttura visiva di Het Open Vizier. Fai clic su un blocco per andare più in profondità; fai clic al centro per tornare.",
        "hint": "Fai clic su un blocco per andare più in profondità · fai clic al centro per tornare",
        "loading": "caricamento struttura…",
        "reader_cta": "→ Leggi l'articolo",
        "reader_terug": "Indietro",
        "footer_lead": "Het Open Vizier · giornale mensile indipendente · Jacobus van Merksteijn · Malta · giugno 2026",
        "footer_voorpagina": "Home",
        "menu_items": [
            ("./", "Home"),
            ("edizione-0/", "Edizione Europa"),
            ("cio-che-emerge/", "Ciò che emerge"),
            ("verkennen.html", "Esplorare", "active"),
        ],
        "lang_label": "⌂ Lingua",
        "lang_link": "index-talenring.html",
    },
    "pt": {
        "lang": "pt",
        "title": "Explorar — Het Open Vizier",
        "meta_desc": "Exploração visual da estrutura de Het Open Vizier — percorra as camadas.",
        "topband_kop": "Jornal mensal gratuito sem publicidade",
        "topband_link": "Inscreva-se sem compromisso",
        "topband_href": "share.html",
        "masthead_kicker": "Explorar · junho 2026",
        "masthead_sub": "Um jornal para pensar sem antolhos",
        "intro_h1": "Explorar",
        "intro_lead": "Uma estrutura visual de Het Open Vizier. Clique num bloco para ir mais fundo; clique no centro para voltar.",
        "hint": "Clique num bloco para ir mais fundo · clique no centro para voltar",
        "loading": "a carregar estrutura…",
        "reader_cta": "→ Ler o artigo",
        "reader_terug": "Voltar",
        "footer_lead": "Het Open Vizier · jornal mensal independente · Jacobus van Merksteijn · Malta · junho 2026",
        "footer_voorpagina": "Início",
        "menu_items": [
            ("./", "Início"),
            ("edicao-0/", "Edição Europa"),
            ("o-que-emerge/", "O que emerge"),
            ("verkennen.html", "Explorar", "active"),
        ],
        "lang_label": "⌂ Idioma",
        "lang_link": "index-talenring.html",
    },
}

def menu_html(t):
    items = []
    for item in t["menu_items"]:
        if len(item) == 3:
            href, label, cls = item
            items.append(f'      <li><a href="{href}" class="{cls}">{label}</a></li>')
        else:
            href, label = item
            items.append(f'      <li><a href="{href}">{label}</a></li>')
    # Talenkeuze-link verschilt per taalstijl
    if "lang_link" in t:
        lang_href = t["lang_link"]
    else:
        lang_href = "/"
    return f'''<nav class="nav">
  <div class="nav__inner">
    <ul class="nav__links">
{chr(10).join(items)}
    </ul>
    <div class="nav__lang">
      <a href="{lang_href}" title="{t["lang_label"]}" style="color:#1c5760;">{t["lang_label"]}</a>
    </div>
  </div>
</nav>'''


def build_page(t):
    return f"""<!DOCTYPE html>
<html lang="{t["lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t["title"]}</title>
<meta name="description" content="{t["meta_desc"]}">
<link rel="stylesheet" href="../assets/style.css">
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
<style>
  body {{ background:#faf8f3; color:#1a1a1a; margin:0; font-family: Georgia, serif; }}
  .top-band {{ background:#1c5760; color:#f5f0e6; text-align:center; padding:0.6rem 1rem; font-size:0.9rem; }}
  .top-band a {{ color:#ffd700; font-weight:700; text-decoration:underline; }}
  .masthead {{ text-align:center; padding:2rem 1.5rem 0.8rem; }}
  .masthead__kicker {{ font-size:0.78rem; letter-spacing:0.15em; text-transform:uppercase; color:#1c5760; margin:0 0 0.6rem 0; font-weight:600; }}
  .masthead__logo {{ display:inline-block; font-family:Georgia,serif; font-style:italic; font-weight:700; font-size:clamp(2rem,4.5vw,3rem); color:#1a1a1a; text-decoration:none; }}
  .masthead__sub {{ font-family:Georgia,serif; font-style:italic; color:#4a5263; margin:0.4rem 0 0; font-size:1.05rem; }}

  main.verkennen-main {{ max-width:1200px; margin:0 auto; padding:2rem 1.5rem 3rem; }}
  .verkennen-intro {{ text-align:center; margin-bottom:2rem; }}
  .verkennen-intro h1 {{ font-family:Georgia,serif; font-size:clamp(2rem,4vw,2.8rem); margin:0 0 0.8rem; color:#1a1a1a; font-weight:700; }}
  .verkennen-intro p {{ font-family:Georgia,serif; font-style:italic; color:#4a5263; max-width:700px; margin:0 auto; line-height:1.55; font-size:1.05rem; }}

  /* Verkenner-canvas — ingebed in pagina, niet langer fullscreen */
  .verkennen-canvas {{
    position:relative;
    width:100%;
    height:75vh;
    min-height:560px;
    max-height:820px;
    background:#2e2519;
    color:#f6f1e6;
    border-radius:8px;
    overflow:hidden;
    box-shadow:0 8px 30px rgba(0,0,0,0.20);
    font-family:Georgia,"Times New Roman",serif;
  }}

  /* Stage (grid van blokken) — binnen frame */
  .verkennen-canvas .stage {{
    position:absolute; inset:0; display:grid; gap:0;
    background:#2e2519; overflow:hidden;
  }}

  /* Tile-styling — gekopieerd uit oude verkennen.html */
  .verkennen-canvas .tile {{ position:relative; overflow:hidden; cursor:pointer;
    display:flex; align-items:center; justify-content:center; transition:opacity .5s ease; }}
  .verkennen-canvas .tile.concept,
  .verkennen-canvas .tile.onbereikbaar {{ cursor:default; }}
  .verkennen-canvas .tile.concept .bg,
  .verkennen-canvas .tile.onbereikbaar .bg {{
    filter:sepia(.55) brightness(.50) contrast(1.05) saturate(.35);
  }}
  .verkennen-canvas .tile.concept:hover .bg,
  .verkennen-canvas .tile.onbereikbaar:hover .bg {{
    filter:sepia(.55) brightness(.50) contrast(1.05) saturate(.35);
  }}
  .verkennen-canvas .tile.concept .label::after {{
    content:"binnenkort"; display:block; margin-top:.6em;
    font-size:.7em; font-style:italic; color:rgba(255,255,255,.55);
    letter-spacing:1.5px; text-transform:uppercase;
  }}
  .verkennen-canvas .tile.concept .label h2,
  .verkennen-canvas .tile.onbereikbaar .label h2 {{ opacity:.7; }}
  .verkennen-canvas .tile.vervolg {{ background:#1a1612; }}
  .verkennen-canvas .tile.vervolg .bg {{ display:none; }}
  .verkennen-canvas .tile.vervolg .veil {{ background:linear-gradient(135deg,rgba(40,32,22,.6) 0%,rgba(0,0,0,.4) 100%); }}
  .verkennen-canvas .tile.vervolg .label h2 {{ font-style:italic; letter-spacing:2px; opacity:.85; }}
  .verkennen-canvas .tile .bg {{ position:absolute; inset:-2%; background-size:cover;
    background-position:center; filter:sepia(.35) brightness(.85) contrast(1.05);
    transition:filter .4s ease, transform .8s ease; }}
  .verkennen-canvas .tile:hover .bg {{ filter:sepia(.25) brightness(.95) contrast(1.1); transform:scale(1.04); }}
  .verkennen-canvas .tile .veil {{ position:absolute; inset:0;
    background:linear-gradient(180deg,rgba(0,0,0,.10) 0%,rgba(0,0,0,.38) 100%);
    pointer-events:none; }}
  .verkennen-canvas .tile .label {{ position:relative; z-index:2; text-align:center; padding:1rem; max-width:90%; }}
  .verkennen-canvas .tile .label h2 {{ font-size:clamp(1rem,2.2vw,1.8rem); font-weight:700; line-height:1.1;
    color:#f7efdc; letter-spacing:.4px;
    text-shadow:0 2px 14px rgba(0,0,0,.55),0 0 2px rgba(0,0,0,.7); }}
  .verkennen-canvas .tile .label p {{ margin-top:.4em; font-size:clamp(.75rem,1vw,.95rem); font-style:italic;
    color:#e3d8bc; opacity:.92; text-shadow:0 1px 8px rgba(0,0,0,.6); }}
  .verkennen-canvas .tile.entering {{ opacity:0; animation:tileIn .6s cubic-bezier(.22,1,.36,1) forwards; }}
  @keyframes tileIn {{ from {{ opacity:0; transform:scale(1.04); }} to {{ opacity:1; transform:scale(1); }} }}

  /* Verkennen-controls: home-knop boven canvas */
  .verkennen-controls {{ display:flex; justify-content:space-between; align-items:center;
    margin:0 auto 0.8rem; padding:0 0.2rem; max-width:1200px; }}
  .verkennen-controls button#home {{ background:transparent; border:1px solid #c8d2bb;
    color:#1c5760; padding:0.4rem 0.9rem; border-radius:4px; cursor:pointer;
    font-family:Georgia,serif; font-size:0.9rem; letter-spacing:0.04em; display:none;
    align-items:center; gap:0.4rem; }}
  .verkennen-controls button#home.show {{ display:inline-flex; }}
  .verkennen-controls button#home:hover {{ background:#eef1e8; }}
  .verkennen-controls button#home svg {{ width:14px; height:14px; stroke:currentColor; fill:none; stroke-width:1.8; }}
  .verkennen-controls .topbar-title {{ font-family:Georgia,serif; font-style:italic; color:#4a5263; font-size:0.95rem; }}

  /* Loading-tekst binnen frame */
  .verkennen-canvas .loading {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
    color:rgba(231,222,193,.7); font-style:italic; z-index:1; }}

  /* Hint onderaan binnen frame */
  .verkennen-canvas .hint {{ position:absolute; bottom:14px; left:50%; transform:translateX(-50%);
    color:rgba(231,222,193,.55); font-size:12px; font-style:italic; letter-spacing:.3px;
    pointer-events:none; z-index:6; text-shadow:0 1px 4px rgba(0,0,0,.5); }}

  /* Reader-overlay — binnen frame, geen volledige scherm-overlay */
  .verkennen-canvas .reader {{ position:absolute; inset:0; background:rgba(20,16,12,.92);
    display:none; align-items:center; justify-content:center; flex-direction:column;
    padding:40px; text-align:center; z-index:20; }}
  .verkennen-canvas .reader.show {{ display:flex; }}
  .verkennen-canvas .reader h2 {{ font-size:clamp(1.5rem,2.6vw,2.2rem); margin-bottom:1rem; color:#f7efdc; }}
  .verkennen-canvas .reader p {{ max-width:600px; color:#cdc3a8; font-size:1rem; line-height:1.55; margin-bottom:1.4rem; }}
  .verkennen-canvas .reader a.read {{ background:#f7efdc; color:#1a1612; padding:11px 24px;
    text-decoration:none; border-radius:999px; font-size:15px; letter-spacing:.4px; transition:background .2s; }}
  .verkennen-canvas .reader a.read:hover {{ background:#fff; }}
  .verkennen-canvas .reader button.close {{ margin-top:1.2rem; background:none; border:1px solid rgba(255,255,255,.2);
    color:#cdc3a8; padding:7px 16px; border-radius:999px; cursor:pointer; font:inherit; }}
  .verkennen-canvas .reader button.close:hover {{ color:#fff; border-color:#fff; }}

  /* Geen wapen */
  .verkennen-canvas .center-overlay {{ display:none !important; }}

  footer.eindvoet {{ padding:2.5rem 1.5rem 3rem; text-align:center; color:#6b7280;
    font-family:Georgia,serif; font-size:0.9rem; border-top:1px solid #d4d1ca; margin-top:1.5rem; }}
  footer.eindvoet a {{ color:#1c5760; text-decoration:none; }}

  @media (max-width:760px) {{
    .verkennen-canvas {{ height:65vh; min-height:480px; }}
  }}
</style>
</head>
<body>

<div class="top-band">{t["topband_kop"]} — <a href="{t["topband_href"]}">{t["topband_link"]}</a></div>

<header class="masthead">
  <p class="masthead__kicker">{t["masthead_kicker"]}</p>
  <a href="./" class="masthead__logo">Het Open Vizier</a>
  <p class="masthead__sub">{t["masthead_sub"]}</p>
</header>

{menu_html(t)}

<main class="verkennen-main">

  <section class="verkennen-intro">
    <h1>{t["intro_h1"]}</h1>
    <p>{t["intro_lead"]}</p>
  </section>

  <div class="verkennen-controls">
    <button id="home" title="{t["intro_h1"]}">
      <svg viewBox="0 0 24 24"><path d="M3 11.5 L12 4 L21 11.5 M5.5 10 V20 H18.5 V10"/></svg>
      <span>{t["intro_h1"]}</span>
    </button>
    <span class="topbar-title" id="topbar-title" data-prefix=""></span>
  </div>

  <div class="verkennen-canvas">
    <div class="stage" id="stage"></div>

    <!-- center-overlay verborgen (geen wapen meer) -->
    <div class="center-overlay" id="center" style="display:none">
      <div class="veil"></div>
      <div class="label"><h2 id="center-name"></h2><p id="center-sub"></p></div>
    </div>

    <div class="loading" id="loading">{t["loading"]}</div>

    <div class="reader" id="reader">
      <h2 id="reader-title"></h2>
      <p id="reader-desc"></p>
      <a class="read" id="reader-link" href="#" target="_self">{t["reader_cta"]}</a>
      <button class="close" id="reader-close">{t["reader_terug"]}</button>
    </div>

    <div class="hint">{t["hint"]}</div>
  </div>

</main>

<footer class="eindvoet">
  <p>{t["footer_lead"]}</p>
  <p><a href="./">← {t["footer_voorpagina"]}</a></p>
</footer>

{JS_BLOK}

</body>
</html>
"""

changed = []
for lang_code, t in LANGS.items():
    path = REPO / lang_code / "verkennen.html"
    if not path.parent.exists():
        print(f"MISSING DIR: {path.parent}")
        continue
    path.write_text(build_page(t), encoding="utf-8")
    changed.append(str(path.relative_to(REPO)))

print(f"=== HERBOUWD ({len(changed)}) ===")
for c in changed: print(" -", c)
