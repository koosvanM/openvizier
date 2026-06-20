#!/usr/bin/env python3
"""
Bed de Verkenner in op de voorpagina van alle 4 hoofdtalen (NL/DE/EN/RU),
direct na het hoofdmenu en vóór de eerste section.

Implementatie: <iframe> dat verkennen.html laadt — geen JS-conflict, geen
CSS-conflict, volledig functioneel.
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

MARKER = "<!-- verkennen-embed v1 -->"

# Per taal: label en bestandsnaam (verkennen.html staat overal in elke taal)
LANGS = {
    "nl": {
        "kop_label": "Verkennen",
        "kop_titel": "De landkaart van Het Open Vizier",
        "kop_lead": "Klik door de lagen — van actualiteit tot dossier, van editie tot onderzoek.",
        "cta": "Open de volledige Verkenner →",
    },
    "de": {
        "kop_label": "Erkunden",
        "kop_titel": "Die Landkarte von Het Open Vizier",
        "kop_lead": "Klicken Sie sich durch die Schichten — von Aktualität bis Dossier, von Ausgabe bis Forschung.",
        "cta": "Den vollständigen Erkunder öffnen →",
    },
    "en": {
        "kop_label": "Explore",
        "kop_titel": "The map of The Open Visor",
        "kop_lead": "Click through the layers — from current events to dossier, from edition to research.",
        "cta": "Open the full Explorer →",
    },
    "ru": {
        "kop_label": "Исследовать",
        "kop_titel": "Карта «Открытого забрала»",
        "kop_lead": "Кликайте по слоям — от актуальных событий до досье, от выпуска до исследования.",
        "cta": "Открыть полный Исследователь →",
    },
    "es": {
        "kop_label": "Explorar",
        "kop_titel": "El mapa de Het Open Vizier",
        "kop_lead": "Recorra las capas — de la actualidad al dosier, de la edición a la investigación.",
        "cta": "Abrir el Explorador completo →",
    },
    "fr": {
        "kop_label": "Explorer",
        "kop_titel": "La carte de Het Open Vizier",
        "kop_lead": "Parcourez les couches — de l'actualité au dossier, de l'édition à la recherche.",
        "cta": "Ouvrir l'Explorateur complet →",
    },
    "it": {
        "kop_label": "Esplorare",
        "kop_titel": "La mappa di Het Open Vizier",
        "kop_lead": "Attraversa gli strati — dall'attualità al dossier, dall'edizione alla ricerca.",
        "cta": "Apri l'Esploratore completo →",
    },
    "pt": {
        "kop_label": "Explorar",
        "kop_titel": "O mapa de Het Open Vizier",
        "kop_lead": "Percorra as camadas — da atualidade ao dossiê, da edição à investigação.",
        "cta": "Abrir o Explorador completo →",
    },
}


def build_embed(t):
    return f'''
{MARKER}
<section class="verkennen-embed" style="background:#faf8f3;padding:2.5rem 1.5rem 3rem;border-top:1px solid #d4d1ca;border-bottom:1px solid #d4d1ca;">
  <div style="max-width:1200px;margin:0 auto;">
    <div style="text-align:center;margin-bottom:1.5rem;">
      <p style="font-size:0.78rem;letter-spacing:0.15em;text-transform:uppercase;color:#1c5760;margin:0 0 0.5rem 0;font-family:Georgia,serif;font-weight:600;">★ {t["kop_label"]}</p>
      <h2 style="font-family:Georgia,serif;font-size:clamp(1.7rem,3.6vw,2.3rem);color:#1a1a1a;margin:0 0 0.7rem 0;font-weight:700;font-style:italic;">{t["kop_titel"]}</h2>
      <p style="font-family:Georgia,serif;font-style:italic;color:#4a5263;max-width:720px;margin:0 auto;line-height:1.6;">{t["kop_lead"]}</p>
    </div>
    <div style="position:relative;width:100%;height:70vh;min-height:520px;max-height:780px;border-radius:8px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.15);">
      <iframe src="verkennen-embed.html"
              title="{t["kop_titel"]}"
              loading="lazy"
              style="position:absolute;inset:0;width:100%;height:100%;border:0;display:block;"></iframe>
    </div>
    <p style="text-align:center;margin:1.2rem 0 0;">
      <a href="verkennen.html" style="color:#1c5760;text-decoration:none;font-weight:700;border-bottom:1px solid #1c5760;padding-bottom:1px;font-family:Georgia,serif;">{t["cta"]}</a>
    </p>
  </div>
</section>
'''


changed = []
for lang, t in LANGS.items():
    path = REPO / lang / "index.html"
    if not path.exists():
        print(f"MISSING: {path}")
        continue
    html = path.read_text(encoding="utf-8")
    if MARKER in html:
        print(f"  al ingebed: {lang}/index.html")
        continue
    # Vind insertion-point: na </nav>, vóór de eerste <section.
    # Probeer </nav><section> (NL/DE/EN/RU patroon) of </nav><main> (ES/FR/IT/PT)
    m = re.search(r'(</nav>)\s*(<section|<main)', html)
    if not m:
        print(f"  insertion-point niet gevonden: {lang}/index.html")
        continue
    embed = build_embed(t)
    # Voor ES/FR/IT/PT: invoegen NA <main> zodat de iframe in de main-container valt
    if m.group(2) == '<main':
        # Vind eind van <main ...> tag
        main_end = html.find('>', m.start(2)) + 1
        new_html = html[:main_end] + "\n\n" + embed + "\n" + html[main_end:]
    else:
        new_html = html[:m.end(1)] + "\n\n" + embed + "\n" + html[m.end(1):]
    path.write_text(new_html, encoding="utf-8")
    changed.append(f"{lang}/index.html")

print(f"\n=== Ingebed ({len(changed)}) ===")
for c in changed: print(f"  - {c}")
