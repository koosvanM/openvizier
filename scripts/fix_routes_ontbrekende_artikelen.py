#!/usr/bin/env python3
"""Repareer routes naar artikelen die niet als wat-opkomt-slug bestaan,
maar wel onder editie-5/. En koppel ontbrekende dossiers-routes."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAB = ROOT / "nl/_data/tabellen"

LANGS = ["nl", "de", "en", "ru", "es", "fr", "it", "pt"]

# code -> nieuwe relatieve URL vanuit <lang>/verkennen.html
# Doel: editie-5-artikelen onder NL (cross-taal fallback), of taal-eigen als bestaat
RESOLVE = {
    "1.2.2.4": ("editie-5/artikel-03-vergeten-orde.html",),
    "1.2.2.5": ("editie-5/artikel-04-methaan-misleiding.html",),
    "1.2.2.6": ("editie-5/artikel-05-plant-die-verhuist.html",),
    "1.2.2.7": ("editie-5/index.html",),                        # kernfusie als concept
    "1.2.2.8": ("editie-5/index.html",),                        # klimaathagiografie als concept
}

# Per taal: per code het pad relatief aan <lang>/verkennen.html
def resolve_for_lang(lang: str, code: str) -> str | None:
    # Strip eerste cijfer (taal-prefix) en houd de NL-equivalente code
    nl_code = "1" + code[1:] if code[0].isdigit() else code
    if nl_code not in RESOLVE:
        return None
    nl_path = RESOLVE[nl_code][0]
    # Map editie-5 -> taal-eigen
    dir_map = {
        "nl": "editie-5", "de": "ausgabe-5", "en": "edition-5", "ru": "vypusk-5",
        # ES/FR/IT/PT hebben geen editie-5 -> fallback NL
    }
    if lang in dir_map:
        local_path = nl_path.replace("editie-5", dir_map[lang])
        if (ROOT / lang / local_path).exists():
            return local_path  # relatief aan <lang>/verkennen.html
    # Cross-link NL
    return f"../nl/{nl_path}"


# Per taal: dossiers fallback naar NL voor ES/FR/IT/PT
DOSSIERS_FALLBACK = {
    "es": "../nl/dossiers/",
    "fr": "../nl/dossiers/",
    "it": "../nl/dossiers/",
    "pt": "../nl/dossiers/",
}


def main() -> None:
    totaal = 0
    for lang in LANGS:
        path = TAB / f"2_routes_{lang}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        gefixt = 0
        for r in data["rijen"]:
            code = r.get("code", "")
            # Editie-5-artikelen
            nieuwe = resolve_for_lang(lang, code)
            if nieuwe and r.get("url") != nieuwe:
                # Check of bestand bestaat
                target = nieuwe.lstrip("/")
                if target.startswith("../"):
                    target = target.replace("../", "", 1)
                else:
                    target = f"{lang}/{target}"
                if (ROOT / target).exists():
                    r["url"] = nieuwe
                    gefixt += 1
            # Dossiers fallback
            # Knopen die naar dossiers wijzen hebben meestal 'dossiers/' in url
            url = r.get("url", "")
            if lang in DOSSIERS_FALLBACK and url and "dossiers" in url and "/dossiers/" not in (ROOT / lang / "dossiers" / "").as_posix():
                # eigen taal heeft geen dossiers -> ../nl/dossiers/
                if url != DOSSIERS_FALLBACK[lang]:
                    r["url"] = DOSSIERS_FALLBACK[lang]
                    gefixt += 1
        if gefixt:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{lang.upper()}: {gefixt} routes bijgewerkt")
        totaal += gefixt
    print(f"\nTotaal: {totaal}")


if __name__ == "__main__":
    main()
