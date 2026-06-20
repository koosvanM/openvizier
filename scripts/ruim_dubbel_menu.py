#!/usr/bin/env python3
"""
Verwijder dubbel menu en verlaten talenring uit gevolgenkaart-artikelen.

Te verwijderen:
1. <nav class="topnav">...</nav>  — oude eigen menu, het uniforme
   <nav class="nav"> ervoor blijft staan.
2. <div class="lang-switch">...</div> — verlaten talen-toggle met
   "(andere talen volgen)" of equivalent in andere talen.
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

# Werkbestanden: alles dat een topnav of lang-switch heeft
TARGETS = []
for f in REPO.rglob("*.html"):
    try:
        content = f.read_text(encoding="utf-8")
    except Exception:
        continue
    if 'class="topnav"' in content or 'class="lang-switch"' in content:
        TARGETS.append(f)

TOPNAV_RE = re.compile(r'\s*<nav class="topnav">.*?</nav>', re.DOTALL)
LANGSWITCH_RE = re.compile(r'\s*<div class="lang-switch">.*?</div>', re.DOTALL)

veranderd = []
for path in TARGETS:
    content = path.read_text(encoding="utf-8")
    orig = content
    content = TOPNAV_RE.sub('', content)
    content = LANGSWITCH_RE.sub('', content)
    if content != orig:
        path.write_text(content, encoding="utf-8")
        veranderd.append(str(path.relative_to(REPO)))

print(f"Opgeruimd: {len(veranderd)}")
for v in veranderd: print(f"  - {v}")
