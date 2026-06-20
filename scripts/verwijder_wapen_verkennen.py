#!/usr/bin/env python3
"""
Verwijder het centrale wapen uit verkennen.html in alle 8 talen.
- Verwijder de CSS background-image van .center-overlay .bg
- Verwijder de <div class="bg" id="center-bg"></div> markup (volledig)
- Maak .center-overlay onzichtbaar wanneer het toch zou worden getoond
- Pas .center-overlay h2 / label aan zodat het centrum tekst-only wordt
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
LANGS = ["nl", "de", "en", "ru", "es", "fr", "it", "pt"]

MARKER = "/* wapen-verwijderd v1 */"

def fix(html):
    if MARKER in html:
        return html, "skipped (already done)"

    # 1) Verwijder de background-image regel in .center-overlay .bg
    #    Vervang de URL door 'none' en haal positionering eruit
    html = re.sub(
        r"background-image:url\('\.\./assets/wat-opkomt/wapen_nova_democratia\.png'\);?",
        "background-image:none;",
        html,
    )

    # 2) Verwijder de hele div class="bg" id="center-bg" (lege div blijft anders een gat)
    html = re.sub(
        r'\s*<div class="bg" id="center-bg"></div>',
        '',
        html,
    )

    # 3) Verberg evt. resterende achtergrond via een extra CSS-regel
    extra_css = f"""
  {MARKER}
  .center-overlay {{ display:none !important; }}
  .center-overlay .bg {{ display:none !important; background:none !important; }}
"""
    html = html.replace("</style>", extra_css + "\n</style>", 1)

    return html, "ok"

changed, skipped, missing = [], [], []
for lang in LANGS:
    path = REPO / lang / "verkennen.html"
    if not path.exists():
        missing.append(str(path))
        continue
    html = path.read_text(encoding="utf-8")
    new, status = fix(html)
    if status == "ok" and new != html:
        path.write_text(new, encoding="utf-8")
        changed.append(f"{lang}/verkennen.html")
    elif status == "skipped (already done)":
        skipped.append(f"{lang}/verkennen.html")
    else:
        skipped.append(f"{lang}/verkennen.html ({status})")

print(f"CHANGED ({len(changed)}):")
for c in changed: print(" -", c)
if skipped:
    print(f"SKIPPED ({len(skipped)}):")
    for s in skipped: print(" -", s)
if missing:
    print(f"MISSING ({len(missing)}):")
    for m in missing: print(" -", m)
