#!/usr/bin/env python3
"""
Plaats het uniforme hoofdmenu op alle top-level pagina's per taal.
NL is canoniek. DE/EN/RU krijgen identieke structuur met vertaalde labels
en taalspecifieke paden.

Toepassing: zoek het bestaande <nav class="nav">...</nav>-blok (eenvoudige variant
of leeg blok) en vervang door volledig menu. Voor pagina's zonder <nav class="nav">
wordt het ingevoegd direct na </header> (na de masthead).
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# Menulabels per taal — volgorde identiek
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
    },
}

def build_menu(lang, active_path=""):
    """Bouw <nav class='nav'>... voor taal. active_path = relatief pad om 'active' te markeren."""
    m = MENUS[lang]
    items_html = []
    for href, label in m["items"]:
        active = ' class="active"' if href == active_path else ''
        items_html.append(f'      <li><a href="{href}"{active}>{label}</a></li>')
    items_block = "\n".join(items_html)
    return f'''<nav class="nav">
  <div class="nav__inner">
    <ul class="nav__links">
{items_block}
    </ul>
    <div class="nav__lang">
      <a href="/" title="{m['lang_label']}" style="color:#1c5760;">{m['lang_label']}</a>
    </div>
  </div>
</nav>'''

# Pagina's per taal die het menu krijgen (= dezelfde set top-level pagina's als NL)
TARGET_PAGES = {
    "nl": ["index.html","wat-opkomt/index.html","verkennen.html","archief.html","idee.html","over.html","colofon.html","delen.html","bedankt.html","talenring.html","index-klassiek.html","navigatie.html","structuur.html"],
    "de": ["index.html","was-aufkommt/index.html","verkennen.html","archiv.html","idee.html","ueber.html","impressum.html","teilen.html","bedankt.html","index-talenring.html","index-klassiek.html"],
    "en": ["index.html","what-surfaces/index.html","verkennen.html","archive.html","idea.html","about.html","colophon.html","share.html","bedankt.html","index-talenring.html","index-klassiek.html"],
    "ru": ["index.html","chto-vsplyvaet/index.html","verkennen.html","arkhiv.html","ideya.html","o-gazete.html","vykhodnye-dannye.html","podelitsya.html","bedankt.html","index-talenring.html","index-klassiek.html"],
}

# Active-path mapping (kruimels: welke menu-item hoort bij deze pagina)
def active_for(lang, page_rel):
    """Geef terug welk href in MENUS overeenkomt met deze pagina."""
    m = MENUS[lang]
    # index.html -> ./
    if page_rel == "index.html":
        return "./"
    # subdir/index.html -> subdir/
    if page_rel.endswith("/index.html"):
        return page_rel[:-len("index.html")]
    # losse top-level
    return page_rel

changed, skipped = [], []

# Bestaand <nav class="nav">...</nav> blok regex (greedy tot </nav>)
NAV_RE = re.compile(r'<nav class="nav">.*?</nav>', re.DOTALL)

for lang in ["nl", "de", "en", "ru"]:
    for page in TARGET_PAGES[lang]:
        path = REPO / lang / page
        if not path.exists():
            skipped.append(f"MISSING: {path}")
            continue
        html = path.read_text(encoding="utf-8")
        active = active_for(lang, page)
        # Voor sub-paginas onder /wat-opkomt/ moeten relatieve URLs aangepast worden
        # Maar TARGET_PAGES bevat alleen 'wat-opkomt/index.html' — die heeft relatieve paden naar parent
        menu_html = build_menu(lang, active)
        # Als pagina onder een subdir zit (zoals wat-opkomt/index.html),
        # moeten links 1 niveau omhoog
        if "/" in page:
            # Prefixeer alle relatieve hrefs met ../
            def fix_href(m):
                href = m.group(1)
                if href.startswith("/") or href.startswith("http") or href.startswith("#"):
                    return m.group(0)
                return f'href="../{href}"'
            menu_html_local = re.sub(r'href="([^"]+)"', fix_href, menu_html, count=len(MENUS[lang]["items"])+1)
            # eerste 'active' link (./) wordt ../ — dat klopt
            menu_to_use = menu_html_local
        else:
            menu_to_use = menu_html

        if NAV_RE.search(html):
            new_html = NAV_RE.sub(menu_to_use, html, count=1)
        else:
            # Invoegen direct na sluiting van masthead/header
            m_head = re.search(r'(</header>)', html)
            if m_head:
                idx = m_head.end()
                new_html = html[:idx] + "\n\n" + menu_to_use + "\n" + html[idx:]
            else:
                # Fallback: na <body>
                m_body = re.search(r'(<body[^>]*>)', html)
                if m_body:
                    idx = m_body.end()
                    new_html = html[:idx] + "\n" + menu_to_use + "\n" + html[idx:]
                else:
                    skipped.append(f"no anchor: {path}")
                    continue

        if new_html == html:
            skipped.append(f"unchanged: {path}")
            continue
        path.write_text(new_html, encoding="utf-8")
        changed.append(str(path.relative_to(REPO)))

print(f"=== CHANGED ({len(changed)}) ===")
for c in changed: print(" -", c)
print(f"\n=== SKIPPED ({len(skipped)}) ===")
for s in skipped: print(" -", s)
