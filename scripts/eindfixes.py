#!/usr/bin/env python3
"""Eind-fixes voor de laatste broken links."""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# 1) Verwijder NL-bestand "de-methodologie-van-de-aanpassing.html" uit niet-NL taalmappen
te_verwijderen = [
    "pt/o-que-emerge/de-methodologie-van-de-aanpassing.html",
    "it/cio-che-emerge/de-methodologie-van-de-aanpassing.html",
    "es/lo-que-emerge/de-methodologie-van-de-aanpassing.html",
    "fr/ce-qui-emerge/de-methodologie-van-de-aanpassing.html",
    "ru/chto-vsplyvaet/de-methodologie-van-de-aanpassing.html",
    "en/what-surfaces/de-methodologie-van-de-aanpassing.html",
    "de/was-aufkommt/de-methodologie-van-de-aanpassing.html",
]
verwijderd = 0
for rel in te_verwijderen:
    f = REPO / rel
    if f.exists():
        f.unlink()
        verwijderd += 1
        print(f"  verwijderd: {rel}")
print(f"\n{verwijderd} NL-rommel-bestanden verwijderd")

# 2) Vervang specifieke broken hrefs één-op-één
fixes = {
    # NL: wat-opkomt/delen.html bestaat niet, moet ../delen.html zijn vanaf wat-opkomt-artikel
    ("nl/navigatie.html", "wat-opkomt/delen.html", "delen.html"),
    ("nl/wat-opkomt/de-methodologie-van-de-aanpassing.html", "/nl/wat-opkomt/delen.html", "/nl/delen.html"),
    # DE: onderwijs-manifest -> bildung-manifest
    ("de/was-aufkommt/sie-toeten-ihre-lebensader.html", "../ausgabe-2/onderwijs-manifest.html", "../ausgabe-2/bildung-manifest.html"),
    ("de/was-aufkommt/die-autoimmunkrankheit-schlaegt-zu.html", "../ausgabe-2/onderwijs-manifest.html", "../ausgabe-2/bildung-manifest.html"),
    # EN: denkraam-7d -> 7d-framework
    ("en/index.html", "edition-1/denkraam-7d.html", "edition-1/7d-framework.html"),
    ("en/index-klassiek.html", "edition-1/denkraam-7d.html", "edition-1/7d-framework.html"),
    # RU: denkraam-7d -> 7d-konceptualnaya-ramka
    ("ru/index.html", "vypusk-1/denkraam-7d.html", "vypusk-1/7d-konceptualnaya-ramka.html"),
    ("ru/index-klassiek.html", "vypusk-1/denkraam-7d.html", "vypusk-1/7d-konceptualnaya-ramka.html"),
    # IT: gevolgenkaart-iii bestaat niet vertaald, fallback naar NL
    ("it/cio-che-emerge/die-konsequenzkarte.html", "mappa-delle-conseguenze-iii-analisi-silenziosa.html", "../../nl/wat-opkomt/gevolgenkaart-iii-stille-analyse.html"),
}

# Werk in batches per bestand
from collections import defaultdict
per_file = defaultdict(list)
for rel, old, new in fixes:
    per_file[rel].append((old, new))

veranderd_files = 0
veranderd_hrefs = 0
for rel, swaps in per_file.items():
    p = REPO / rel
    if not p.exists():
        print(f"BESTAAT NIET: {rel}")
        continue
    content = p.read_text(encoding="utf-8")
    orig = content
    for old, new in swaps:
        # Vervang in href="..." en href='...'
        for q in ['"', "'"]:
            content = content.replace(f'href={q}{old}{q}', f'href={q}{new}{q}')
        # Geweidigt: ook gevallen zonder quote-prefix (edge)
    if content != orig:
        p.write_text(content, encoding="utf-8")
        veranderd_files += 1
        veranderd_hrefs += sum(1 for _ in swaps)
        print(f"  bijgewerkt: {rel}")

print(f"\nTotaal: {veranderd_files} bestanden, {veranderd_hrefs} hrefs vervangen")
