#!/usr/bin/env python3
"""
Koppel alle Editie-Europa Verkenner-knopen (X.1.3.1.*) aan hun werkelijke
artikelpagina's in de wat-opkomt-map.

X = taalprefix (1=NL, 2=DE, 3=EN, 4=RU, 5=FR, 6=ES, 7=IT, 8=PT)

Voor talen waar het artikel niet vertaald bestaat, valt de route terug
op de NL-versie via ../../nl/wat-opkomt/...
"""
import json
from pathlib import Path

REPO = Path("/tmp/gh-repo")
TAB = REPO / "nl/_data/tabellen"

# Per code-suffix (na 1.3.1.): { taal: relatief-pad-binnen-taalroot }
# Pad-vorm: 'wat-opkomt/<slug>.html' of '../../nl/wat-opkomt/<slug>.html' bij fallback
ROUTES = {
    # 1.3.1.1.* Diagnose Nederland → De Grote Plundering
    "1.1": {
        "nl": "wat-opkomt/de-grote-plundering.html",
        "de": "was-aufkommt/die-grosse-pluenderung.html",
        "en": "what-surfaces/the-great-plunder.html",
        "ru": "chto-vsplyvaet/velikoe-razgrablenie.html",
        "es": "../../nl/wat-opkomt/de-grote-plundering.html",
        "fr": "../../nl/wat-opkomt/de-grote-plundering.html",
        "it": "../../nl/wat-opkomt/de-grote-plundering.html",
        "pt": "../../nl/wat-opkomt/de-grote-plundering.html",
    },
    # 1.3.1.2.* Het instrument → De Gevolgenkaart (Manifest)
    "2.1": {
        "nl": "wat-opkomt/de-gevolgenkaart.html",
        # andere talen vertaling ontbreekt → fallback
        "de": "../../nl/wat-opkomt/de-gevolgenkaart.html",
        "en": "../../nl/wat-opkomt/de-gevolgenkaart.html",
        "ru": "../../nl/wat-opkomt/de-gevolgenkaart.html",
        "es": "../../nl/wat-opkomt/de-gevolgenkaart.html",
        "fr": "../../nl/wat-opkomt/de-gevolgenkaart.html",
        "it": "../../nl/wat-opkomt/de-gevolgenkaart.html",
        "pt": "../../nl/wat-opkomt/de-gevolgenkaart.html",
    },
    # 1.3.1.3.1 De Brusselse Gevolgenkaart → de-anti-immuunziekte-van-brussel
    "3.1": {
        "nl": "wat-opkomt/de-anti-immuunziekte-van-brussel.html",
        "de": "was-aufkommt/die-anti-immunkrankheit-bruessels.html",
        "en": "what-surfaces/the-anti-immune-disease-of-brussels.html",
        "ru": "chto-vsplyvaet/anti-immunnaya-bolezn-bryusselya.html",
        "es": "lo-que-emerge/la-enfermedad-anti-inmune-de-bruselas.html",
        "fr": "ce-qui-emerge/la-maladie-anti-immunitaire-de-bruxelles.html",
        "it": "cio-che-emerge/la-malattia-anti-immune-di-bruxelles.html",
        "pt": "o-que-emerge/a-doenca-anti-imune-de-bruxelas.html",
    },
    # 1.3.1.3.2 Brusselse Gevolgenkaart BiCRS → zij-doden-hun-levensaders-brussel
    "3.2": {
        "nl": "wat-opkomt/zij-doden-hun-levensaders-brussel.html",
        "de": "was-aufkommt/sie-toeten-ihre-lebensadern-bruessel.html",
        "en": "what-surfaces/they-kill-their-lifelines-brussels.html",
        "ru": "chto-vsplyvaet/oni-ubivayut-svoi-zhiznennye-arterii-bryussel.html",
        "es": "lo-que-emerge/matan-sus-arterias-vitales-bruselas.html",
        "fr": "ce-qui-emerge/ils-tuent-leurs-arteres-vitales-bruxelles.html",
        "it": "cio-che-emerge/uccidono-le-loro-arterie-vitali-bruxelles.html",
        "pt": "o-que-emerge/matam-as-suas-arterias-vitais-bruxelas.html",
    },
    # 1.3.1.3.3 Mappa Tal Konsegwenzi → niet meer relevant (Maltees verwijderd)
    # We koppelen aan gevolgenkaart-iii-stille-analyse als best beschikbaar
    "3.3": {
        "nl": "wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
        "de": "../../nl/wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
        "en": "../../nl/wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
        "ru": "../../nl/wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
        "es": "../../nl/wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
        "fr": "../../nl/wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
        "it": "../../nl/wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
        "pt": "../../nl/wat-opkomt/gevolgenkaart-iii-stille-analyse.html",
    },
    # 1.3.1.3.4 De Op De Natuur Aangepaste Analyse
    "3.4": {
        "nl": "wat-opkomt/de-op-de-natuur-aangepaste-analyse.html",
        # check of bestand bestaat — anders fallback naar de-actor-is-de-regel
    },
    # 1.3.1.4.1 De Kantelmechanica → de-actor-is-de-regel
    "4.1": {
        "nl": "wat-opkomt/de-actor-is-de-regel.html",
        "de": "was-aufkommt/der-akteur-ist-die-regel.html",
        "en": "what-surfaces/the-actor-is-the-rule.html",
        "ru": "chto-vsplyvaet/aktor-est-pravilo.html",
        "es": "../../nl/wat-opkomt/de-actor-is-de-regel.html",
        "fr": "../../nl/wat-opkomt/de-actor-is-de-regel.html",
        "it": "../../nl/wat-opkomt/de-actor-is-de-regel.html",
        "pt": "../../nl/wat-opkomt/de-actor-is-de-regel.html",
    },
    # 1.3.1.4.2 Nova Democratia Manifest
    "4.2": {
        "nl": "wat-opkomt/nova-democratia-manifest.html",
        "de": "../../nl/wat-opkomt/nova-democratia-manifest.html",
        "en": "../../nl/wat-opkomt/nova-democratia-manifest.html",
        "ru": "../../nl/wat-opkomt/nova-democratia-manifest.html",
        "es": "../../nl/wat-opkomt/nova-democratia-manifest.html",
        "fr": "../../nl/wat-opkomt/nova-democratia-manifest.html",
        "it": "../../nl/wat-opkomt/nova-democratia-manifest.html",
        "pt": "../../nl/wat-opkomt/nova-democratia-manifest.html",
    },
}

PREFIX = {"nl": "1", "de": "2", "en": "3", "ru": "4", "fr": "5", "es": "6", "it": "7", "pt": "8"}

# Update 2_routes_<lang>.json per taal
totaal_added = totaal_updated = totaal_skipped = 0
for lang, prefix in PREFIX.items():
    routes_path = TAB / f"2_routes_{lang}.json"
    if not routes_path.exists():
        continue
    data = json.loads(routes_path.read_text(encoding="utf-8"))
    existing = {r["code"]: r for r in data["rijen"]}

    for suffix, taal_paden in ROUTES.items():
        if lang not in taal_paden:
            continue
        url = taal_paden[lang]
        # Verifieer dat bestand bestaat (resolve relatief)
        # Pad in 2_routes is relatief aan <taalroot>/<verkennen.html>
        # Dus 'wat-opkomt/x.html' = REPO/<lang>/wat-opkomt/x.html
        # En '../../nl/wat-opkomt/x.html' = REPO/nl/wat-opkomt/x.html
        if url.startswith("../../nl/"):
            check_path = REPO / "nl" / url.replace("../../nl/", "")
        else:
            check_path = REPO / lang / url
        if not check_path.exists():
            totaal_skipped += 1
            continue

        code = f"{prefix}.1.3.{suffix}"
        if code in existing:
            if existing[code].get("url") != url:
                existing[code]["url"] = url
                totaal_updated += 1
        else:
            new_row = {k: None for k in data["rijen"][0].keys()} if data["rijen"] else {}
            new_row["code"] = code
            new_row["url"] = url
            new_row["doel_open"] = "zelf"
            data["rijen"].append(new_row)
            totaal_added += 1

    routes_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Routes toegevoegd: {totaal_added}")
print(f"Routes bijgewerkt: {totaal_updated}")
print(f"Skipped (bestand niet gevonden): {totaal_skipped}")
