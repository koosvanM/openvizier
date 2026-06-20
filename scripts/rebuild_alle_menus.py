#!/usr/bin/env python3
"""
Rebuild alle <nav class="nav"> menubalken in alle HTML-bestanden, alle talen,
volgens de canonieke menu_definitie.

Regels:
- Bestanden MET een bestaande <nav class="nav">...</nav>: VERVANG dat blok
- Bestanden met <header class="masthead"> maar geen menu: INVOEGEN na </header>
- Talenring-pagina's: SKIPPEN (hebben eigen donkere stijl, geen menu)
- Artikelpagina's (geen masthead): SKIPPEN (zoals afgesproken)
- Editie-indexen die wel content tonen maar geen masthead: INVOEGEN na <h1> in <header>?
  Voor de zekerheid: alleen pagina's met <header class="masthead"> krijgen menu.

Diepte wordt berekend uit het bestandspad.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from menu_definitie import build_menu, MENUS

REPO = Path("/tmp/gh-repo")
LANGS = list(MENUS.keys())

# Talenring-pagina's krijgen geen menu (donkere standalone)
SKIP_NAMES = {"index-talenring.html", "talenring.html"}

# Bestaand <nav class="nav">...</nav> regex (greedy maar binnen één blok)
NAV_RE = re.compile(r'<nav class="nav">.*?</nav>', re.DOTALL)

# Header anchor — zoek </header> als invoegpunt
HEADER_END_RE = re.compile(r'</header>')

stats = {"vervangen": 0, "ingevoegd": 0, "skip_geen_anker": 0,
         "skip_talenring": 0, "skip_geen_masthead": 0, "ongewijzigd": 0}

changed_files = []
no_anchor = []

for lang in LANGS:
    lang_dir = REPO / lang
    if not lang_dir.exists():
        continue
    # Alle HTML-bestanden in deze taal
    for html_path in sorted(lang_dir.rglob("*.html")):
        rel_in_taal = html_path.relative_to(lang_dir).as_posix()  # bv. "wat-opkomt/index.html"
        name = html_path.name

        # Skip talenringen
        if name in SKIP_NAMES:
            stats["skip_talenring"] += 1
            continue

        html = html_path.read_text(encoding="utf-8")

        # Bouw het juiste menu voor deze pagina
        new_menu = build_menu(lang, rel_in_taal)

        # CASE 1: bestaande <nav class="nav"> → vervangen
        if NAV_RE.search(html):
            new_html = NAV_RE.sub(new_menu, html, count=1)
            if new_html != html:
                html_path.write_text(new_html, encoding="utf-8")
                changed_files.append(str(html_path.relative_to(REPO)))
                stats["vervangen"] += 1
            else:
                stats["ongewijzigd"] += 1
            continue

        # CASE 2: heeft <header class="masthead"> maar geen menu → invoegen
        if 'class="masthead"' in html or '<header class="masthead' in html:
            # Voeg na </header>
            m = HEADER_END_RE.search(html)
            if m:
                idx = m.end()
                new_html = html[:idx] + "\n\n" + new_menu + "\n" + html[idx:]
                html_path.write_text(new_html, encoding="utf-8")
                changed_files.append(str(html_path.relative_to(REPO)))
                stats["ingevoegd"] += 1
            else:
                no_anchor.append(str(html_path.relative_to(REPO)))
                stats["skip_geen_anker"] += 1
            continue

        # CASE 3: geen masthead, geen menu — artikelpagina, skip
        stats["skip_geen_masthead"] += 1

print("=== STATS ===")
for k, v in stats.items():
    print(f"  {k}: {v}")
print(f"\nTotaal gewijzigde bestanden: {len(changed_files)}")
if no_anchor:
    print(f"\n=== GEEN ANCHOR ({len(no_anchor)}) ===")
    for n in no_anchor[:10]: print(f"  - {n}")
print("\n=== EERSTE 20 GEWIJZIGD ===")
for c in changed_files[:20]:
    print(f"  - {c}")
