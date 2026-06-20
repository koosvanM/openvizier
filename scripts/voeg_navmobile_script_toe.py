#!/usr/bin/env python3
"""
Voeg <script src=".../assets/nav-mobile.js" defer></script> toe aan elk
HTML-bestand dat een <nav class="nav"> bevat, op alle 8 talen.

Pad-prefix wordt automatisch berekend op basis van bestandsdiepte.
Idempotent.
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
MARKER = "nav-mobile.js"

LANGS = ["nl", "de", "en", "ru", "es", "fr", "it", "pt"]

veranderd = 0
overgeslagen = 0
for lang in LANGS:
    base = REPO / lang
    if not base.exists():
        continue
    for html in base.rglob("*.html"):
        content = html.read_text(encoding="utf-8")
        # Alleen bestanden met <nav class="nav"> krijgen het script
        if 'class="nav"' not in content:
            continue
        # Al aanwezig?
        if MARKER in content:
            overgeslagen += 1
            continue
        # Bereken depth: hoe diep zit dit bestand onder REPO/<lang>/?
        rel = html.relative_to(base)
        depth = len(rel.parts) - 1  # alles voor de bestandsnaam
        prefix = "../" * (depth + 1)  # +1 om naar de taal-root te gaan en dan naar assets/
        script_tag = f'<script src="{prefix}assets/nav-mobile.js" defer></script>'

        # Voeg toe vóór </body>
        if "</body>" not in content:
            continue
        new_content = content.replace("</body>", script_tag + "\n</body>", 1)
        html.write_text(new_content, encoding="utf-8")
        veranderd += 1

print(f"Bijgewerkt: {veranderd}")
print(f"Al aanwezig: {overgeslagen}")
