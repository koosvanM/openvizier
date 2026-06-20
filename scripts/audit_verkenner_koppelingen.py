#!/usr/bin/env python3
"""
Audit alle Verkenner-knopen over alle 8 talen.

Voor elke artikel-knoop (type=artikel of equivalent) in 1_knopen.json:
- Heeft het een URL in 2_routes_<lang>.json?
- Bestaat het pad waarnaar de URL wijst echt?
- Is er een tekst (naam + ondertitel) voor de taal in 4_teksten_<lang>.json?

Rapporteer per taal:
- Aantal eindknopen (geen kinderen)
- Aantal met werkende URL
- Aantal zonder URL
- Aantal met broken URL
"""
import json
from pathlib import Path
from collections import defaultdict

REPO = Path("/tmp/gh-repo")
TAB = REPO / "nl/_data/tabellen"

# Verzamel bestaande paden
existing = set()
for f in REPO.rglob("*"):
    if f.is_file():
        existing.add(f.relative_to(REPO).as_posix())

def path_exists(p):
    p = p.lstrip("/")
    if not p: return True
    if p in existing: return True
    if p.endswith("/"):
        return (p + "index.html") in existing
    if (p + "/index.html") in existing: return True
    if (p + ".html") in existing: return True
    return False

knopen = json.loads((TAB / "1_knopen.json").read_text())["rijen"]

# Per taal de routes en teksten laden
PREFIX = {"nl": "1", "de": "2", "en": "3", "ru": "4", "fr": "5", "es": "6", "it": "7", "pt": "8"}
LANGS = list(PREFIX.keys())

routes_per_lang = {}
teksten_per_lang = {}
for lang in LANGS:
    rt = TAB / f"2_routes_{lang}.json"
    tk = TAB / f"4_teksten_{lang}.json"
    if rt.exists():
        routes_per_lang[lang] = {r["code"]: r for r in json.loads(rt.read_text())["rijen"]}
    if tk.exists():
        teksten_per_lang[lang] = {r["code"]: r for r in json.loads(tk.read_text())["rijen"]}

# Bepaal welke codes per taal artikel-knopen zijn (eindknopen of intern)
# Een artikel-knoop = leaf (geen kinderen in 1_knopen) OF heeft type='artikel'
# We nemen alles binnen taalwortel (X.*) en checken of het een leaf is
all_codes = {r["code"] for r in knopen if r.get("code")}
parent_to_kids = defaultdict(list)
for r in knopen:
    code = r.get("code")
    if not code: continue
    parts = code.split(".")
    if len(parts) > 1:
        parent = ".".join(parts[:-1])
        parent_to_kids[parent].append(code)

# Rapporteer per taal
rapport = {}
for lang, prefix in PREFIX.items():
    # Eindknopen in deze taal = codes die met prefix beginnen en GEEN kinderen hebben
    eindknopen = []
    for code in all_codes:
        if not code.startswith(prefix + "."):
            continue
        if code in parent_to_kids:
            continue  # heeft kinderen, is geen leaf
        eindknopen.append(code)

    werkend = []
    geen_url = []
    broken_url = []
    geen_naam = []
    routes = routes_per_lang.get(lang, {})
    teksten = teksten_per_lang.get(lang, {})

    for code in eindknopen:
        # Heeft het een naam?
        if code not in teksten or not teksten[code].get("naam"):
            geen_naam.append(code)
        # Heeft het een url-route?
        r = routes.get(code, {})
        url = r.get("url")
        if not url:
            geen_url.append(code)
            continue
        # Url wijst naar wat? Routes-url is relatief aan /<lang>/verkennen.html.
        # Resolveer netjes: combineer met de directory van verkennen.html (= <lang>/).
        if url.startswith("/"):
            test_pad = url[1:]
        else:
            # base = <lang>/, dus combineer en normaliseer
            import posixpath
            test_pad = posixpath.normpath(posixpath.join(f"{lang}/", url))
            if test_pad.startswith("./"):
                test_pad = test_pad[2:]
        if path_exists(test_pad):
            werkend.append(code)
        else:
            broken_url.append((code, url))

    rapport[lang] = {
        "eindknopen": len(eindknopen),
        "werkend": len(werkend),
        "geen_url": geen_url,
        "broken_url": broken_url,
        "geen_naam": geen_naam,
    }

# Print
totaal_eind = totaal_werk = totaal_geen = totaal_broken = 0
for lang in LANGS:
    r = rapport[lang]
    n_geen = len(r["geen_url"])
    n_broken = len(r["broken_url"])
    print(f"=== {lang.upper()} ===  eindknopen={r['eindknopen']:3}  werkend={r['werkend']:3}  geen-url={n_geen:3}  broken={n_broken:2}  geen-naam={len(r['geen_naam']):2}")
    totaal_eind += r["eindknopen"]
    totaal_werk += r["werkend"]
    totaal_geen += n_geen
    totaal_broken += n_broken

print(f"\nTOTAAL: eindknopen={totaal_eind}, werkend={totaal_werk}, geen-url={totaal_geen}, broken={totaal_broken}")

# Toon details voor geen-url codes (top 20 per taal die niet 'concept' zijn)
print("\n=== DETAIL — top 10 'geen-url' per taal ===")
for lang in LANGS:
    geen = rapport[lang]["geen_url"][:10]
    if not geen: continue
    print(f"\n{lang.upper()}:")
    for code in geen:
        naam = teksten_per_lang[lang].get(code, {}).get("naam", "(geen naam)")
        # ouder uit code
        parts = code.split(".")
        ouder_code = ".".join(parts[:-1]) if len(parts) > 1 else None
        ouder_naam = teksten_per_lang[lang].get(ouder_code, {}).get("naam", "?") if ouder_code else "?"
        print(f"  {code:18} {naam[:35]:35} (in: {ouder_naam[:25]})")

# Broken URL's
print("\n=== BROKEN URLs ===")
for lang in LANGS:
    for code, url in rapport[lang]["broken_url"]:
        print(f"  {lang} {code:18} → {url}")
