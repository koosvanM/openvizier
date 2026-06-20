#!/usr/bin/env python3
"""
Verplaats óók 'De voedingslijn' en 'Het immuunsysteem dat gezonde cellen aanvalt'
van bovenaan nl/wat-opkomt/index.html naar onderaan, na de proloog-card en vóór
de drie harde anti-immuun-leads.

Volgorde-doel onderaan:
1. Sectietitel-blok (al aanwezig)
2. Proloog "Een staat met een auto-immuunziekte" (al aanwezig)
3. De voedingslijn (verplaatsen vanaf boven)
4. Het immuunsysteem dat gezonde cellen aanvalt (verplaatsen vanaf boven)
5. De anti-immuunziekte van Brussel (al onderaan)
6. De anti-immuunziekte van onze overheid slaat toe (al onderaan)
7. Zij doden hun levensader (al onderaan)
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
PATH = REPO / "nl/wat-opkomt/index.html"

html = PATH.read_text(encoding="utf-8")

# Marker voor idempotentie
MARKER = "<!-- voedingslijn-immuun-verplaatst v1 -->"
if MARKER in html:
    print("al verplaatst, niets te doen")
    raise SystemExit(0)

# Twee titels om te lokaliseren
markers = [
    "De voedingslijn — alles is een vervangingsmarkt",
    "Het immuunsysteem dat gezonde cellen aanvalt",
]

extracted_sections = []
for marker in markers:
    idx = html.find(marker)
    if idx == -1:
        print(f"NIET GEVONDEN: {marker}")
        raise SystemExit(1)
    sec_start = html.rfind("<section", 0, idx)
    sec_end = html.find("</section>", idx) + len("</section>")
    if sec_start == -1 or sec_end < 0:
        print(f"section grens niet gevonden voor: {marker}")
        raise SystemExit(1)
    extracted_sections.append((sec_start, sec_end))

# Sorteer op startpositie
extracted_sections.sort()

# Knip beide blokken eruit
parts, extracted = [], []
last = 0
for s, e in extracted_sections:
    parts.append(html[last:s])
    extracted.append(html[s:e])
    last = e
parts.append(html[last:])
new_html = "".join(parts)
extracted_block = "\n\n".join(extracted)

# Insertieplek: direct ná de proloog-card, vóór de eerste anti-immuunziekte-lead-sectie
# (zoek naar "de-anti-immuunziekte-van-brussel.html" link)
# Anker: zoek de <section> die de "LEAD BRUSSEL · 19 juni 2026" tekst bevat
lead_marker_idx = new_html.find("★★★ LEAD BRUSSEL")
if lead_marker_idx == -1:
    print("LEAD BRUSSEL marker niet gevonden")
    raise SystemExit(1)
sec_start = new_html.rfind("<section", 0, lead_marker_idx)
class Wrap: pass
m_target = Wrap(); m_target.start = lambda: sec_start
if not m_target:
    print("insertie-anker niet gevonden")
    raise SystemExit(1)
insert_idx = m_target.start()

# Bouw het in te voegen blok
inject = f"\n\n{MARKER}\n{extracted_block}\n\n"
new_html = new_html[:insert_idx] + inject + new_html[insert_idx:]

PATH.write_text(new_html, encoding="utf-8")
print(f"Verplaatst: {len(extracted)} secties naar nieuwe positie")
print(f"Pagina-grootte: {len(html)} → {len(new_html)} bytes")
