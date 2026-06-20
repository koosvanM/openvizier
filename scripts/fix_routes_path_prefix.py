#!/usr/bin/env python3
"""Repareer routes-JSON: corrigeer verkeerde diepte-prefix.

Routes worden gebruikt vanuit <lang>/verkennen.html.
Dus correcte prefix om naar NL te springen is '../nl/...', niet '../../nl/...'.

Voor elke 2_routes_<lang>.json, vervang '../../nl/' door '../nl/' WANNEER het
bijbehorende doelbestand wél bestaat als '../nl/...' maar niet als '../../nl/...'.

Niet-NL-talen die het ook doen krijgen dezelfde behandeling.
"""
from __future__ import annotations
import json
import posixpath
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAB = ROOT / "nl/_data/tabellen"
LANGS = ["nl", "de", "en", "ru", "es", "fr", "it", "pt"]

# Verzamel bestaande paden
existing = set()
for f in ROOT.rglob("*"):
    if f.is_file():
        existing.add(f.relative_to(ROOT).as_posix())


def path_exists(p: str) -> bool:
    p = p.lstrip("/")
    if not p: return True
    if p in existing: return True
    if p.endswith("/") and (p + "index.html") in existing: return True
    if (p + "/index.html") in existing: return True
    return False


def resolve(lang: str, url: str) -> str:
    if url.startswith("/"):
        return url[1:]
    base = f"{lang}/"
    return posixpath.normpath(posixpath.join(base, url))


def try_fix(lang: str, url: str) -> str | None:
    """Probeer URL te repareren. Return nieuwe URL of None als niet te repareren."""
    if not url:
        return None
    test = resolve(lang, url)
    if path_exists(test):
        return None  # al goed

    # Heuristiek 1: één '../' te veel?
    if url.startswith("../../"):
        kandidaat = "../" + url[len("../../"):]
        if path_exists(resolve(lang, kandidaat)):
            return kandidaat

    # Heuristiek 2: één '../' te weinig?
    if url.startswith("../") and not url.startswith("../../"):
        kandidaat = "../../" + url[len("../"):]
        if path_exists(resolve(lang, kandidaat)):
            return kandidaat

    return None


def main() -> None:
    totaal_gefixt = 0
    totaal_onverbeterbaar = []
    for lang in LANGS:
        path = TAB / f"2_routes_{lang}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        gefixt = 0
        for r in data["rijen"]:
            url = r.get("url", "")
            if not url:
                continue
            nieuwe = try_fix(lang, url)
            if nieuwe:
                r["url"] = nieuwe
                gefixt += 1
            else:
                # Check of nog kapot
                if not path_exists(resolve(lang, url)):
                    totaal_onverbeterbaar.append((lang, r.get("code"), url))
        if gefixt:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{lang.upper()}: {gefixt} routes gerepareerd")
        totaal_gefixt += gefixt
    print(f"\nTotaal gefixt: {totaal_gefixt}")
    print(f"Onverbeterbaar: {len(totaal_onverbeterbaar)}")
    if totaal_onverbeterbaar:
        print("\n=== Onverbeterbare URLs ===")
        for lang, code, url in totaal_onverbeterbaar[:40]:
            print(f"  {lang} {code}: {url}")


if __name__ == "__main__":
    main()
