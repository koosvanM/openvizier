#!/usr/bin/env python3
"""Link-audit voor Het Open Vizier.

Loopt alle HTML-bestanden door en controleert of elke interne href naar
een bestaand bestand verwijst. Externe URLs en anchors worden overgeslagen.

Gebruik:
    python3 tools/link_audit.py                    # rapport in console
    python3 tools/link_audit.py --json rapport.json  # ook JSON-output
    python3 tools/link_audit.py --fail-on-errors   # exit-code 1 bij fouten

Wat wordt overgeslagen:
- /preview/-paden (preview-content, niet live)
- ${...}-template-literals (JavaScript dynamisch)
- Externe URLs (http://, https://, mailto:, tel:)
- Anchors (#fragment)
"""
import argparse
import json
import posixpath
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent  # repo root

HREF_PAT = re.compile(r'\bhref="([^"#]+?)"', re.IGNORECASE)


def laad_skip_patterns():
    cfg = ROOT / "tools" / "slug_clusters.json"
    if not cfg.exists():
        return ["/preview/", "${"]
    data = json.loads(cfg.read_text(encoding="utf-8"))
    return data.get("skip_paths", {}).get("patterns", ["/preview/", "${"])


def alle_bestanden():
    """Set van alle bestandspaden in de repo (absoluut vanaf root)."""
    s = set()
    for f in ROOT.rglob("*"):
        if "preview" in f.parts:
            continue
        if ".git" in f.parts:
            continue
        if f.is_file():
            s.add("/" + str(f.relative_to(ROOT)))
    return s


def bestaat(target, bestand_set):
    if target.endswith("/"):
        return (target + "index.html") in bestand_set
    return target in bestand_set


def audit():
    bestand_set = alle_bestanden()
    skip_patterns = laad_skip_patterns()
    issues = []

    html_files = [
        f for f in ROOT.rglob("*.html")
        if "preview" not in f.parts and ".git" not in f.parts
    ]

    for f in html_files:
        try:
            html = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        src_rel = "/" + str(f.relative_to(ROOT))
        src_dir = "/" + str(f.relative_to(ROOT).parent) + "/"
        if src_dir == "//":
            src_dir = "/"

        for m in HREF_PAT.finditer(html):
            href = m.group(1).strip()
            if not href:
                continue
            if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "//")):
                continue
            if href.startswith("#"):
                continue
            # Skip JS template literals etc.
            if any(p in href for p in skip_patterns if not p.startswith("/")):
                continue

            clean = unquote(href.split("#", 1)[0].split("?", 1)[0])
            if not clean:
                continue

            if clean.startswith("/"):
                target = clean
            else:
                target = posixpath.normpath(posixpath.join(src_dir, clean))
                if clean.endswith("/") and not target.endswith("/"):
                    target += "/"

            # Skip-paths check
            if any(target.startswith(p) for p in skip_patterns if p.startswith("/")):
                continue

            if not bestaat(target, bestand_set):
                issues.append({"src": src_rel, "href": href, "target": target})

    return issues


def rapporteer(issues, verbose=True):
    """Print human-readable rapport."""
    print(f"Het Open Vizier — Link-audit rapport")
    print(f"=" * 60)
    print(f"Totaal gebroken interne links : {len(issues)}")
    per_src = defaultdict(list)
    per_target = defaultdict(list)
    for i in issues:
        per_src[i["src"]].append(i)
        per_target[i["target"]].append(i)
    print(f"Bron-paginas met fouten       : {len(per_src)}")
    print(f"Unieke gebroken doelen        : {len(per_target)}")

    if not issues:
        print()
        print("✓ Alles klopt — geen gebroken links gevonden.")
        return

    if not verbose:
        return

    print()
    print("Top 25 gebroken doelen (sorteer op aantal verwijzingen):")
    print("-" * 60)
    top = sorted(per_target.items(), key=lambda kv: -len(kv[1]))[:25]
    for target, refs in top:
        print(f"\n  ✗ {target}  ({len(refs)} verwijzingen)")
        for r in refs[:3]:
            print(f"      vanuit {r['src']}  →  {r['href']}")
        if len(refs) > 3:
            print(f"      … en {len(refs) - 3} meer")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", metavar="PAD", help="Schrijf rapport ook als JSON naar PAD")
    ap.add_argument("--quiet", action="store_true", help="Alleen samenvatting, geen details")
    ap.add_argument("--fail-on-errors", action="store_true", help="Exit-code 1 bij fouten (voor CI)")
    args = ap.parse_args()

    issues = audit()
    rapporteer(issues, verbose=not args.quiet)

    if args.json:
        out = {
            "totaal": len(issues),
            "issues": issues,
        }
        Path(args.json).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nJSON-rapport: {args.json}")

    if args.fail_on_errors and issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
