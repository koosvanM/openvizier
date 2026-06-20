#!/usr/bin/env python3
"""Verklein de tegel-labels in alle verkennen-pagina's."""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# Doelbestanden: per taal verkennen.html + verkennen-embed.html
LANGS = ["nl", "de", "en", "ru", "es", "fr", "it", "pt"]
EMBED_LANGS = ["nl", "de", "en", "ru"]

bestanden = []
for lang in LANGS:
    p = REPO / lang / "verkennen.html"
    if p.exists(): bestanden.append(p)
for lang in EMBED_LANGS:
    p = REPO / lang / "verkennen-embed.html"
    if p.exists(): bestanden.append(p)

# Vervangregels (regex → vervanging)
# Patroon herkent de bestaande clamp-waarden in beide bestanden.
REGELS = [
    # h2 in tile-label (standalone verkennen.html)
    (
        r'font-size:clamp\(1rem,2\.2vw,1\.8rem\)',
        'font-size:clamp(.85rem,1.7vw,1.4rem)',
    ),
    # h2 in tile-label (embed verkennen-embed.html)
    (
        r'font-size:clamp\(1rem,2\.4vw,1\.9rem\)',
        'font-size:clamp(.85rem,1.8vw,1.45rem)',
    ),
    # p (subtitel) in tile-label — beide versies
    (
        r'font-size:clamp\(\.75rem,1vw,\.95rem\)',
        'font-size:clamp(.7rem,.85vw,.85rem)',
    ),
    # padding van de label-wrapper iets ruimer (verkennen.html versie)
    (
        r'\.verkennen-canvas \.tile \.label \{ position:relative; z-index:2; text-align:center; padding:1rem; max-width:90% \}',
        '.verkennen-canvas .tile .label { position:relative; z-index:2; text-align:center; padding:1.4rem 1rem; max-width:92%; }',
    ),
    # embed-versie padding
    (
        r'\.tile \.label \{ position:relative; z-index:2; text-align:center; padding:1rem; max-width:90%; \}',
        '.tile .label { position:relative; z-index:2; text-align:center; padding:1.4rem 1rem; max-width:92%; }',
    ),
]

veranderd = []
for path in bestanden:
    content = path.read_text(encoding="utf-8")
    orig = content
    for pat, vervang in REGELS:
        content = re.sub(pat, vervang, content)
    if content != orig:
        path.write_text(content, encoding="utf-8")
        veranderd.append(str(path.relative_to(REPO)))

print(f"Gewijzigd: {len(veranderd)} bestanden")
for v in veranderd: print(f"  - {v}")
