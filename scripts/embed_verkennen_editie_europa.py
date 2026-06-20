#!/usr/bin/env python3
"""
Plaats een Verkenner-iframe direct op elke Editie-Europa landingpagina,
ingesteld om te openen op de subtree 'Editie 0 — Europa' (code X.1.3.1).

Wordt geplaatst direct na </nav> en vóór <main> of de eerste <section>.
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
MARKER = "<!-- verkennen-embed-editie-europa v1 -->"

LANGS = {
    "nl": {
        "pad": "nl/editie-0/index.html",
        "code": "1.1.3.1",
        "kop_label": "Verkennen",
        "kop_titel": "De landkaart van Editie Europa",
        "kop_lead": "Klik door de stukken — van diagnose tot recept, van scenario tot serie.",
        "cta": "Open de volledige Verkenner →",
    },
    "de": {
        "pad": "de/ausgabe-0/index.html",
        "code": "2.1.3.1",
        "kop_label": "Erkunden",
        "kop_titel": "Die Landkarte der Ausgabe Europa",
        "kop_lead": "Klicken Sie sich durch die Stücke — von Diagnose zu Rezept, von Szenario zur Serie.",
        "cta": "Den vollständigen Erkunder öffnen →",
    },
    "en": {
        "pad": "en/edition-0/index.html",
        "code": "3.1.3.1",
        "kop_label": "Explore",
        "kop_titel": "The map of Edition Europe",
        "kop_lead": "Click through the pieces — from diagnosis to recipe, from scenario to series.",
        "cta": "Open the full Explorer →",
    },
    "ru": {
        "pad": "ru/vypusk-0/index.html",
        "code": "4.1.3.1",
        "kop_label": "Исследовать",
        "kop_titel": "Карта выпуска «Европа»",
        "kop_lead": "Кликайте по материалам — от диагноза до рецепта, от сценария до серии.",
        "cta": "Открыть полный Исследователь →",
    },
    "es": {
        "pad": "es/edicion-0/index.html",
        "code": "6.1.3.1",
        "kop_label": "Explorar",
        "kop_titel": "El mapa de la Edición Europa",
        "kop_lead": "Recorra los textos — del diagnóstico a la receta, del escenario a la serie.",
        "cta": "Abrir el Explorador completo →",
    },
    "fr": {
        "pad": "fr/edition-0/index.html",
        "code": "5.1.3.1",
        "kop_label": "Explorer",
        "kop_titel": "La carte de l'Édition Europe",
        "kop_lead": "Parcourez les textes — du diagnostic à la recette, du scénario à la série.",
        "cta": "Ouvrir l'Explorateur complet →",
    },
    "it": {
        "pad": "it/edizione-0/index.html",
        "code": "7.1.3.1",
        "kop_label": "Esplorare",
        "kop_titel": "La mappa dell'Edizione Europa",
        "kop_lead": "Attraversa i testi — dalla diagnosi alla ricetta, dallo scenario alla serie.",
        "cta": "Apri l'Esploratore completo →",
    },
    "pt": {
        "pad": "pt/edicao-0/index.html",
        "code": "8.1.3.1",
        "kop_label": "Explorar",
        "kop_titel": "O mapa da Edição Europa",
        "kop_lead": "Percorra os textos — do diagnóstico à receita, do cenário à série.",
        "cta": "Abrir o Explorador completo →",
    },
}


def build_embed(t):
    # iframe-src: relatief, gaat één map omhoog naar de taal-root
    return f'''
{MARKER}
<section class="verkennen-embed" style="background:#faf8f3;padding:2.5rem 1.5rem 3rem;border-top:1px solid #d4d1ca;border-bottom:1px solid #d4d1ca;">
  <div style="max-width:1200px;margin:0 auto;">
    <div style="text-align:center;margin-bottom:1.5rem;">
      <p style="font-size:0.78rem;letter-spacing:0.15em;text-transform:uppercase;color:#1c5760;margin:0 0 0.5rem 0;font-family:Georgia,serif;font-weight:600;">★ {t["kop_label"]}</p>
      <h2 style="font-family:Georgia,serif;font-size:clamp(1.5rem,3.2vw,2.1rem);color:#1a1a1a;margin:0 0 0.7rem 0;font-weight:700;font-style:italic;">{t["kop_titel"]}</h2>
      <p style="font-family:Georgia,serif;font-style:italic;color:#4a5263;max-width:720px;margin:0 auto;line-height:1.6;">{t["kop_lead"]}</p>
    </div>
    <div style="position:relative;width:100%;height:65vh;min-height:480px;max-height:720px;border-radius:8px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.15);">
      <iframe src="../verkennen-embed.html#code={t["code"]}"
              title="{t["kop_titel"]}"
              loading="lazy"
              style="position:absolute;inset:0;width:100%;height:100%;border:0;display:block;"></iframe>
    </div>
    <p style="text-align:center;margin:1.2rem 0 0;">
      <a href="../verkennen.html#code={t["code"]}" style="color:#1c5760;text-decoration:none;font-weight:700;border-bottom:1px solid #1c5760;padding-bottom:1px;font-family:Georgia,serif;">{t["cta"]}</a>
    </p>
  </div>
</section>
'''


changed = []
skipped = []
for lang, t in LANGS.items():
    p = REPO / t["pad"]
    if not p.exists():
        skipped.append(f"MISSING: {p}")
        continue
    html = p.read_text(encoding="utf-8")
    if MARKER in html:
        skipped.append(f"al ingebed: {t['pad']}")
        continue
    # Anker: na </nav>, vóór <main> of eerste <section>
    m = re.search(r'(</nav>)\s*(<main|<section)', html)
    if not m:
        skipped.append(f"insertie-anker niet gevonden: {t['pad']}")
        continue
    embed = build_embed(t)
    if m.group(2) == "<main":
        # Voeg in NA <main ...>-tag
        main_end = html.find(">", m.start(2)) + 1
        new_html = html[:main_end] + "\n\n" + embed + "\n" + html[main_end:]
    else:
        new_html = html[:m.end(1)] + "\n\n" + embed + "\n" + html[m.end(1):]
    p.write_text(new_html, encoding="utf-8")
    changed.append(t["pad"])

print(f"=== Ingebed ({len(changed)}) ===")
for c in changed: print(f"  - {c}")
if skipped:
    print(f"\n=== Overgeslagen ({len(skipped)}) ===")
    for s in skipped: print(f"  - {s}")
