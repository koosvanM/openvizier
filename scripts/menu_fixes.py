#!/usr/bin/env python3
"""
Menu-correcties:

FIX 1: ES/FR/IT/PT voorpagina's — voeg Verkennen-link toe aan kort menu
FIX 2: nl/onderzoek/index.html — vervang afwijkend menu door standaard NL-menu
       (paden ../ voor subdir-niveau)
FIX 3: ES/FR/IT/PT subdir-indexes (edicion-0/index.html, lo-que-emerge/index.html
       en hun varianten) — voeg het korte menu toe direct na </header>,
       met paden ../ aangepast voor subdir-niveau
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

SHORT_MENU_LANGS = {
    "es": {
        "lang_label": "⌂ Idioma",
        "lang_link_rel": "index-talenring.html",
        "items": [
            ("./", "Inicio"),
            ("edicion-0/", "Edición Europa"),
            ("lo-que-emerge/", "Lo que emerge"),
            ("verkennen.html", "Explorar"),
        ],
    },
    "fr": {
        "lang_label": "⌂ Langue",
        "lang_link_rel": "index-talenring.html",
        "items": [
            ("./", "Accueil"),
            ("edition-0/", "Édition Europe"),
            ("ce-qui-emerge/", "Ce qui émerge"),
            ("verkennen.html", "Explorer"),
        ],
    },
    "it": {
        "lang_label": "⌂ Lingua",
        "lang_link_rel": "index-talenring.html",
        "items": [
            ("./", "Home"),
            ("edizione-0/", "Edizione Europa"),
            ("cio-che-emerge/", "Ciò che emerge"),
            ("verkennen.html", "Esplorare"),
        ],
    },
    "pt": {
        "lang_label": "⌂ Idioma",
        "lang_link_rel": "index-talenring.html",
        "items": [
            ("./", "Início"),
            ("edicao-0/", "Edição Europa"),
            ("o-que-emerge/", "O que emerge"),
            ("verkennen.html", "Explorar"),
        ],
    },
}

def build_short_menu(lang, active_path, depth):
    """Bouw <nav class="nav"> blok. depth=0 voor top-level, 1 voor één subdir diep."""
    t = SHORT_MENU_LANGS[lang]
    prefix = "../" * depth
    items_html = []
    for href, label in t["items"]:
        active = ' class="active"' if href == active_path else ''
        items_html.append(f'      <li><a href="{prefix}{href}"{active}>{label}</a></li>')
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


# =============================================================================
# FIX 1: ES/FR/IT/PT voorpagina — Verkennen-link toevoegen
# =============================================================================

VOORPAGINA_VERKENNEN_LINK = {
    "es": ('verkennen.html', 'Explorar'),
    "fr": ('verkennen.html', 'Explorer'),
    "it": ('verkennen.html', 'Esplorare'),
    "pt": ('verkennen.html', 'Explorar'),
}

changed = []
warnings = []

for lang, (href, label) in VOORPAGINA_VERKENNEN_LINK.items():
    path = REPO / lang / "index.html"
    html = path.read_text(encoding="utf-8")
    if f'>{label}</a>' in html:
        # al aanwezig
        continue
    # Voeg <li><a href="verkennen.html">LABEL</a></li> toe vóór het laatste <li> dat "lang_link" bevat
    # We zoeken het <li> dat naar index-talenring.html verwijst (idioma-link in NL stijl)
    # In de ES/FR/IT/PT voorpagina staat die zo:
    # <li><a href="index-talenring.html">{lang_menu without ⌂}</a></li>
    pattern = re.compile(r'(<li><a href="index-talenring\.html">[^<]+</a></li>)')
    m = pattern.search(html)
    if not m:
        warnings.append(f"FIX1 anker niet gevonden: {path}")
        continue
    new_item = f'<li><a href="{href}">{label}</a></li>\n      '
    new_html = html[:m.start()] + new_item + html[m.start():]
    path.write_text(new_html, encoding="utf-8")
    changed.append(str(path.relative_to(REPO)))

# =============================================================================
# FIX 2: nl/onderzoek/index.html — repareer afwijkend menu
# =============================================================================

NL_ONDERZOEK_PATH = REPO / "nl/onderzoek/index.html"
if NL_ONDERZOEK_PATH.exists():
    html = NL_ONDERZOEK_PATH.read_text(encoding="utf-8")
    # Standaard NL-menu op subdir-niveau (1 diep)
    standaard_menu = '''<nav class="nav">
  <div class="nav__inner">
    <ul class="nav__links">
      <li><a href="../">Voorpagina</a></li>
      <li><a href="../wat-opkomt/">Wat opkomt</a></li>
      <li><a href="../verkennen.html">Verkennen</a></li>
      <li><a href="../editie-6/">Editie 6</a></li>
      <li><a href="../editie-5/">Editie 5</a></li>
      <li><a href="../editie-4/">Editie 4</a></li>
      <li><a href="../editie-3/">Editie 3</a></li>
      <li><a href="../editie-2/">Editie 2</a></li>
      <li><a href="../editie-1/">Editie 1</a></li>
      <li><a href="../editie-0/">Editie Europa</a></li>
      <li><a href="../delen.html">Delen</a></li>
    </ul>
    <div class="nav__lang">
      <a href="/" title="⌂ Taal" style="color:#1c5760;">⌂ Taal</a>
    </div>
  </div>
</nav>'''
    # Vervang het oude nav-blok
    new = re.sub(r'<nav class="nav">.*?</nav>', standaard_menu, html, count=1, flags=re.DOTALL)
    if new != html:
        NL_ONDERZOEK_PATH.write_text(new, encoding="utf-8")
        changed.append("nl/onderzoek/index.html")

# =============================================================================
# FIX 3: ES/FR/IT/PT subdir-indexes — menu toevoegen
# =============================================================================

SUBDIR_INDEXES = {
    "es": ["edicion-0/index.html", "lo-que-emerge/index.html"],
    "fr": ["edition-0/index.html", "ce-qui-emerge/index.html"],
    "it": ["edizione-0/index.html", "cio-che-emerge/index.html"],
    "pt": ["edicao-0/index.html", "o-que-emerge/index.html"],
}

for lang, paths in SUBDIR_INDEXES.items():
    for rel in paths:
        full = REPO / lang / rel
        if not full.exists():
            warnings.append(f"FIX3 niet gevonden: {full}")
            continue
        html = full.read_text(encoding="utf-8")
        # Heeft al een menu?
        if 'class="nav__links"' in html:
            continue
        # Bepaal active_path
        first_part = rel.split("/")[0] + "/"
        menu = build_short_menu(lang, first_part, depth=1)
        # Voeg in direct na </header>; als geen </header>, na <body>
        if '</header>' in html:
            html = html.replace('</header>', '</header>\n\n' + menu + '\n', 1)
        elif '<body' in html:
            html = re.sub(r'(<body[^>]*>)', r'\1\n' + menu + '\n', html, count=1)
        else:
            warnings.append(f"FIX3 geen anker: {full}")
            continue
        full.write_text(html, encoding="utf-8")
        changed.append(str(full.relative_to(REPO)))

print(f"=== CHANGED ({len(changed)}) ===")
for c in changed: print(" -", c)
if warnings:
    print(f"\n=== WARNINGS ({len(warnings)}) ===")
    for w in warnings: print(" -", w)
