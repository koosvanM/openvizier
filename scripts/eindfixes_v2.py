#!/usr/bin/env python3
"""Eind-fixes v2 — corrigeer vorige fouten."""
import re, json
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# 1) Verwijder routes naar niet-bestaande methodologie-bestanden in DE/EN/RU/ES/FR/IT/PT
# (NL behouden: nl/_data/tabellen/2_routes_nl.json wijst correct naar wat-opkomt/de-methodologie-van-de-aanpassing.html)
TAB = REPO / "nl/_data/tabellen"
for lang in ["de", "en", "ru", "es", "fr", "it", "pt"]:
    rt = TAB / f"2_routes_{lang}.json"
    if not rt.exists(): continue
    data = json.loads(rt.read_text())
    # Verwijder 'X.1.1.1' route (voedingslijn) want vertaling bestaat niet meer
    # Prefix per taal
    prefix_map = {"de":"2","en":"3","ru":"4","es":"6","fr":"5","it":"7","pt":"8"}
    code_to_remove = f"{prefix_map[lang]}.1.1.1"
    before = len(data["rijen"])
    data["rijen"] = [r for r in data["rijen"] if r.get("code") != code_to_remove]
    after = len(data["rijen"])
    if before != after:
        rt.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {lang}: route {code_to_remove} verwijderd")

# 2) Repareer de eerder verkeerd-gefixte hrefs
fixes = [
    # bildung-manifest bestaat niet — wijzig naar bildung-wahle-eine-seite (het opvolger-artikel)
    ("de/was-aufkommt/sie-toeten-ihre-lebensader.html", "../ausgabe-2/bildung-manifest.html", "../ausgabe-2/bildung-wahle-eine-seite.html"),
    ("de/was-aufkommt/die-autoimmunkrankheit-schlaegt-zu.html", "../ausgabe-2/bildung-manifest.html", "../ausgabe-2/bildung-wahle-eine-seite.html"),
    # 7d-framework bestaat niet — wijzig naar dimensions.html (EN)
    ("en/index.html", "edition-1/7d-framework.html", "edition-1/dimensions.html"),
    ("en/index-klassiek.html", "edition-1/7d-framework.html", "edition-1/dimensions.html"),
    # 7d-konceptualnaya-ramka bestaat niet — wijzig naar sem-izmerenij.html (RU)
    ("ru/index.html", "vypusk-1/7d-konceptualnaya-ramka.html", "vypusk-1/sem-izmerenij.html"),
    ("ru/index-klassiek.html", "vypusk-1/7d-konceptualnaya-ramka.html", "vypusk-1/sem-izmerenij.html"),
]

veranderd = 0
for rel, old, new in fixes:
    p = REPO / rel
    if not p.exists(): continue
    content = p.read_text(encoding="utf-8")
    orig = content
    for q in ['"', "'"]:
        content = content.replace(f'href={q}{old}{q}', f'href={q}{new}{q}')
    if content != orig:
        p.write_text(content, encoding="utf-8")
        veranderd += 1
        print(f"  {rel}: {old} -> {new}")
print(f"\nTotaal: {veranderd} bestanden gerepareerd")
