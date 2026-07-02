#!/usr/bin/env python3
"""Eén canonieke menu-definitie voor alle 8 talen.

NL/DE/EN/RU: volledig menu (11 items)
ES/FR/IT/PT: kort menu (4 items)

Diepte-prefix wordt door build_menu() berekend op basis van het pagina-pad.
"""

# (href_relatief_aan_taalroot, label)
MENUS = {
    "nl": {
        "items": [
            ("./", "Voorpagina"),
            ("wat-opkomt/", "Wat opkomt"),
            ("verkennen.html", "Verkennen"),
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
        "lang_link_rel": "/",  # root taalkeuze
    },
    "de": {
        "items": [
            ("./", "Startseite"),
            ("was-aufkommt/", "Was aufkommt"),
            ("verkennen.html", "Erkunden"),
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
        "lang_link_rel": "/",
    },
    "en": {
        "items": [
            ("./", "Home"),
            ("what-surfaces/", "What surfaces"),
            ("verkennen.html", "Explore"),
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
        "lang_link_rel": "/",
    },
    "ru": {
        "items": [
            ("./", "Главная"),
            ("chto-vsplyvaet/", "Что всплывает"),
            ("verkennen.html", "Исследовать"),
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
        "lang_link_rel": "/",
    },
    "es": {
        "items": [
            ("./", "Inicio"),
            ("edicion-0/", "Edición Europa"),
            ("lo-que-emerge/", "Lo que emerge"),
            ("verkennen.html", "Explorar"),
        ],
        "lang_label": "⌂ Idioma",
        "lang_link_rel": "index-talenring.html",  # blijft binnen taal
    },
    "fr": {
        "items": [
            ("./", "Accueil"),
            ("edition-0/", "Édition Europe"),
            ("ce-qui-emerge/", "Ce qui émerge"),
            ("verkennen.html", "Explorer"),
        ],
        "lang_label": "⌂ Langue",
        "lang_link_rel": "index-talenring.html",
    },
    "it": {
        "items": [
            ("./", "Home"),
            ("edizione-0/", "Edizione Europa"),
            ("cio-che-emerge/", "Ciò che emerge"),
            ("verkennen.html", "Esplorare"),
        ],
        "lang_label": "⌂ Lingua",
        "lang_link_rel": "index-talenring.html",
    },
    "pt": {
        "items": [
            ("./", "Início"),
            ("edicao-0/", "Edição Europa"),
            ("o-que-emerge/", "O que emerge"),
            ("verkennen.html", "Explorar"),
        ],
        "lang_label": "⌂ Idioma",
        "lang_link_rel": "index-talenring.html",
    },
}


def build_menu(lang, page_path_in_taal):
    """Bouw uniform <nav class="nav">...</nav> blok voor een pagina.

    Args:
        lang: 'nl', 'de', etc.
        page_path_in_taal: relatief pad ten opzichte van /<lang>/, bv:
            'index.html'                     -> depth 0
            'verkennen.html'                 -> depth 0
            'wat-opkomt/index.html'          -> depth 1
            'editie-0/de-grote-plundering.html' -> depth 1
    """
    t = MENUS[lang]
    parts = page_path_in_taal.split("/")
    depth = len(parts) - 1  # alles ná de laatste / is bestand
    prefix = "../" * depth

    # Bepaal active item: matching op het eerste pad-onderdeel of het hele bestand
    if depth == 0:
        # bv. "index.html" -> active is "./"
        # bv. "verkennen.html" -> active is "verkennen.html"
        # bv. "delen.html" -> active is "delen.html"
        active = parts[0] if parts[0] != "index.html" else "./"
    else:
        # Subdir-pagina: active is "<subdir>/"
        active = parts[0] + "/"

    items_html = []
    for href, label in t["items"]:
        active_attr = ' class="active"' if href == active else ''
        if href == "./" and depth > 0:
            # voor subdir-niveaus: ./ wordt ../
            full_href = prefix.rstrip("/") + "/" if prefix else "./"
            # mooie weergave: gebruik bv. '../'
            full_href = prefix if prefix else "./"
        else:
            full_href = (prefix + href) if not href.startswith("/") else href

        items_html.append(f'      <li><a href="{full_href}"{active_attr}>{label}</a></li>')

    # Talenkeuze-link
    if t["lang_link_rel"].startswith("/"):
        lang_href = t["lang_link_rel"]
    else:
        lang_href = prefix + t["lang_link_rel"]

    return f'''<nav class="nav">
  <div class="nav__inner">
    <ul class="nav__links">
{chr(10).join(items_html)}
    </ul>
    <div class="nav__lang">
      <a href="{lang_href}" title="{t["lang_label"]}" style="color:#1c5760;">{t["lang_label"]}</a>
    </div>
  </div>
</nav>'''
