#!/usr/bin/env python3
"""
Verplaats de 5 anti-immuun-blokken op de NL voorpagina van bovenaan
naar onderaan de home-wo sectie, met proloog-card als ingang.

Vijf <a class="home-wo__rij-breed"> blokken te verplaatsen
(geïdentificeerd via href-target):
1. wat-opkomt/de-anti-immuunziekte-van-brussel.html
2. wat-opkomt/de-auto-immuunziekte-slaat-toe.html
3. wat-opkomt/zij-doden-hun-levensader.html
4. wat-opkomt/de-methodologie-van-de-aanpassing.html (voedingslijn)
5. wat-opkomt/het-immuunsysteem-van-organisaties.html

Volgorde onderaan home-wo (vóór .home-wo__naar_alles):
- sectietitel "Eerst het beeld. Dan de toepassing."
- proloog-card "Een staat met een auto-immuunziekte"
- De voedingslijn
- Het immuunsysteem
- De anti-immuunziekte van Brussel
- De anti-immuunziekte van onze overheid slaat toe
- Zij doden hun levensader
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
PATH = REPO / "nl/index.html"
html = PATH.read_text(encoding="utf-8")

MARKER = "<!-- voorpagina-anti-immuun-onderaan v1 -->"
if MARKER in html:
    print("al verplaatst")
    raise SystemExit(0)

# Volgorde-doel onderaan (slug -> volgorde-index)
TARGETS = [
    "wat-opkomt/de-methodologie-van-de-aanpassing.html",
    "wat-opkomt/het-immuunsysteem-van-organisaties.html",
    "wat-opkomt/de-anti-immuunziekte-van-brussel.html",
    "wat-opkomt/de-auto-immuunziekte-slaat-toe.html",
    "wat-opkomt/zij-doden-hun-levensader.html",
]

# Voor elk doel: zoek de bijbehorende <a href="..."> tot en met </a>
# (de blokken zijn allemaal home-wo__rij-breed kaarten)
def find_block(html, href):
    """Vind de complete <a href="..."> ... </a> blok inclusief leading whitespace."""
    pat = re.compile(
        r'\n?\s*<a\s+href="' + re.escape(href) + r'"[^>]*>.*?</a>',
        re.DOTALL
    )
    m = pat.search(html)
    return (m.start(), m.end(), m.group(0)) if m else (None, None, None)

# Knip alle 5 blokken eruit
removed_blocks = {}  # href -> raw HTML
new_html = html
for href in TARGETS:
    s, e, block = find_block(new_html, href)
    if s is None:
        print(f"NIET GEVONDEN: {href}")
        raise SystemExit(1)
    removed_blocks[href] = block
    new_html = new_html[:s] + new_html[e:]

# Vind de insertie-positie: vlak vóór <p class="home-wo__naar_alles">
m_naar = re.search(r'\s*<p class="home-wo__naar_alles">', new_html)
if not m_naar:
    print("home-wo__naar_alles niet gevonden")
    raise SystemExit(1)
insert_idx = m_naar.start()

# Bouw insertie-blok
sectietitel = '''
<section style="grid-column: 1 / -1; margin:3rem auto 1rem auto; padding:0 1.25rem; text-align:center;">
  <p style="font-size:0.8rem;letter-spacing:0.12em;text-transform:uppercase;color:#5a7a78;margin:0 0 0.4rem 0;font-family:Georgia,serif;font-weight:600;">De diagnose — onderaan</p>
  <h2 style="font-family:Georgia,serif;font-size:clamp(1.7rem,3.6vw,2.3rem);color:#1a1a1a;margin:0 0 0.7rem 0;font-weight:700;font-style:italic;">Eerst het beeld. Dan de toepassing.</h2>
  <p style="font-family:Georgia,serif;font-style:italic;color:#4a5263;max-width:720px;margin:0 auto;line-height:1.6;">Onderaan deze pagina staat een rustige proloog die de medische metafoor uitlegt, gevolgd door vijf artikelen die het beeld concreet toepassen op de bestuurlijke werkelijkheid.</p>
</section>
'''

proloog_card = '''
<a href="wat-opkomt/de-metafoor-auto-immuunziekte.html" style="grid-column: 1 / -1; display:block;text-decoration:none;color:inherit;background:#eef1e8;border:1px solid #c8d2bb;border-left:5px solid #5a7a52;padding:2rem 2rem;margin:0 auto 2rem auto;max-width:960px;border-radius:4px;transition:box-shadow 0.2s;" onmouseover="this.style.boxShadow='0 6px 18px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
  <p style="font-size:0.78rem;letter-spacing:0.12em;text-transform:uppercase;color:#5a7a52;margin:0 0 0.5rem 0;font-family:Georgia,serif;font-weight:600;">Proloog · het beeld</p>
  <h3 style="font-family:Georgia,serif;font-size:clamp(1.5rem,3vw,2rem);color:#1a1a1a;margin:0 0 0.7rem 0;font-weight:700;line-height:1.2;">Een staat met een auto-immuunziekte</h3>
  <p style="font-family:Georgia,serif;font-style:italic;color:#3a4a35;margin:0 0 0.8rem 0;font-size:1.05rem;line-height:1.6;">Een beeld om mee te denken, niet om mee te slaan. Rustig uitgelegd, in één keer te volgen — de metafoor waarmee de vijf stukken hierna gelezen kunnen worden.</p>
  <span style="display:inline-block;color:#5a7a52;font-weight:700;border-bottom:1px solid #5a7a52;padding-bottom:1px;font-size:0.95rem;font-family:Georgia,serif;">Lees de proloog →</span>
</a>
'''

# Voeg blokken in volgens TARGETS-volgorde
ordered_blocks = "\n".join(removed_blocks[href] for href in TARGETS)

injection = f"\n\n{MARKER}\n{sectietitel}\n{proloog_card}\n{ordered_blocks}\n"

new_html = new_html[:insert_idx] + injection + new_html[insert_idx:]

PATH.write_text(new_html, encoding="utf-8")
print(f"OK: 5 blokken verplaatst + proloog + sectietitel ingevoegd")
print(f"Bytes: {len(html)} → {len(new_html)}")
