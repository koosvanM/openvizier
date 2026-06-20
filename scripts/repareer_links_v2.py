#!/usr/bin/env python3
"""
V2 — voorzichtige link-reparatie.

Regels:
1. Alleen hrefs binnen DEZE taal vervangen (geen ../../<andere_taal>/... paden).
2. Voor elke href, eerst checken of het pad bestaat. Zo ja: NIET aanraken.
3. Pas slug-substitutie alleen toe als het pad NU broken is.
4. Voor cross-taal-links (../../nl/...) niets doen.

Werkwijze:
- Doorloop ELK <a href="..."> in elke pagina van een taal X.
- Resolveer href naar absoluut repo-pad.
- Als bestaat: skip.
- Anders: probeer slug-rules van taal X toe te passen op het basename.
- Test nieuwe pad. Als bestaat: vervang. Anders: rapporteer als nog-broken.
"""
import re
import json
from pathlib import Path
from urllib.parse import unquote

REPO = Path("/tmp/gh-repo")

# Verzamel alle bestaande paden
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
    if (p + "/") in existing: return True
    if (p + ".html") in existing: return True
    return False

# Slug-mapping per taal: NL-stem -> taal-stem (zonder .html)
# Toepasbaar op basename van link-targets binnen dezelfde taalmap.
SLUG_TRANSLATIONS = {
    "de": {
        "delen": "teilen", "over": "ueber", "colofon": "impressum",
        "archief": "archiv",
        "erkunden": "verkennen",  # special: bestand heet verkennen.html
        "de-grote-plundering": "die-grosse-pluenderung",
        "the-great-plunder": "die-grosse-pluenderung",
        "europa-hoeft-geen-schadekaart-te-zijn": "europa-muss-keine-schadenskarte-sein",
        "onderwijs-manifest": "bildung-manifest",
        "voorwoord": "vorwort",
        "denkraam-7d": "7d-denkraum",
    },
    "en": {
        "delen": "share", "over": "about", "colofon": "colophon",
        "archief": "archive", "idee": "idea",
        "de-grote-plundering": "the-great-plunder",
        "europa-hoeft-geen-schadekaart-te-zijn": "europe-need-not-be-a-damage-map",
        "voorwoord": "foreword",
        "denkraam-7d": "7d-framework",
    },
    "ru": {
        "delen": "podelitsya", "over": "o-gazete", "colofon": "vykhodnye-dannye",
        "archief": "arkhiv", "idee": "ideya",
        "de-grote-plundering": "velikoe-razgrablenie",
        "voorwoord": "predislovie",
        "denkraam-7d": "7d-konceptualnaya-ramka",
    },
    "es": {"delen": "share", "europa-hoeft-geen-schadekaart-te-zijn": None, "the-great-plunder": None, "de-grote-plundering": None},
    "fr": {"delen": "share", "europa-hoeft-geen-schadekaart-te-zijn": None, "the-great-plunder": None, "de-grote-plundering": None},
    "it": {"delen": "share", "europa-hoeft-geen-schadekaart-te-zijn": None, "the-great-plunder": None, "de-grote-plundering": None, "la-mappa-delle-conseguenze": None},
    "pt": {"delen": "share", "europa-hoeft-geen-schadekaart-te-zijn": None, "the-great-plunder": None, "de-grote-plundering": None},
}

# Mapnaam-vertaling (deel van pad: editie-X -> ausgabe-X etc.)
DIR_TRANSLATIONS = {
    "de": {"wat-opkomt": "was-aufkommt", "editie-0": "ausgabe-0", "editie-1": "ausgabe-1",
           "editie-2": "ausgabe-2", "editie-3": "ausgabe-3", "editie-4": "ausgabe-4",
           "editie-5": "ausgabe-5", "editie-6": "ausgabe-6", "onderzoek": "forschung"},
    "en": {"wat-opkomt": "what-surfaces", "editie-0": "edition-0", "editie-1": "edition-1",
           "editie-2": "edition-2", "editie-3": "edition-3", "editie-4": "edition-4",
           "editie-5": "edition-5", "editie-6": "edition-6", "onderzoek": "research"},
    "ru": {"wat-opkomt": "chto-vsplyvaet", "editie-0": "vypusk-0", "editie-1": "vypusk-1",
           "editie-2": "vypusk-2", "editie-3": "vypusk-3", "editie-4": "vypusk-4",
           "editie-5": "vypusk-5", "editie-6": "vypusk-6", "onderzoek": "issledovanie"},
    "es": {"wat-opkomt": "lo-que-emerge", "editie-0": "edicion-0"},
    "fr": {"wat-opkomt": "ce-qui-emerge", "editie-0": "edition-0"},
    "it": {"wat-opkomt": "cio-che-emerge", "editie-0": "edizione-0"},
    "pt": {"wat-opkomt": "o-que-emerge", "editie-0": "edicao-0"},
}


def kandidate_paden(href, html_path, lang):
    """Genereer kandidaat-paden om te proberen, op volgorde."""
    parent = html_path.parent
    candidates = []

    # Origineel
    try:
        orig = (parent / href).resolve().relative_to(REPO).as_posix()
        candidates.append(("origineel", href, orig))
    except (ValueError, OSError):
        pass

    # Slug-substitutie binnen dezelfde href
    new_href = href
    # 1. Map-vervanging (alleen als de href NIET cross-taal is)
    if not re.search(r'(?:^|/)\.\.\/\.\.\/[a-z]{2}\/', href):
        for nl_dir, target_dir in DIR_TRANSLATIONS.get(lang, {}).items():
            new_href = re.sub(rf'(^|/){re.escape(nl_dir)}(/|$)', rf'\1{target_dir}\2', new_href)
    # 2. Basename-vertaling
    if "/" in new_href:
        path_part, base = new_href.rsplit("/", 1)
    else:
        path_part, base = "", new_href
    base_stem = base.rsplit(".html", 1)[0] if base.endswith(".html") else base
    if base_stem in SLUG_TRANSLATIONS.get(lang, {}):
        translated = SLUG_TRANSLATIONS[lang][base_stem]
        if translated:  # niet None
            new_base = translated + ".html" if base.endswith(".html") else translated
            new_href = (path_part + "/" if path_part else "") + new_base
    if new_href != href:
        try:
            resolved = (parent / new_href).resolve().relative_to(REPO).as_posix()
            candidates.append(("slug-vertaald", new_href, resolved))
        except (ValueError, OSError):
            pass

    return candidates


def repareer(lang):
    base = REPO / lang
    if not base.exists():
        return 0, 0
    n_fixed = 0
    n_changed_files = 0
    for html_path in base.rglob("*.html"):
        content = html_path.read_text(encoding="utf-8", errors="replace")
        original = content

        def replace(m):
            nonlocal n_fixed
            quote = m.group(1)
            href = m.group(2)
            # Skip externe en speciale
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")) or not href:
                return m.group(0)
            clean = href.split("#")[0].split("?")[0]
            if not clean: return m.group(0)
            anker = href[len(clean):]  # eventuele #anker of ?query

            cands = kandidate_paden(clean, html_path, lang)
            if not cands:
                return m.group(0)
            # eerste kandidaat = origineel; check of bestaat
            _, _, orig_resolved = cands[0]
            if path_exists(orig_resolved):
                return m.group(0)  # origineel werkt, niet aanraken
            # Probeer slug-vertaalde varianten
            for label, new_href, resolved in cands[1:]:
                if path_exists(resolved):
                    n_fixed += 1
                    return f'href={quote}{new_href}{anker}{quote}'
            return m.group(0)  # niets gevonden, laat staan

        content = re.sub(r'''href=(["'])([^"']+)\1''', replace, content)
        if content != original:
            html_path.write_text(content, encoding="utf-8")
            n_changed_files += 1
    return n_changed_files, n_fixed

print("Reparatie per taal...")
totaal_files = 0
totaal_fixed = 0
for lang in ["de", "en", "ru", "es", "fr", "it", "pt"]:
    files, fixed = repareer(lang)
    print(f"  {lang}: {files} bestanden, {fixed} hrefs gerepareerd")
    totaal_files += files
    totaal_fixed += fixed

print(f"\nTotaal: {totaal_files} bestanden, {totaal_fixed} hrefs gerepareerd")
