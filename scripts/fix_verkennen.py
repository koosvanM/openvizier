#!/usr/bin/env python3
"""
Repareer verkennen.html in alle 8 talen.

Wat wordt vertaald per taal:
- <title>
- Verkennen-tag (header masthead suffix-titel via JS gevuld — alleen interface elements)
- Header link "Naar taalkeuze" (title attribuut)
- Knop "Begin" + tooltip "Terug naar begin van verkennen"
- Ondertitel "Een krant over denken zonder oogkleppen"
- "structuur laden…"
- "→ Lees het artikel"
- "Terug" (sluitknop)
- "Klik op een blok om dieper te gaan · klik op het centrum om terug"
- Volledig menu plaatsen in ES/FR/IT/PT (kort menu)
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

T = {
    "nl": {
        "title": "Verkennen — Het Open Vizier",
        "ondertitel": "Een krant over denken zonder oogkleppen",
        "taalkeuze_tip": "Naar taalkeuze",
        "begin_tip": "Terug naar begin van verkennen",
        "begin": "Begin",
        "loading": "structuur laden…",
        "read_link": "→ Lees het artikel",
        "terug": "Terug",
        "hint": "Klik op een blok om dieper te gaan · klik op het centrum om terug",
        # menu (volledig — alleen voor NL/DE/EN/RU)
        "menu_short": False,
        "lang_label": "⌂ Taal",
    },
    "de": {
        "title": "Erkunden — Het Open Vizier",
        "ondertitel": "Eine Zeitung über das Denken ohne Scheuklappen",
        "taalkeuze_tip": "Zur Sprachauswahl",
        "begin_tip": "Zurück zum Anfang von Erkunden",
        "begin": "Anfang",
        "loading": "Struktur wird geladen…",
        "read_link": "→ Den Artikel lesen",
        "terug": "Zurück",
        "hint": "Auf einen Block klicken, um tiefer zu gehen · auf das Zentrum klicken, um zurückzukehren",
        "menu_short": False,
        "lang_label": "⌂ Sprache",
    },
    "en": {
        "title": "Explore — The Open Visor",
        "ondertitel": "A newspaper about thinking without blinkers",
        "taalkeuze_tip": "To language selection",
        "begin_tip": "Back to the beginning of Explore",
        "begin": "Start",
        "loading": "loading structure…",
        "read_link": "→ Read the article",
        "terug": "Back",
        "hint": "Click on a block to go deeper · click on the centre to return",
        "menu_short": False,
        "lang_label": "⌂ Language",
    },
    "ru": {
        "title": "Исследовать — Открытое забрало",
        "ondertitel": "Газета о мышлении без шор",
        "taalkeuze_tip": "К выбору языка",
        "begin_tip": "Вернуться к началу Исследовать",
        "begin": "Начало",
        "loading": "структура загружается…",
        "read_link": "→ Читать статью",
        "terug": "Назад",
        "hint": "Нажмите на блок, чтобы углубиться · нажмите на центр, чтобы вернуться",
        "menu_short": False,
        "lang_label": "⌂ Язык",
    },
    "es": {
        "title": "Explorar — Het Open Vizier",
        "ondertitel": "Un periódico para pensar sin anteojeras",
        "taalkeuze_tip": "A la selección de idioma",
        "begin_tip": "Volver al inicio de Explorar",
        "begin": "Inicio",
        "loading": "cargando estructura…",
        "read_link": "→ Leer el artículo",
        "terug": "Atrás",
        "hint": "Haga clic en un bloque para profundizar · haga clic en el centro para volver",
        "menu_short": True,
        "lang_label": "⌂ Idioma",
        "menu_home": "Inicio", "menu_ed0": "Edición Europa", "menu_wo": "Lo que emerge",
        "menu_ed0_path": "edicion-0/", "menu_wo_path": "lo-que-emerge/",
    },
    "fr": {
        "title": "Explorer — Het Open Vizier",
        "ondertitel": "Un journal pour penser sans œillères",
        "taalkeuze_tip": "Vers le choix de la langue",
        "begin_tip": "Retour au début d'Explorer",
        "begin": "Début",
        "loading": "chargement de la structure…",
        "read_link": "→ Lire l'article",
        "terug": "Retour",
        "hint": "Cliquez sur un bloc pour aller plus profond · cliquez au centre pour revenir",
        "menu_short": True,
        "lang_label": "⌂ Langue",
        "menu_home": "Accueil", "menu_ed0": "Édition Europe", "menu_wo": "Ce qui émerge",
        "menu_ed0_path": "edition-0/", "menu_wo_path": "ce-qui-emerge/",
    },
    "it": {
        "title": "Esplorare — Het Open Vizier",
        "ondertitel": "Un giornale per pensare senza paraocchi",
        "taalkeuze_tip": "Alla selezione della lingua",
        "begin_tip": "Torna all'inizio di Esplorare",
        "begin": "Inizio",
        "loading": "caricamento struttura…",
        "read_link": "→ Leggi l'articolo",
        "terug": "Indietro",
        "hint": "Fai clic su un blocco per andare più in profondità · fai clic al centro per tornare",
        "menu_short": True,
        "lang_label": "⌂ Lingua",
        "menu_home": "Home", "menu_ed0": "Edizione Europa", "menu_wo": "Ciò che emerge",
        "menu_ed0_path": "edizione-0/", "menu_wo_path": "cio-che-emerge/",
    },
    "pt": {
        "title": "Explorar — Het Open Vizier",
        "ondertitel": "Um jornal para pensar sem antolhos",
        "taalkeuze_tip": "Para a seleção do idioma",
        "begin_tip": "Voltar ao início de Explorar",
        "begin": "Início",
        "loading": "a carregar estrutura…",
        "read_link": "→ Ler o artigo",
        "terug": "Voltar",
        "hint": "Clique num bloco para ir mais fundo · clique no centro para voltar",
        "menu_short": True,
        "lang_label": "⌂ Idioma",
        "menu_home": "Início", "menu_ed0": "Edição Europa", "menu_wo": "O que emerge",
        "menu_ed0_path": "edicao-0/", "menu_wo_path": "o-que-emerge/",
    },
}

def build_short_menu(t):
    return f'''<nav class="nav">
  <div class="nav__inner">
    <ul class="nav__links">
      <li><a href="./">{t["menu_home"]}</a></li>
      <li><a href="{t["menu_ed0_path"]}">{t["menu_ed0"]}</a></li>
      <li><a href="{t["menu_wo_path"]}">{t["menu_wo"]}</a></li>
      <li><a href="verkennen.html" class="active">{t["title"].split(" — ")[0]}</a></li>
      <li><a href="index-talenring.html">{t["lang_label"].replace("⌂ ", "")}</a></li>
    </ul>
    <div class="nav__lang">
      <a href="index-talenring.html" title="{t["lang_label"]}" style="color:#1c5760;">{t["lang_label"]}</a>
    </div>
  </div>
</nav>'''

# Standaard nav__links blok zoeken (voor NL/DE/EN/RU bestaande hervertaling van labels)
NAV_LINKS_RE = re.compile(r'(<ul class="nav__links">.*?</ul>\s*<div class="nav__lang">\s*<a href="/")(\s+)(title="[^"]+")(\s+style="color:#1c5760;">)([^<]+)(</a>\s*</div>)', re.DOTALL)

changed = []
for lang, t in T.items():
    path = REPO / lang / "verkennen.html"
    if not path.exists():
        print(f"MISSING: {path}")
        continue
    html = path.read_text(encoding="utf-8")
    orig = html

    # 1) <title>
    html = re.sub(r'<title>[^<]+</title>', f'<title>{t["title"]}</title>', html, count=1)

    # 2) Header "Naar taalkeuze" tooltip
    html = html.replace(
        '<a href="/" title="Naar taalkeuze"',
        f'<a href="/" title="{t["taalkeuze_tip"]}"',
    )

    # 3) Begin-knop tooltip + label
    html = html.replace(
        'title="Terug naar begin van verkennen"',
        f'title="{t["begin_tip"]}"',
    )
    html = html.replace(
        '<span>Begin</span>',
        f'<span>{t["begin"]}</span>',
    )

    # 4) Ondertitel
    html = html.replace(
        'Een krant over denken zonder oogkleppen',
        t["ondertitel"],
    )

    # 5) "structuur laden…"
    html = html.replace(
        'structuur laden…',
        t["loading"],
    )

    # 6) "→ Lees het artikel"
    html = html.replace(
        '→ Lees het artikel',
        t["read_link"],
    )

    # 7) "Terug" (sluitknop)
    html = html.replace(
        '<button class="close" id="reader-close">Terug</button>',
        f'<button class="close" id="reader-close">{t["terug"]}</button>',
    )

    # 8) Hint
    html = html.replace(
        'Klik op een blok om dieper te gaan · klik op het centrum om terug',
        t["hint"],
    )

    # 9) Menu: voor ES/FR/IT/PT volledig vervangen
    if t["menu_short"]:
        # Verwijder evt. bestaande <nav class="nav"> blok (er staat geen, maar veiligheidshalve)
        html = re.sub(r'<nav class="nav">.*?</nav>\s*', '', html, flags=re.DOTALL, count=1)
        # Voeg ons menu in direct na </header>
        html = re.sub(r'(</header>)', r'\1\n\n' + build_short_menu(t) + '\n', html, count=1)

    if html != orig:
        path.write_text(html, encoding="utf-8")
        changed.append(str(path.relative_to(REPO)))

print(f"=== CHANGED ({len(changed)}) ===")
for c in changed: print(" -", c)
