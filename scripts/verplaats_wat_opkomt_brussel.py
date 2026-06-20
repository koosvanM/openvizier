#!/usr/bin/env python3
"""
Verplaats de drie anti-immuunziekte-openers in nl/wat-opkomt/index.html
naar onderaan (vóór de footer), na al het andere materiaal.

De drie openers (titels):
1. "De anti-immuunziekte van Brussel maakt dat we arm worden"
2. "De anti-immuunziekte van onze overheid slaat toe"
3. "Zij doden hun levensader"

Plus equivalenten voor DE/EN/RU in hun was-aufkommt/what-surfaces/chto-vsplyvaet/index.html
indien die ook drie zulke openers hebben.
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

PAGES = {
    "nl": {
        "path": "nl/wat-opkomt/index.html",
        "markers": [
            "De anti-immuunziekte van Brussel maakt dat we arm worden",
            "De anti-immuunziekte van onze overheid slaat toe",
            "Zij doden hun levensader",
        ],
        "kop_label": "DE DIAGNOSE — ONDERAAN",
        "kop_titel": "Anti-immuunziekte — Brussel én Den Haag",
        "kop_lead": "Aan het einde — de diagnose, niet als aanval, maar als beschrijving van het ziektebeeld.",
    },
    "de": {
        "path": "de/was-aufkommt/index.html",
        "markers": [
            "Die Anti-Immunkrankheit Brüssels macht uns arm",
            "Die Autoimmunkrankheit unserer Regierung schlägt zu",
            "Sie töten ihre Lebensader",
        ],
        "kop_label": "DIE DIAGNOSE — AM ENDE",
        "kop_titel": "Anti-Immunkrankheit — Brüssel und Den Haag",
        "kop_lead": "Am Ende — die Diagnose, kein Angriff, sondern die Beschreibung des Krankheitsbildes.",
    },
    "en": {
        "path": "en/what-surfaces/index.html",
        "markers": [
            "The anti-immune disease of Brussels is making us poor",
            "The autoimmune disease of our government strikes",
            "They kill their lifeline",
        ],
        "kop_label": "THE DIAGNOSIS — AT THE END",
        "kop_titel": "Anti-immune disease — Brussels and The Hague",
        "kop_lead": "At the end — the diagnosis, not as an attack, but as a description of the clinical picture.",
    },
    "ru": {
        "path": "ru/chto-vsplyvaet/index.html",
        "markers": [
            "Анти-иммунная болезнь Брюсселя делает нас бедными",
            "Аутоиммунная болезнь нашего правительства наносит удар",
            "Они убивают свою жизненную артерию",
        ],
        "kop_label": "ДИАГНОЗ — В КОНЦЕ",
        "kop_titel": "Анти-иммунная болезнь — Брюссель и Гаага",
        "kop_lead": "В конце — диагноз, не нападение, а описание клинической картины.",
    },
}

MARKER = "<!-- brussel-diagnose-onderaan v1 -->"

def kop_blok(t):
    return f'''
{MARKER}
<section style="max-width:100%;margin:3rem auto 1.5rem auto;padding:0 1.25rem;text-align:center;">
  <p style="font-size:0.8rem;letter-spacing:0.12em;text-transform:uppercase;color:#1c5760;margin:0 0 0.4rem 0;font-family:Georgia,serif;">{t["kop_label"]}</p>
  <h2 style="font-family:Georgia,serif;font-size:clamp(1.6rem,3.5vw,2.2rem);color:#1a1a1a;margin:0 0 0.6rem 0;font-weight:700;">{t["kop_titel"]}</h2>
  <p style="font-family:Georgia,serif;font-style:italic;color:#4a5263;max-width:760px;margin:0 auto;line-height:1.5;">{t["kop_lead"]}</p>
</section>
'''

def extract_sections(html, markers):
    """Vind en knip de <section>...</section> blokken die elke marker bevatten."""
    sections = []
    for marker in markers:
        idx = html.find(marker)
        if idx == -1:
            return None, html, marker
        sec_start = html.rfind("<section", 0, idx)
        if sec_start == -1:
            return None, html, marker
        sec_end = html.find("</section>", idx) + len("</section>")
        if sec_end < 0:
            return None, html, marker
        sections.append((sec_start, sec_end))
    sections.sort()
    parts, extracted = [], []
    last = 0
    for s, e in sections:
        parts.append(html[last:s])
        extracted.append(html[s:e])
        last = e
    parts.append(html[last:])
    return "\n\n".join(extracted), "".join(parts), None

changed, skipped = [], []
for lang, t in PAGES.items():
    path = REPO / t["path"]
    if not path.exists():
        skipped.append(f"MISSING: {path}")
        continue
    html = path.read_text(encoding="utf-8")
    if MARKER in html:
        skipped.append(f"already moved: {path}")
        continue
    extracted, new_html, missing_marker = extract_sections(html, t["markers"])
    if extracted is None:
        skipped.append(f"marker not found ({missing_marker}): {path}")
        continue
    m_footer = re.search(r'(\s*<footer)', new_html)
    if not m_footer:
        skipped.append(f"no footer: {path}")
        continue
    insert_idx = m_footer.start()
    new_html = (
        new_html[:insert_idx]
        + "\n" + kop_blok(t)
        + "\n" + extracted
        + "\n"
        + new_html[insert_idx:]
    )
    path.write_text(new_html, encoding="utf-8")
    changed.append(t["path"])

print(f"=== Verplaatst ({len(changed)}) ===")
for c in changed: print(" -", c)
print(f"\n=== SKIPPED ({len(skipped)}) ===")
for s in skipped: print(" -", s)
