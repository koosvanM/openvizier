#!/usr/bin/env python3
"""
Verplaats de twee Brussel-opener-secties van BOVEN naar ONDER in alle 8 editie-Europa
landingpagina's. Ze komen direct vóór de <footer> staan.

Identificatie: secties met de twee Brussel-artikel-titels (per taal), met inline-style
attributen die uniek zijn voor deze opener-blokken.
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# Per taal: (pad, herkenningskenmerken voor de twee secties)
PAGES = {
    "nl": {
        "path": "nl/editie-0/index.html",
        "art1_marker": "De anti-immuunziekte van Brussel maakt dat we arm worden",
        "art2_marker": "Zij doden hun levensaders",
        "kop_label": "DE TWEE BRUSSEL-ARTIKELEN",
        "kop_titel": "De anti-immuunziekte van Brussel",
        "kop_lead": "Aan het einde van deze editie — de diagnose, niet als aanval, maar als beschrijving van het ziektebeeld.",
    },
    "de": {
        "path": "de/ausgabe-0/index.html",
        "art1_marker": "Die Anti-Immunkrankheit Brüssels macht uns arm",
        "art2_marker": "Sie töten ihre Lebensadern",
        "kop_label": "DIE ZWEI BRÜSSEL-ARTIKEL",
        "kop_titel": "Die Anti-Immunkrankheit Brüssels",
        "kop_lead": "Am Ende dieser Ausgabe — die Diagnose, kein Angriff, sondern die Beschreibung des Krankheitsbildes.",
    },
    "en": {
        "path": "en/edition-0/index.html",
        "art1_marker": "The anti-immune disease of Brussels is making us poor",
        "art2_marker": "They kill their lifelines",
        "kop_label": "THE TWO BRUSSELS ARTICLES",
        "kop_titel": "The anti-immune disease of Brussels",
        "kop_lead": "At the end of this edition — the diagnosis, not as an attack, but as a description of the clinical picture.",
    },
    "ru": {
        "path": "ru/vypusk-0/index.html",
        "art1_marker": "Анти-иммунная болезнь Брюсселя делает нас бедными",
        "art2_marker": "Они убивают свои жизненные артерии",
        "kop_label": "ДВЕ СТАТЬИ О БРЮССЕЛЕ",
        "kop_titel": "Анти-иммунная болезнь Брюсселя",
        "kop_lead": "В конце выпуска — диагноз, не нападение, а описание клинической картины.",
    },
    "es": {
        "path": "es/edicion-0/index.html",
        "art1_marker": "La enfermedad anti-inmune de Bruselas nos empobrece",
        "art2_marker": "Matan sus arterias vitales",
        "kop_label": "LOS DOS ARTÍCULOS DE BRUSELAS",
        "kop_titel": "La enfermedad anti-inmune de Bruselas",
        "kop_lead": "Al final de esta edición — el diagnóstico, no como un ataque, sino como descripción del cuadro clínico.",
    },
    "fr": {
        "path": "fr/edition-0/index.html",
        "art1_marker": "La maladie anti-immunitaire de Bruxelles nous appauvrit",
        "art2_marker": "Ils tuent leurs artères vitales",
        "kop_label": "LES DEUX ARTICLES SUR BRUXELLES",
        "kop_titel": "La maladie anti-immunitaire de Bruxelles",
        "kop_lead": "À la fin de cette édition — le diagnostic, non comme attaque, mais comme description du tableau clinique.",
    },
    "it": {
        "path": "it/edizione-0/index.html",
        "art1_marker": "La malattia anti-immune di Bruxelles ci impoverisce",
        "art2_marker": "Uccidono le loro arterie vitali",
        "kop_label": "I DUE ARTICOLI SU BRUXELLES",
        "kop_titel": "La malattia anti-immune di Bruxelles",
        "kop_lead": "Alla fine di questa edizione — la diagnosi, non un attacco, ma una descrizione del quadro clinico.",
    },
    "pt": {
        "path": "pt/edicao-0/index.html",
        "art1_marker": "A doença anti-imune de Bruxelas empobrece-nos",
        "art2_marker": "Matam as suas artérias vitais",
        "kop_label": "OS DOIS ARTIGOS SOBRE BRUXELAS",
        "kop_titel": "A doença anti-imune de Bruxelas",
        "kop_lead": "No final desta edição — o diagnóstico, não como ataque, mas como descrição do quadro clínico.",
    },
}

MARKER = "<!-- brussel-onderaan v1 -->"

def kop_blok(t):
    """Sectie-titel die boven de twee Brussel-blokken op het einde komt."""
    return f'''
{MARKER}
<section style="max-width:1280px;margin:3rem auto 1.5rem auto;padding:0 1.25rem;text-align:center;">
  <p style="font-size:0.8rem;letter-spacing:0.12em;text-transform:uppercase;color:#1c5760;margin:0 0 0.4rem 0;font-family:Georgia,serif;">{t["kop_label"]}</p>
  <h2 style="font-family:Georgia,serif;font-size:clamp(1.6rem,3.5vw,2.2rem);color:#1a1a1a;margin:0 0 0.6rem 0;font-weight:700;">{t["kop_titel"]}</h2>
  <p style="font-family:Georgia,serif;font-style:italic;color:#4a5263;max-width:760px;margin:0 auto;line-height:1.5;">{t["kop_lead"]}</p>
</section>
'''

def extract_two_sections(html, art1_marker, art2_marker):
    """Vind en knip de twee <section>...</section> blokken die de Brussel-openers bevatten."""
    # Volledige <section ...>...</section> blokken (zoekt naar buitenste niveau)
    # Strategie: zoek positie van marker, vind de <section> die ervoor staat en de bijbehorende </section>
    sections = []
    for marker in [art1_marker, art2_marker]:
        idx = html.find(marker)
        if idx == -1:
            return None, html  # niet gevonden
        # Loop terug naar de openende <section ...>
        sec_start = html.rfind("<section", 0, idx)
        if sec_start == -1:
            return None, html
        # Vind de bijbehorende </section> ná het marker — eenvoudig: eerste </section> na idx
        sec_end = html.find("</section>", idx) + len("</section>")
        if sec_end < 0:
            return None, html
        # Extracteer het comment net boven (optioneel)
        # Kijk of er een HTML-comment direct boven de <section> staat
        comment_start = html.rfind("<!--", max(0, sec_start - 200), sec_start)
        if comment_start != -1:
            comment_end = html.find("-->", comment_start) + 3
            if comment_end > 0 and comment_end <= sec_start + 1:
                sec_start = comment_start  # neem comment mee
        sections.append((sec_start, sec_end))
    sections.sort()
    # Bouw nieuwe HTML: knip beide secties eruit
    parts = []
    last = 0
    extracted = []
    for s, e in sections:
        parts.append(html[last:s])
        extracted.append(html[s:e])
        last = e
    parts.append(html[last:])
    new_html = "".join(parts)
    extracted_block = "\n\n".join(extracted)
    return extracted_block, new_html

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
    extracted, new_html = extract_two_sections(html, t["art1_marker"], t["art2_marker"])
    if extracted is None:
        skipped.append(f"markers not found: {path}")
        continue
    # Plaats opnieuw vóór <footer>
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
