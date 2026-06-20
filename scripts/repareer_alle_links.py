#!/usr/bin/env python3
"""
Repareer alle gebroken interne links in alle 8 talen op basis van een
canonieke slug-vervangmapping.

Strategie:
- Voor elke (taal, broken_pad) bepalen we een vervangend pad.
- Als er geen vertaalde versie bestaat, verwijzen we naar de NL-versie
  (../../nl/<pad>) of laten de link weg (uitgecommentarieerd in HTML niet
  gedaan — we vervangen direct).

We gaan vooral in op de top-N broken-targets uit de audit.
"""
import re
import json
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# Per taal: NL-slug -> taal-specifieke slug (in dezelfde wat-opkomt map)
# Pad-vorm is RELATIEF aan het bestand dat de link bevat.
# Vervangregels zijn van toepassing op zowel "href='X'" als "href=\"X\"".

# Slug-mapping per taal (NL-slug → ander-taal-slug)
SLUG_MAP = {
    "de": {
        # Top-level pagina's
        "delen.html": "teilen.html",
        "over.html": "ueber.html",
        "colofon.html": "impressum.html",
        "archief.html": "archiv.html",
        "idee.html": "idee.html",
        # erkunden naar verkennen (bestand heet verkennen.html in alle talen)
        "erkunden.html": "verkennen.html",
        # wat-opkomt artikel-slugs (DE)
        "de-grote-plundering.html": "die-grosse-pluenderung.html",
        "the-great-plunder.html": "die-grosse-pluenderung.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "europa-muss-keine-schadenskarte-sein.html",
        # editie-2 artikelen: onderwijs-manifest verschilt
        "onderwijs-manifest.html": "bildung-manifest.html",
        # Mapnamen (in href-prefix)
        "wat-opkomt/": "was-aufkommt/",
        "editie-0/": "ausgabe-0/",
        "editie-1/": "ausgabe-1/",
        "editie-2/": "ausgabe-2/",
        "editie-3/": "ausgabe-3/",
        "editie-4/": "ausgabe-4/",
        "editie-5/": "ausgabe-5/",
        "editie-6/": "ausgabe-6/",
        "onderzoek/": "forschung/",
    },
    "en": {
        "delen.html": "share.html",
        "over.html": "about.html",
        "colofon.html": "colophon.html",
        "archief.html": "archive.html",
        "idee.html": "idea.html",
        "de-grote-plundering.html": "the-great-plunder.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "europe-need-not-be-a-damage-map.html",
        # editie-1 artikelen
        "voorwoord.html": "foreword.html",
        "denkraam-7d.html": "7d-framework.html",
        "wat-opkomt/": "what-surfaces/",
        "editie-0/": "edition-0/",
        "editie-1/": "edition-1/",
        "editie-2/": "edition-2/",
        "editie-3/": "edition-3/",
        "editie-4/": "edition-4/",
        "editie-5/": "edition-5/",
        "editie-6/": "edition-6/",
        "onderzoek/": "research/",
    },
    "ru": {
        "delen.html": "podelitsya.html",
        "over.html": "o-gazete.html",
        "colofon.html": "vykhodnye-dannye.html",
        "archief.html": "arkhiv.html",
        "idee.html": "ideya.html",
        "de-grote-plundering.html": "velikoe-razgrablenie.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "evropa-ne-dolzhna-byt-kartoy-ushcherba.html",
        "voorwoord.html": "predislovie.html",
        "denkraam-7d.html": "7d-konceptualnaya-ramka.html",
        "wat-opkomt/": "chto-vsplyvaet/",
        "editie-0/": "vypusk-0/",
        "editie-1/": "vypusk-1/",
        "editie-2/": "vypusk-2/",
        "editie-3/": "vypusk-3/",
        "editie-4/": "vypusk-4/",
        "editie-5/": "vypusk-5/",
        "editie-6/": "vypusk-6/",
        "onderzoek/": "issledovanie/",
    },
    "es": {
        # In ES bestaan alleen Brussel + landingpagina's
        "delen.html": "share.html",   # ES voorpagina link gaat naar share.html (root)
        "the-great-plunder.html": "../../nl/wat-opkomt/de-grote-plundering.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "../../nl/wat-opkomt/europa-hoeft-geen-schadekaart-te-zijn.html",
        "plundering-0-eerst-plukken-dan-oordelen.html": "../../nl/wat-opkomt/plundering-0-eerst-plukken-dan-oordelen.html",
        "plundering-1-diagnose.html": "../../nl/wat-opkomt/plundering-1-diagnose.html",
        "plundering-2-mechaniek.html": "../../nl/wat-opkomt/plundering-2-mechaniek.html",
        "plundering-3-afloop.html": "../../nl/wat-opkomt/plundering-3-afloop.html",
        "plundering-4-politieke-landschap.html": "../../nl/wat-opkomt/plundering-4-politieke-landschap.html",
        "de-grote-plundering.html": "../../nl/wat-opkomt/de-grote-plundering.html",
        "wat-opkomt/": "lo-que-emerge/",
    },
    "fr": {
        "delen.html": "share.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "../../nl/wat-opkomt/europa-hoeft-geen-schadekaart-te-zijn.html",
        "the-great-plunder.html": "../../nl/wat-opkomt/de-grote-plundering.html",
        "de-grote-plundering.html": "../../nl/wat-opkomt/de-grote-plundering.html",
        "wat-opkomt/": "ce-qui-emerge/",
    },
    "it": {
        "delen.html": "share.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "../../nl/wat-opkomt/europa-hoeft-geen-schadekaart-te-zijn.html",
        "the-great-plunder.html": "../../nl/wat-opkomt/de-grote-plundering.html",
        "de-grote-plundering.html": "../../nl/wat-opkomt/de-grote-plundering.html",
        "la-mappa-delle-conseguenze.html": "../../nl/wat-opkomt/de-gevolgenkaart.html",
        "wat-opkomt/": "cio-che-emerge/",
    },
    "pt": {
        "delen.html": "share.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "../../nl/wat-opkomt/europa-hoeft-geen-schadekaart-te-zijn.html",
        "the-great-plunder.html": "../../nl/wat-opkomt/de-grote-plundering.html",
        "de-grote-plundering.html": "../../nl/wat-opkomt/de-grote-plundering.html",
        "wat-opkomt/": "o-que-emerge/",
    },
    "nl": {
        # In NL kunnen er nog ${a.url} placeholders zijn die niet zijn gerenderd
        # Die laten we voor nu staan, ze worden door JS gegenereerd
    },
}

# Specifieke replace-regels — vervang link-targets letterlijk
# Format: per taal, lijst van (regex-patroon, vervanging)
# Werkt op hele HTML-bestanden, dus we matchen op het URL-deel in href="..."
def repareer_bestand(html_path, lang):
    """Repareer alle href-attributen in een bestand op basis van SLUG_MAP[lang]."""
    if lang not in SLUG_MAP:
        return 0
    rules = SLUG_MAP[lang]
    if not rules:
        return 0
    content = html_path.read_text(encoding="utf-8")
    original = content
    n_repl = 0

    # We werken op de hele tekst maar alleen binnen href="..." of href='...'
    def replace_href(m):
        nonlocal n_repl
        quote = m.group(1)
        href = m.group(2)
        new_href = href
        # Zoek de langste matchende regel
        # We splitsen het pad in segments en kijken of een segment matcht
        # Eenvoudigste aanpak: voor elke regel-key proberen we ze als suffix te matchen
        # OF als prefix wanneer het een mapnaam met / is

        # Mapnaam-substitutie (bv. "editie-3/" → "ausgabe-3/")
        for nl_key, target in rules.items():
            if nl_key.endswith("/"):
                # mapnaam: vervang waar dit segment voorkomt in het pad
                # we vervangen ALLE voorkomens behalve in absolute paden naar andere talen
                if nl_key in new_href:
                    # Niet aanraken als de href al naar een andere taal verwijst
                    if not re.search(r'(?:^|/)(de|en|ru|es|fr|it|pt)/', new_href):
                        new_href = new_href.replace(nl_key, target)
            else:
                # bestandsnaam: vervang alleen als het de basename is
                # bv. href="delen.html" -> "teilen.html"
                # bv. href="../delen.html" -> "../teilen.html"
                if new_href.endswith("/" + nl_key) or new_href == nl_key:
                    new_href = new_href[:-len(nl_key)] + target
                elif new_href.endswith(nl_key) and not target.startswith("../../nl/"):
                    # bv. ../delen.html  
                    new_href = new_href[:-len(nl_key)] + target
                # Fallback voor NL-fallback links (target begint met ../../nl/)
                if target.startswith("../../nl/") and new_href.endswith(nl_key):
                    # Bereken de relatieve diepte van de huidige pagina vanaf taal-root
                    # Voor pagina's onder /xx/lo-que-emerge/foo.html is ../../nl/ correct
                    # We laten staan zoals de target is gedefinieerd
                    new_href = target

        if new_href != href:
            n_repl += 1
            return f'href={quote}{new_href}{quote}'
        return m.group(0)

    content = re.sub(r'''href=(["'])([^"']+)\1''', replace_href, content)

    if content != original:
        html_path.write_text(content, encoding="utf-8")
    return n_repl

# Run
totaal = 0
gewijzigd = 0
per_lang = {}

for lang in SLUG_MAP:
    base = REPO / lang
    if not base.exists():
        continue
    lang_total = 0
    lang_files = 0
    for html_path in base.rglob("*.html"):
        n = repareer_bestand(html_path, lang)
        if n > 0:
            gewijzigd += 1
            lang_files += 1
        lang_total += n
        totaal += n
    per_lang[lang] = (lang_files, lang_total)

print(f"=== Link-reparatie voltooid ===")
print(f"Totaal vervangen hrefs: {totaal}")
print(f"Totaal gewijzigde bestanden: {gewijzigd}")
print(f"\nPer taal (bestanden, vervangingen):")
for lang, (f, n) in per_lang.items():
    print(f"  {lang}: {f} bestanden, {n} hrefs")
