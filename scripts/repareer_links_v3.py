#!/usr/bin/env python3
"""V3 — fallback naar ../../nl/ voor ES/FR/IT/PT untranslated artikelen + specifieke laatste fixes."""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")

existing = set()
for f in REPO.rglob("*"):
    if f.is_file():
        existing.add(f.relative_to(REPO).as_posix())

def path_exists(p):
    p = p.lstrip("/")
    if not p: return True
    if p in existing: return True
    if (p + "/index.html") in existing: return True
    return False

# Per taal: (broken_basename, nl_target_basename)
# Verwijzen naar NL-equivalent via ../../nl/wat-opkomt/<naam>
NL_FALLBACKS = {
    "es": {
        "the-great-plunder.html": "de-grote-plundering.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "europa-hoeft-geen-schadekaart-te-zijn.html",
        "plundering-0-eerst-plukken-dan-oordelen.html": "plundering-0-eerst-plukken-dan-oordelen.html",
        "plundering-1-diagnose.html": "plundering-1-diagnose.html",
        "plundering-2-mechaniek.html": "plundering-2-mechaniek.html",
        "plundering-3-afloop.html": "plundering-3-afloop.html",
        "plundering-4-politieke-landschap.html": "plundering-4-politieke-landschap.html",
    },
    "fr": {
        "the-great-plunder.html": "de-grote-plundering.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "europa-hoeft-geen-schadekaart-te-zijn.html",
        "plundering-0-eerst-plukken-dan-oordelen.html": "plundering-0-eerst-plukken-dan-oordelen.html",
        "plundering-1-diagnose.html": "plundering-1-diagnose.html",
        "plundering-2-mechaniek.html": "plundering-2-mechaniek.html",
        "plundering-3-afloop.html": "plundering-3-afloop.html",
        "plundering-4-politieke-landschap.html": "plundering-4-politieke-landschap.html",
    },
    "it": {
        "the-great-plunder.html": "de-grote-plundering.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "europa-hoeft-geen-schadekaart-te-zijn.html",
        "la-mappa-delle-conseguenze.html": "de-gevolgenkaart.html",
        "plundering-0-eerst-plukken-dan-oordelen.html": "plundering-0-eerst-plukken-dan-oordelen.html",
        "plundering-1-diagnose.html": "plundering-1-diagnose.html",
        "plundering-2-mechaniek.html": "plundering-2-mechaniek.html",
        "plundering-3-afloop.html": "plundering-3-afloop.html",
        "plundering-4-politieke-landschap.html": "plundering-4-politieke-landschap.html",
    },
    "pt": {
        "the-great-plunder.html": "de-grote-plundering.html",
        "europa-hoeft-geen-schadekaart-te-zijn.html": "europa-hoeft-geen-schadekaart-te-zijn.html",
        "plundering-0-eerst-plukken-dan-oordelen.html": "plundering-0-eerst-plukken-dan-oordelen.html",
        "plundering-1-diagnose.html": "plundering-1-diagnose.html",
        "plundering-2-mechaniek.html": "plundering-2-mechaniek.html",
        "plundering-3-afloop.html": "plundering-3-afloop.html",
        "plundering-4-politieke-landschap.html": "plundering-4-politieke-landschap.html",
    },
}

# Top-level voor ES/FR/IT/PT die linkt naar share.html, delen.html → moet ../../nl/delen.html
# WANT er bestaat geen es/share.html als zelfstandig, ES verwijst naar NL
SHARE_FALLBACK_BASENAMES = {"share.html", "delen.html", "s-abonner.html"}

def relpath_to_nl(from_html_path, target_in_nl):
    """Bereken relatief pad vanaf from_html_path naar 'nl/<target_in_nl>'."""
    parent = from_html_path.parent
    nl_path = REPO / "nl" / target_in_nl
    try:
        from os.path import relpath
        return relpath(nl_path, parent).replace("\\", "/")
    except ValueError:
        return None

def repareer_lang(lang):
    n_fixed = 0
    fallbacks = NL_FALLBACKS.get(lang, {})
    base = REPO / lang
    if not base.exists(): return 0
    for html_path in base.rglob("*.html"):
        content = html_path.read_text(encoding="utf-8", errors="replace")
        original = content

        def replace(m):
            nonlocal n_fixed
            quote = m.group(1)
            href = m.group(2)
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
                return m.group(0)
            clean = href.split("#")[0].split("?")[0]
            if not clean: return m.group(0)
            # Resolve
            try:
                resolved = (html_path.parent / clean).resolve().relative_to(REPO).as_posix()
            except (ValueError, OSError):
                return m.group(0)
            # Bestaat al
            if path_exists(resolved):
                return m.group(0)
            # Basename
            base_name = clean.rsplit("/", 1)[-1]
            # Fallback voor wat-opkomt-artikelen
            if base_name in fallbacks:
                # Stuur naar ../../nl/wat-opkomt/<nl_naam>
                nl_target = f"wat-opkomt/{fallbacks[base_name]}"
                rel = relpath_to_nl(html_path, nl_target)
                if rel and path_exists((REPO / "nl" / nl_target).relative_to(REPO).as_posix()):
                    n_fixed += 1
                    return f'href={quote}{rel}{quote}'
            # Fallback voor share/delen → ../../nl/delen.html
            if base_name in SHARE_FALLBACK_BASENAMES:
                nl_target = "delen.html"
                rel = relpath_to_nl(html_path, nl_target)
                if rel and path_exists("nl/delen.html"):
                    n_fixed += 1
                    return f'href={quote}{rel}{quote}'
            return m.group(0)

        content = re.sub(r'''href=(["'])([^"']+)\1''', replace, content)
        if content != original:
            html_path.write_text(content, encoding="utf-8")
    return n_fixed

totaal = 0
for lang in ["es", "fr", "it", "pt"]:
    n = repareer_lang(lang)
    print(f"  {lang}: {n} hrefs gerepareerd")
    totaal += n
print(f"\nTotaal: {totaal}")
