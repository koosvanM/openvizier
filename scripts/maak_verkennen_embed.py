#!/usr/bin/env python3
"""
Genereer een 'bare' versie van verkennen.html per taal — alleen het canvas
en JS, zonder masthead/menu/footer. Bedoeld voor inbedding via <iframe>.

Output: <lang>/verkennen-embed.html per taal.
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
JS_PATH = Path("/tmp/verkennen_script.js")
JS_BLOK = JS_PATH.read_text(encoding="utf-8")

LANGS = {
    "nl": {
        "lang": "nl",
        "title": "Verkennen — Het Open Vizier",
        "hint": "Klik op een blok om dieper te gaan · klik op het centrum om terug",
        "loading": "structuur laden…",
        "reader_cta": "→ Lees het artikel",
        "reader_terug": "Terug",
        "begin": "Begin",
        "begin_tip": "Terug naar begin van Verkennen",
    },
    "de": {
        "lang": "de",
        "title": "Erkunden — Het Open Vizier",
        "hint": "Auf einen Block klicken, um tiefer zu gehen · auf das Zentrum klicken, um zurückzukehren",
        "loading": "Struktur wird geladen…",
        "reader_cta": "→ Den Artikel lesen",
        "reader_terug": "Zurück",
        "begin": "Anfang",
        "begin_tip": "Zurück zum Anfang von Erkunden",
    },
    "en": {
        "lang": "en",
        "title": "Explore — The Open Visor",
        "hint": "Click on a block to go deeper · click on the centre to return",
        "loading": "loading structure…",
        "reader_cta": "→ Read the article",
        "reader_terug": "Back",
        "begin": "Start",
        "begin_tip": "Back to the beginning of Explore",
    },
    "ru": {
        "lang": "ru",
        "title": "Исследовать — Открытое забрало",
        "hint": "Нажмите на блок, чтобы углубиться · нажмите на центр, чтобы вернуться",
        "loading": "структура загружается…",
        "reader_cta": "→ Читать статью",
        "reader_terug": "Назад",
        "begin": "Начало",
        "begin_tip": "Вернуться к началу Исследовать",
    },
}


TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  :root {{ --bg:#2e2519; --ink:#1a1a1a; --muted:#9a9385; --cream:#f6f1e6; }}
  *{{ box-sizing:border-box; margin:0; padding:0; }}
  html, body {{ height:100%; background:var(--bg); color:var(--cream);
    font-family:Georgia,"Times New Roman",serif; overflow:hidden; }}

  /* Stage = grid van blokken, vult de hele iframe */
  .stage {{ position:fixed; inset:0; display:grid; gap:0; background:var(--bg); overflow:hidden; }}

  /* Home-knop linksboven, vlakbij rand */
  .home-btn {{ position:fixed; top:10px; left:10px; z-index:10;
    background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.18);
    color:#e3d8bc; padding:5px 10px; border-radius:4px; cursor:pointer;
    display:none; align-items:center; gap:5px; font-size:12px; font-family:inherit; }}
  .home-btn.show {{ display:inline-flex; }}
  .home-btn:hover {{ background:rgba(255,255,255,0.10); }}
  .home-btn svg {{ width:12px; height:12px; stroke:currentColor; fill:none; stroke-width:1.8; }}

  /* Tile styling */
  .tile {{ position:relative; overflow:hidden; cursor:pointer;
    display:flex; align-items:center; justify-content:center; transition:opacity .5s ease; }}
  .tile.concept, .tile.onbereikbaar {{ cursor:default; }}
  .tile.concept .bg, .tile.onbereikbaar .bg {{ filter:sepia(.55) brightness(.50) contrast(1.05) saturate(.35); }}
  .tile.concept:hover .bg, .tile.onbereikbaar:hover .bg {{ filter:sepia(.55) brightness(.50) contrast(1.05) saturate(.35); }}
  .tile.concept .label::after {{ content:"binnenkort"; display:block; margin-top:.6em;
    font-size:.7em; font-style:italic; color:rgba(255,255,255,.55);
    letter-spacing:1.5px; text-transform:uppercase; }}
  .tile.concept .label h2, .tile.onbereikbaar .label h2 {{ opacity:.7; }}
  .tile.vervolg {{ background:#1a1612; }}
  .tile.vervolg .bg {{ display:none; }}
  .tile.vervolg .veil {{ background:linear-gradient(135deg,rgba(40,32,22,.6) 0%,rgba(0,0,0,.4) 100%); }}
  .tile.vervolg .label h2 {{ font-style:italic; letter-spacing:2px; opacity:.85; }}
  .tile .bg {{ position:absolute; inset:-2%; background-size:cover; background-position:center;
    filter:sepia(.35) brightness(.85) contrast(1.05); transition:filter .4s ease, transform .8s ease; }}
  .tile:hover .bg {{ filter:sepia(.25) brightness(.95) contrast(1.1); transform:scale(1.04); }}
  .tile .veil {{ position:absolute; inset:0;
    background:linear-gradient(180deg,rgba(0,0,0,.10) 0%,rgba(0,0,0,.38) 100%); pointer-events:none; }}
  .tile .label {{ position:relative; z-index:2; text-align:center; padding:1rem; max-width:90%; }}
  .tile .label h2 {{ font-size:clamp(1rem,2.4vw,1.9rem); font-weight:700; line-height:1.1;
    color:#f7efdc; letter-spacing:.4px; text-shadow:0 2px 14px rgba(0,0,0,.55); }}
  .tile .label p {{ margin-top:.4em; font-size:clamp(.75rem,1vw,.95rem); font-style:italic;
    color:#e3d8bc; opacity:.92; text-shadow:0 1px 8px rgba(0,0,0,.6); }}
  .tile.entering {{ opacity:0; animation:tileIn .6s cubic-bezier(.22,1,.36,1) forwards; }}
  @keyframes tileIn {{ from {{ opacity:0; transform:scale(1.04); }} to {{ opacity:1; transform:scale(1); }} }}

  /* Loading text */
  .loading {{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
    color:rgba(231,222,193,.7); font-style:italic; z-index:1; }}

  /* Hint onderaan */
  .hint {{ position:fixed; bottom:8px; left:50%; transform:translateX(-50%);
    color:rgba(231,222,193,.55); font-size:11px; font-style:italic;
    pointer-events:none; z-index:6; }}

  /* Reader overlay */
  .reader {{ position:fixed; inset:0; background:rgba(20,16,12,.92);
    display:none; align-items:center; justify-content:center; flex-direction:column;
    padding:30px; text-align:center; z-index:20; }}
  .reader.show {{ display:flex; }}
  .reader h2 {{ font-size:clamp(1.4rem,2.6vw,2rem); margin-bottom:1rem; color:#f7efdc; }}
  .reader p {{ max-width:600px; color:#cdc3a8; font-size:1rem; line-height:1.55; margin-bottom:1.4rem; }}
  .reader a.read {{ background:#f7efdc; color:#1a1612; padding:11px 24px; text-decoration:none;
    border-radius:999px; font-size:14px; letter-spacing:.4px; }}
  .reader a.read:hover {{ background:#fff; }}
  .reader button.close {{ margin-top:1.2rem; background:none; border:1px solid rgba(255,255,255,.2);
    color:#cdc3a8; padding:7px 16px; border-radius:999px; cursor:pointer; font:inherit; }}

  /* Center-overlay verborgen */
  .center-overlay {{ display:none !important; }}
</style>
</head>
<body>

<button id="home" class="home-btn" title="{begin_tip}">
  <svg viewBox="0 0 24 24"><path d="M3 11.5 L12 4 L21 11.5 M5.5 10 V20 H18.5 V10"/></svg>
  <span>{begin}</span>
</button>

<!-- breadcrumb-element vereist door JS, verborgen in embed -->
<span id="topbar-title" data-prefix="" style="position:absolute;top:10px;left:60px;color:#cdc3a8;font-size:12px;font-style:italic;z-index:9;pointer-events:none;"></span>

<div class="stage" id="stage"></div>

<div class="center-overlay" id="center" style="display:none">
  <div class="veil"></div>
  <div class="label"><h2 id="center-name"></h2><p id="center-sub"></p></div>
</div>

<div class="loading" id="loading">{loading}</div>

<div class="reader" id="reader">
  <h2 id="reader-title"></h2>
  <p id="reader-desc"></p>
  <a class="read" id="reader-link" href="#" target="_top">{reader_cta}</a>
  <button class="close" id="reader-close">{reader_terug}</button>
</div>

<div class="hint">{hint}</div>

{js_blok}

</body>
</html>
"""


changed = []
for lang, t in LANGS.items():
    path = REPO / lang / "verkennen-embed.html"
    content = TEMPLATE.format(js_blok=JS_BLOK, **t)
    path.write_text(content, encoding="utf-8")
    changed.append(str(path.relative_to(REPO)))

print(f"=== Aangemaakt ({len(changed)}) ===")
for c in changed: print(f"  - {c}")
