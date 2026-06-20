#!/usr/bin/env python3
"""Koppel de eind-knopen (leaves) van Editie Europa-tak naar artikelen.

Hiërarchie:
  X.1.3.1        Editie Europa (root)
  X.1.3.1.1      Diagnose Nederland (groep)
  X.1.3.1.1.1    -> artikel: De Grote Plundering         <-- LEAF
  X.1.3.1.2      Het instrument (groep)
  X.1.3.1.2.1    -> artikel: De Gevolgenkaart            <-- LEAF
  X.1.3.1.3      Europa cumulatief (groep)
  X.1.3.1.3.1    -> De Brusselse Gevolgenkaart           <-- LEAF
  X.1.3.1.3.2    -> Brusselse Gevolgenkaart BiCRS        <-- LEAF
  X.1.3.1.3.3    -> Mappa Tal Konsegwenzi                <-- LEAF
  X.1.3.1.3.4    -> De Op De Natuur Aangepaste Analyse   <-- LEAF
  X.1.3.1.4      De uitweg (groep)
  X.1.3.1.4.1    -> De Kantelmechanica                   <-- LEAF
  X.1.3.1.4.2    -> Nova Democratia Manifest             <-- LEAF
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TAB = REPO / "nl/_data/tabellen"

# suffix (na 'X.1.3.1.') -> pad per taal, relatief aan <lang>/verkennen.html
ROUTES = {
    "1.1": {  # De Grote Plundering
        "nl": "wat-opkomt/de-grote-plundering.html",
        "de": "was-aufkommt/die-grosse-pluenderung.html",
        "en": "what-surfaces/the-great-plunder.html",
        "ru": "chto-vsplyvaet/velikoe-razgrablenie.html",
    },
    "2.1": {  # De Gevolgenkaart
        "nl": "wat-opkomt/de-gevolgenkaart.html",
    },
    "3.1": {  # Anti-immuunziekte
        "nl": "wat-opkomt/de-anti-immuunziekte-van-brussel.html",
        "de": "was-aufkommt/die-anti-immunkrankheit-bruessels.html",
        "en": "what-surfaces/the-anti-immune-disease-of-brussels.html",
        "ru": "chto-vsplyvaet/anti-immunnaya-bolezn-bryusselya.html",
        "es": "lo-que-emerge/la-enfermedad-anti-inmune-de-bruselas.html",
        "fr": "ce-qui-emerge/la-maladie-anti-immunitaire-de-bruxelles.html",
        "it": "cio-che-emerge/la-malattia-anti-immune-di-bruxelles.html",
        "pt": "o-que-emerge/a-doenca-anti-imune-de-bruxelas.html",
    },
    "3.2": {  # Levensaders Brussel (Bicrs)
        "nl": "wat-opkomt/levensaders-brussel.html",
        "de": "was-aufkommt/sie-toeten-ihre-lebensadern-bruessel.html",
        "en": "what-surfaces/they-kill-their-vital-arteries-brussels.html",
        "ru": "chto-vsplyvaet/oni-ubivayut-svoi-zhiznennye-arterii-bryussel.html",
        "es": "lo-que-emerge/matan-sus-arterias-vitales-bruselas.html",
        "fr": "ce-qui-emerge/ils-tuent-leurs-arteres-vitales-bruxelles.html",
        "it": "cio-che-emerge/uccidono-le-loro-arterie-vitali-bruxelles.html",
        "pt": "o-que-emerge/matam-as-suas-arterias-vitais-bruxelas.html",
    },
    "3.3": {  # Mappa Tal Konsegwenzi (Maltees verwijderd, fallback naar gevolgenkaart-iii)
        "nl": "wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
    },
    "3.4": {  # De Op De Natuur Aangepaste Analyse
        "nl": "wat-opkomt/de-actor-is-de-regel.html",  # best beschikbare
    },
    "4.1": {  # De Kantelmechanica
        "nl": "wat-opkomt/de-actor-is-de-regel.html",
        "de": "was-aufkommt/der-akteur-ist-die-regel.html",
        "en": "what-surfaces/the-actor-is-the-rule.html",
        "ru": "chto-vsplyvaet/aktor-est-pravilo.html",
    },
    "4.2": {  # Nova Democratia Manifest
        "nl": "wat-opkomt/nova-democratia-manifest.html",
    },
}

PREFIX = {"nl": "1", "de": "2", "en": "3", "ru": "4", "fr": "5", "es": "6", "it": "7", "pt": "8"}


def cross_link_to_nl(nl_path: str) -> str:
    """'wat-opkomt/foo.html' -> '../nl/wat-opkomt/foo.html' (vanuit andere taal)."""
    return f"../nl/{nl_path}"


totaal_added = totaal_updated = totaal_skipped = 0

for lang, prefix in PREFIX.items():
    routes_path = TAB / f"2_routes_{lang}.json"
    if not routes_path.exists():
        continue
    data = json.loads(routes_path.read_text(encoding="utf-8"))
    existing = {r["code"]: r for r in data["rijen"]}

    for suffix, taal_paden in ROUTES.items():
        # Bepaal URL: eigen taal of fallback naar NL
        if lang in taal_paden:
            url = taal_paden[lang]
        elif "nl" in taal_paden:
            url = cross_link_to_nl(taal_paden["nl"])
        else:
            continue

        # Verifieer bestand bestaat
        if url.startswith("../nl/"):
            check_path = REPO / "nl" / url.replace("../nl/", "")
        elif url.startswith("../"):
            # algemeen relatief — resolve vanaf <lang>/
            import posixpath
            check_path = REPO / posixpath.normpath(posixpath.join(f"{lang}/", url))
        else:
            check_path = REPO / lang / url
        if not check_path.exists():
            totaal_skipped += 1
            continue

        code = f"{prefix}.1.3.1.{suffix}"
        if code in existing:
            if existing[code].get("url") != url:
                existing[code]["url"] = url
                totaal_updated += 1
        else:
            new_row = {k: ("" if not isinstance(v, list) else []) for k, v in data["rijen"][0].items()} if data["rijen"] else {}
            new_row["code"] = code
            new_row["url"] = url
            new_row["doel_open"] = "self"
            data["rijen"].append(new_row)
            totaal_added += 1

    routes_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Routes toegevoegd: {totaal_added}")
print(f"Routes bijgewerkt: {totaal_updated}")
print(f"Skipped (bestand niet gevonden): {totaal_skipped}")
