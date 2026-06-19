#!/usr/bin/env python3
"""Verwijder het uniforme <nav class="nav">...</nav> menu van alle talenring-pagina's.
De talenring is een standalone taalkeuze met eigen donkere achtergrond — het menu hoort daar niet."""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
TARGETS = [
    "nl/talenring.html",
    "nl/index-talenring.html",
    "de/index-talenring.html",
    "en/index-talenring.html",
    "ru/index-talenring.html",
    "es/index-talenring.html",
    "fr/index-talenring.html",
    "it/index-talenring.html",
    "pt/index-talenring.html",
]

NAV_RE = re.compile(r'<nav class="nav">.*?</nav>\s*', re.DOTALL)

changed = []
for rel in TARGETS:
    p = REPO / rel
    if not p.exists():
        continue
    html = p.read_text(encoding="utf-8")
    new = NAV_RE.sub('', html, count=1)
    if new != html:
        p.write_text(new, encoding="utf-8")
        changed.append(rel)

print("verwijderd:", changed)
