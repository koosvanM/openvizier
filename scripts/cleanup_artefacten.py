#!/usr/bin/env python3
"""
Ruim oude menu-artefacten op:
1. Losse <a href="/" title="Naar taalkeuze">⌂</a> rechtsboven in headers
2. Verlaten taal-balk <a href="../../<lang>/" ...>⌂ <Verkennen>}</a> (regel 61 / 71)
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

TARGETS = [
    "es/edicion-0/index.html", "es/lo-que-emerge/index.html",
    "fr/edition-0/index.html", "fr/ce-qui-emerge/index.html",
    "it/edizione-0/index.html", "it/cio-che-emerge/index.html",
    "pt/edicao-0/index.html", "pt/o-que-emerge/index.html",
]

# Patronen om weg te halen
PATRONEN = [
    # Losse ⌂-knop rechtsboven met Nederlandse tooltip
    re.compile(r'\s*<a href="/" title="Naar taalkeuze"[^>]*>⌂</a>', re.DOTALL),
    # Verlaten "⌂ Explorar/Explorer/Esplorare/Explorar" balk
    re.compile(r'\s*<a href="\.\./\.\./[a-z]{2}/"[^>]*>⌂\s*(Explorar|Explorer|Esplorare|Esplorar)</a>', re.DOTALL),
    # Ook de wrapper-div als die alleen die ene <a> bevatte (zoeken naar <div>\s*<a ...>⌂ ...</a>\s*</div>)
]

changed = []
for rel in TARGETS:
    path = REPO / rel
    if not path.exists():
        continue
    html = path.read_text(encoding="utf-8")
    orig = html
    for pat in PATRONEN:
        html = pat.sub('', html)
    # Ook: leeggebleven container-div (een div met alleen whitespace)
    # vooral op de plekken waar de "⌂ Explorar" balk in een wrapper-div stond
    html = re.sub(
        r'<div[^>]*>\s*</div>',
        '',
        html,
    )
    if html != orig:
        path.write_text(html, encoding="utf-8")
        changed.append(rel)

print(f"Opgeruimd: {len(changed)}")
for c in changed:
    print(f"  - {c}")
