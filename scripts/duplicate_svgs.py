#!/usr/bin/env python3
"""Dupliceer alle relevante NL-SVG's naar taalspecifieke kopieën:
   foo.svg → foo.de.svg, foo.en.svg, foo.ru.svg
   Subagents vertalen vervolgens de tekstinhoud van elke kopie."""
import shutil
from pathlib import Path

REPO = Path("/tmp/gh-repo")
SVGS = [
    "assets/wat-opkomt/actor-vervanging/hero-actor-vervanging.svg",
    "assets/wat-opkomt/actor-vervanging/medisch-politiek-tableau.svg",
    "assets/wat-opkomt/actor-vervanging/revolutie-routekaart.svg",
    "assets/wat-opkomt/stikstof-slaat-toe/twee-scenarios.svg",
    "assets/wat-opkomt/stikstof-slaat-toe/hero-stikstof-slaat-toe.svg",
    "assets/wat-opkomt/immuunsysteem/hero-immuunsysteem.svg",
    "assets/wat-opkomt/brussel-arm/hero-brussel-arm.svg",
    "assets/wat-opkomt/brussel-aders/hero-brussel-aders.svg",
    "assets/wat-opkomt/voedingslijn/hero-voedingslijn.svg",
    "assets/wat-opkomt/levensader/hero-levensader.svg",
    "assets/wat-opkomt/voedingslijn/illustratie-kompas-verouderd.svg",
    "assets/wat-opkomt/voedingslijn/illustratie-tempo-verschil.svg",
    "assets/diagrams/7d-dimensions.svg",
    "assets/diagrams/samenhang-stromingen.svg",
    "assets/wat-opkomt/voedingslijn/illustratie-wachtkamer-bestuurders.svg",
    "assets/diagrams/seaskin-grenslaag.svg",
]
LANGS = ["de", "en", "ru"]

created = []
for s in SVGS:
    src = REPO / s
    if not src.exists():
        print(f"MISSING: {s}")
        continue
    for lang in LANGS:
        dst = src.with_suffix(f".{lang}.svg")
        shutil.copy(src, dst)
        created.append(str(dst.relative_to(REPO)))

print(f"Aangemaakt: {len(created)} bestanden")
for c in created[:6]: print(" -", c)
print("...")
