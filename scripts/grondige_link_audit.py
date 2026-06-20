#!/usr/bin/env python3
"""
Grondige audit van ALLE interne links in ALLE HTML-bestanden in /tmp/gh-repo.

Voor elke <a href="..."> in elk bestand:
- Resolve relatief naar het bestandspad
- Check of het doel bestaat in de repository
- Rapporteer: type bestand (artikel/index/menu), broken target, voorgestelde fix

Output: /tmp/broken_links.json met volledige rapport
"""
import re
from pathlib import Path
from urllib.parse import urlparse, unquote
from collections import defaultdict
import json

REPO = Path("/tmp/gh-repo")
LANGS = ["nl", "de", "en", "ru", "es", "fr", "it", "pt"]

# Verzamel alle bestaande paden in de repo (relatief vanaf REPO)
existing = set()
for f in REPO.rglob("*"):
    if f.is_file():
        rel = f.relative_to(REPO).as_posix()
        existing.add(rel)
        # Ook /foo/index.html bereikbaar als /foo/
        if rel.endswith("/index.html"):
            existing.add(rel[:-len("index.html")])  # /foo/

# Snel pad-bestaat-check
def path_exists(p):
    p = p.lstrip("/")
    if not p:
        return True  # root
    # Direct bestand
    if p in existing:
        return True
    # Directory met trailing slash
    if p.endswith("/"):
        if (p + "index.html") in existing:
            return True
        return False
    # Directory zonder trailing slash (Netlify-style)
    if (p + "/index.html") in existing:
        return True
    if (p + "/") in existing:
        return True
    # Bestand zonder .html (Netlify pretty URL)
    if (p + ".html") in existing:
        return True
    return False

# Verzamel alle <a href> uit elk html-bestand
HREF_RE = re.compile(r'<a[^>]+href="([^"]+)"', re.IGNORECASE)

issues_per_lang = defaultdict(list)
broken_per_pagina = defaultdict(list)
samenvatting = defaultdict(int)

for lang in LANGS:
    base = REPO / lang
    if not base.exists():
        continue
    for html_path in base.rglob("*.html"):
        rel_html = html_path.relative_to(REPO).as_posix()
        try:
            content = html_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        for href in HREF_RE.findall(content):
            # Skip externe, mailto, anker, tel, JS-template-strings
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
                continue
            if not href:
                continue
            if "${" in href or "{{" in href:  # JS/Jinja template
                continue
            # Pad eindigend op enkel / (root of taal-root) is altijd OK
            clean_test = href.split("#")[0].split("?")[0]
            if clean_test in ("/", "./", "../", "../../", "../../../"):
                continue
            # Strip query/anker
            clean = href.split("#")[0].split("?")[0]
            if not clean:
                continue
            # Absoluut pad?
            if clean.startswith("/"):
                target = clean[1:]
            else:
                # Relatief — resolve t.o.v. bestand
                parent = html_path.parent
                try:
                    abs_target = (parent / clean).resolve()
                except Exception:
                    continue
                try:
                    target = abs_target.relative_to(REPO).as_posix()
                except ValueError:
                    # buiten repo
                    continue
            target = unquote(target)
            # Check bestaan
            if not path_exists(target):
                broken_per_pagina[rel_html].append({
                    "href": href,
                    "resolved": target,
                })
                samenvatting[lang] += 1

# Rapportage
totaal = sum(len(v) for v in broken_per_pagina.values())
print(f"=== TOTAAL GEBROKEN INTERNE LINKS: {totaal} ===\n")
print("Per taal:")
for lang in LANGS:
    n = samenvatting.get(lang, 0)
    print(f"  {lang}: {n}")

# Toon top-10 meest voorkomende broken-targets
target_counts = defaultdict(int)
for issues in broken_per_pagina.values():
    for i in issues:
        target_counts[i["resolved"]] += 1

print(f"\n=== TOP 30 MEEST VOORKOMENDE BROKEN TARGETS ===")
for tgt, n in sorted(target_counts.items(), key=lambda x: -x[1])[:30]:
    print(f"  {n:4d}× {tgt}")

# Sla op
output = {
    "totaal": totaal,
    "per_taal": dict(samenvatting),
    "broken_per_pagina": dict(broken_per_pagina),
    "top_targets": [(t, n) for t, n in sorted(target_counts.items(), key=lambda x: -x[1])],
}
with open("/tmp/broken_links.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\nVolledig rapport: /tmp/broken_links.json")
