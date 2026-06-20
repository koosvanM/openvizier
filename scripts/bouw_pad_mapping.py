#!/usr/bin/env python3
"""Bouw pad-equivalentie-tabel: voor elk HTML-pad in elke taal,
de exacte equivalenten in alle 7 andere talen (op basis van slug).

Output: scripts/_pad_mapping.json
Structuur:
  {
    "wat-opkomt/trump-als-spiegel.html": {
      "nl": "nl/wat-opkomt/trump-als-spiegel.html",
      "de": "de/was-aufkommt/trump-als-spiegel.html",
      ...
    },
    ...
  }
Key = canonieke 'logische' pad (mapnaam vertaald naar NL + slug).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Per taal: mapnaam -> canonieke (NL) mapnaam
DIR_NORM = {
    "nl": {
        "wat-opkomt": "wat-opkomt",
        "verkennen.html": "verkennen.html",
        "verkennen-embed.html": "verkennen-embed.html",
        "delen.html": "delen.html",
        "over.html": "over.html",
        "colofon.html": "colofon.html",
        "archief.html": "archief.html",
        "dossiers": "dossiers",
        "onderzoek": "onderzoek",
        "index.html": "index.html",
        **{f"editie-{i}": f"editie-{i}" for i in range(7)},
    },
    "de": {
        "was-aufkommt": "wat-opkomt",
        "verkennen.html": "verkennen.html",
        "verkennen-embed.html": "verkennen-embed.html",
        "teilen.html": "delen.html",
        "ueber.html": "over.html",
        "impressum.html": "colofon.html",
        "archiv.html": "archief.html",
        "dossiers": "dossiers",
        "forschung": "onderzoek",
        "index.html": "index.html",
        **{f"ausgabe-{i}": f"editie-{i}" for i in range(7)},
    },
    "en": {
        "what-surfaces": "wat-opkomt",
        "verkennen.html": "verkennen.html",
        "verkennen-embed.html": "verkennen-embed.html",
        "share.html": "delen.html",
        "about.html": "over.html",
        "colophon.html": "colofon.html",
        "archive.html": "archief.html",
        "dossiers": "dossiers",
        "research": "onderzoek",
        "index.html": "index.html",
        **{f"edition-{i}": f"editie-{i}" for i in range(7)},
    },
    "ru": {
        "chto-vsplyvaet": "wat-opkomt",
        "verkennen.html": "verkennen.html",
        "verkennen-embed.html": "verkennen-embed.html",
        "podelitsya.html": "delen.html",
        "o-gazete.html": "over.html",
        "vykhodnye-dannye.html": "colofon.html",
        "arkhiv.html": "archief.html",
        "dossiers": "dossiers",
        "issledovanie": "onderzoek",
        "index.html": "index.html",
        **{f"vypusk-{i}": f"editie-{i}" for i in range(7)},
    },
    "es": {
        "lo-que-emerge": "wat-opkomt",
        "verkennen.html": "verkennen.html",
        "verkennen-embed.html": "verkennen-embed.html",
        "edicion-0": "editie-0",
        "index.html": "index.html",
    },
    "fr": {
        "ce-qui-emerge": "wat-opkomt",
        "verkennen.html": "verkennen.html",
        "verkennen-embed.html": "verkennen-embed.html",
        "edition-0": "editie-0",
        "index.html": "index.html",
    },
    "it": {
        "cio-che-emerge": "wat-opkomt",
        "verkennen.html": "verkennen.html",
        "verkennen-embed.html": "verkennen-embed.html",
        "edizione-0": "editie-0",
        "index.html": "index.html",
    },
    "pt": {
        "o-que-emerge": "wat-opkomt",
        "verkennen.html": "verkennen.html",
        "verkennen-embed.html": "verkennen-embed.html",
        "edicao-0": "editie-0",
        "index.html": "index.html",
    },
}

# Omgekeerd: canonieke NL-mapnaam -> taal-specifiek
DIR_REV = {lang: {v: k for k, v in m.items()} for lang, m in DIR_NORM.items()}

LANGS = ["nl", "de", "en", "ru", "es", "fr", "it", "pt"]

def to_logical(lang: str, rel_path: str) -> str | None:
    """'de/ausgabe-3/artikel-04.html' -> 'editie-3/artikel-04.html'."""
    parts = rel_path.split("/")
    if not parts or parts[0] != lang:
        return None
    rest = parts[1:]
    if not rest:
        return None
    norm = DIR_NORM[lang]
    first = rest[0]
    if first not in norm:
        # onbekende top-level map; skip
        return None
    canon_first = norm[first]
    if len(rest) == 1:
        return canon_first
    # slug behoort tot artikel
    return canon_first + "/" + "/".join(rest[1:])

def from_logical(lang: str, logical: str) -> str | None:
    """'editie-3/artikel-04.html' -> 'de/ausgabe-3/artikel-04.html' (alleen als bestand bestaat)."""
    parts = logical.split("/")
    if not parts:
        return None
    rev = DIR_REV[lang]
    first = parts[0]
    if first not in rev:
        return None
    local_first = rev[first]
    rel = lang + "/" + local_first
    if len(parts) > 1:
        rel = rel + "/" + "/".join(parts[1:])
    if (ROOT / rel).exists():
        return rel
    return None

def main() -> None:
    mapping: dict[str, dict[str, str]] = {}
    for lang in LANGS:
        for path in (ROOT / lang).rglob("*.html"):
            rel = path.relative_to(ROOT).as_posix()
            logical = to_logical(lang, rel)
            if not logical:
                continue
            if logical not in mapping:
                mapping[logical] = {}
            mapping[logical][lang] = rel

    # Vul ontbrekende talen in met fallbacks:
    #   1. exact equivalent (bestaat)
    #   2. NL-versie
    #   3. taal-eigen sectie-index
    #   4. taal-root
    for logical, langmap in mapping.items():
        for lang in LANGS:
            if lang in langmap:
                continue
            # Probeer sectie-index in die taal
            section = logical.split("/")[0]
            section_index = from_logical(lang, section + "/index.html" if not section.endswith(".html") else section)
            if section_index:
                langmap[lang] = section_index
            elif "nl" in langmap:
                # Cross-link naar NL
                langmap[lang] = langmap["nl"]
            else:
                langmap[lang] = f"{lang}/"

    out = ROOT / "scripts" / "_pad_mapping.json"
    out.write_text(json.dumps(mapping, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    print(f"Logische paden: {len(mapping)}")
    print(f"Output: {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
