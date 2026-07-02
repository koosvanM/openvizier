#!/usr/bin/env python3
"""Voeg menu-item 'Stemgedrag' toe direct na 'Verkennen' op alle NL/EN/DE-pagina's.

Werkwijze:
- Zoek het <li> dat naar verkennen.html linkt (elke taal, elk pad).
- Voeg direct daarna een nieuw <li> in met de stemgedrag-link in de juiste taal.
- Bepaal de taal aan het pad (nl/, en/, de/).
- Bepaal de href-diepte-prefix aan de href van het gevonden verkennen-<li>: als daar
  '../' voor staat, dan geldt hetzelfde voor stemgedrag.

Idempotent: als het stemgedrag-<li> al aanwezig is direct na verkennen, wordt het
niet nog eens toegevoegd.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

LANG_CONFIG = {
    "nl": {"slug": "stemgedrag.html", "label": "Stemgedrag"},
    "en": {"slug": "vote-impact.html", "label": "Vote Impact"},
    "de": {"slug": "wahlfolgen.html", "label": "Wahlfolgen"},
}

# Zoek een <li>…verkennen.html">…</a></li>, mogelijk met prefix (../ meermaals)
VERKENNEN_RE = re.compile(
    r'(<li>\s*<a\s+href="((?:\.\./)*)verkennen\.html"[^>]*>[^<]*</a>\s*</li>)',
    re.IGNORECASE,
)


def process_file(path: Path, lang: str) -> bool:
    cfg = LANG_CONFIG[lang]
    text = path.read_text(encoding="utf-8")

    m = VERKENNEN_RE.search(text)
    if not m:
        return False

    verkennen_block = m.group(1)
    prefix = m.group(2)  # bv "" of "../" of "../../"
    stemgedrag_href = f'{prefix}{cfg["slug"]}'
    new_li = f'<li><a href="{stemgedrag_href}">{cfg["label"]}</a></li>'

    # Idempotency: check of direct na verkennen-<li> al een stemgedrag-<li> staat
    end = m.end()
    tail = text[end:end + 300]
    if cfg["slug"] in tail[:200]:
        # al aanwezig direct erna
        return False

    # Formatteer met dezelfde indent als verkennen-<li>
    # Zoek de indent van de regel waar de match begint
    line_start = text.rfind("\n", 0, m.start()) + 1
    indent = ""
    for ch in text[line_start:m.start()]:
        if ch in " \t":
            indent += ch
        else:
            break
    inserted = f'{verkennen_block}\n{indent}{new_li}'
    new_text = text[:m.start()] + inserted + text[m.end():]

    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    changed = {"nl": 0, "en": 0, "de": 0}
    scanned = {"nl": 0, "en": 0, "de": 0}
    for lang in ["nl", "en", "de"]:
        for p in (REPO / lang).rglob("*.html"):
            scanned[lang] += 1
            try:
                if process_file(p, lang):
                    changed[lang] += 1
            except Exception as e:
                print(f"! error in {p}: {e}", file=sys.stderr)
    for lang in ["nl", "en", "de"]:
        print(f"{lang}: {changed[lang]} / {scanned[lang]} pagina's gewijzigd")


if __name__ == "__main__":
    main()
