#!/usr/bin/env python3
"""Automatische link-reparatie voor Het Open Vizier.

Loopt door alle HTML-bestanden, vindt gebroken href-links, en probeert ze
te repareren via de slug-cluster-mapping in tools/slug_clusters.json.

Strategie:
1. Common files (op-de-hoogte, delen): vertaal slug naar correcte taal
2. Wat-opkomt artikelen: vind cluster waarin de slug voorkomt, gebruik
   de juiste slug voor de doel-taal
3. Fallback-volgorde: doeltaal → EN → NL
4. Directe pad-fixes: één-op-één mapping uit JSON

Gebruik:
    python3 tools/link_fix.py                # bestanden aanpassen
    python3 tools/link_fix.py --dry-run      # alleen tonen wat zou veranderen
"""
import argparse
import json
import posixpath
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
HREF_PAT = re.compile(r'\bhref="([^"#]+?)"', re.IGNORECASE)


def laad_clusters():
    cfg = ROOT / "tools" / "slug_clusters.json"
    return json.loads(cfg.read_text(encoding="utf-8"))


def alle_bestanden():
    s = set()
    for f in ROOT.rglob("*"):
        if "preview" in f.parts or ".git" in f.parts:
            continue
        if f.is_file():
            s.add("/" + str(f.relative_to(ROOT)))
    return s


def bestaat(t, bestand_set):
    if t.endswith("/"):
        return (t + "index.html") in bestand_set
    return t in bestand_set


def maak_relatief(absoluut, bron_pad):
    src_dir = "/" + str(Path(bron_pad.lstrip("/")).parent) + "/"
    if src_dir == "//":
        src_dir = "/"
    rel = posixpath.relpath(absoluut, src_dir.rstrip("/"))
    if absoluut.endswith("/") and not rel.endswith("/"):
        rel += "/"
    return rel


def vertaal_pad(target, src_taal, clusters, bestand_set):
    """Probeer target naar correcte locatie te vertalen."""
    # 1. Directe fix?
    directe = clusters.get("directe_fixes", {})
    for k, v in directe.items():
        if k.startswith("_"):
            continue
        if target == k:
            return v if bestaat(v, bestand_set) else None

    if not target.startswith("/"):
        return None
    parts = target.lstrip("/").split("/")
    if not parts:
        return None
    target_taal = parts[0]
    talen = {"nl", "en", "de", "fr", "it", "es", "pt", "ru"}
    if target_taal not in talen:
        return None

    basename = parts[-1].replace(".html", "") if parts[-1].endswith(".html") else parts[-1]

    # 2. Common files (op-de-hoogte, delen)
    common = clusters.get("common_files", {})
    for naam, mapping in common.items():
        for taal, slug in mapping.items():
            if taal.startswith("_"):
                continue
            if slug == basename:
                # Probeer doel-taal
                gewenst = mapping.get(target_taal)
                if gewenst and not gewenst.startswith("_"):
                    kandidaat = f"/{target_taal}/{gewenst}.html"
                    if bestaat(kandidaat, bestand_set):
                        return kandidaat
                # EN fallback
                en_slug = mapping.get("en")
                if en_slug:
                    kandidaat = f"/en/{en_slug}.html"
                    if bestaat(kandidaat, bestand_set):
                        return kandidaat
                # NL fallback
                nl_slug = mapping.get("nl")
                if nl_slug:
                    kandidaat = f"/nl/{nl_slug}.html"
                    if bestaat(kandidaat, bestand_set):
                        return kandidaat
                return None

    # 3. Wat-opkomt clusters
    wat_opkomt = clusters.get("wat_opkomt_map_per_taal", {})
    if len(parts) >= 3 and target_taal in wat_opkomt and parts[1] == wat_opkomt[target_taal]:
        for cluster in clusters.get("wat_opkomt_clusters", []):
            for taal, slug in cluster.items():
                if taal.startswith("_"):
                    continue
                if slug == basename:
                    # Probeer doel-taal
                    gewenst = cluster.get(target_taal)
                    if gewenst and not gewenst.startswith("_"):
                        kandidaat = f"/{target_taal}/{wat_opkomt[target_taal]}/{gewenst}.html"
                        if bestaat(kandidaat, bestand_set):
                            return kandidaat
                    # EN fallback
                    en_slug = cluster.get("en")
                    if en_slug:
                        kandidaat = f"/en/{wat_opkomt['en']}/{en_slug}.html"
                        if bestaat(kandidaat, bestand_set):
                            return kandidaat
                    # NL fallback
                    nl_slug = cluster.get("nl")
                    if nl_slug:
                        kandidaat = f"/nl/{wat_opkomt['nl']}/{nl_slug}.html"
                        if bestaat(kandidaat, bestand_set):
                            return kandidaat
                    return None

    # 4. Generic: zoek bestand met zelfde naam in EN versie van zelfde pad-structuur
    if target_taal != "en" and len(parts) >= 2:
        # /<taal>/X/Y.html -> probeer /en/X/Y.html (als wat-opkomt-map: vertaal)
        en_parts = parts.copy()
        en_parts[0] = "en"
        if len(en_parts) >= 2 and en_parts[1] == wat_opkomt.get(target_taal):
            en_parts[1] = wat_opkomt["en"]
        kandidaat = "/" + "/".join(en_parts)
        if bestaat(kandidaat, bestand_set):
            return kandidaat

    return None


def fix(dry_run=False):
    clusters = laad_clusters()
    bestand_set = alle_bestanden()
    skip_patterns = clusters.get("skip_paths", {}).get("patterns", ["/preview/", "${"])

    fixes_per_bestand = defaultdict(list)
    onopgelost = []

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
        src_taal = src_rel.lstrip("/").split("/")[0]

        for m in HREF_PAT.finditer(html):
            href = m.group(1).strip()
            if not href:
                continue
            if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "//")):
                continue
            if href.startswith("#"):
                continue
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

            if any(target.startswith(p) for p in skip_patterns if p.startswith("/")):
                continue

            if bestaat(target, bestand_set):
                continue

            # Probeer te repareren — eerst met doel-taal, dan src-taal
            nieuw_abs = vertaal_pad(target, src_taal, clusters, bestand_set)
            if nieuw_abs:
                nieuw_rel = maak_relatief(nieuw_abs, src_rel)
                fixes_per_bestand[src_rel].append((href, nieuw_rel))
            else:
                onopgelost.append({"src": src_rel, "href": href, "target": target})

    # Pas fixes toe
    bestanden_aangepast = 0
    fixes_toegepast = 0
    for src_rel, lst in fixes_per_bestand.items():
        f = ROOT / src_rel.lstrip("/")
        html = f.read_text(encoding="utf-8")
        nieuw = html
        unieke = sorted({(h, n) for h, n in lst}, key=lambda x: -len(x[0]))
        for oud, nieuw_href in unieke:
            zoek = f'href="{oud}"'
            if zoek in nieuw:
                c = nieuw.count(zoek)
                nieuw = nieuw.replace(zoek, f'href="{nieuw_href}"')
                fixes_toegepast += c
        if nieuw != html:
            if not dry_run:
                f.write_text(nieuw, encoding="utf-8")
            bestanden_aangepast += 1

    return {
        "bestanden_aangepast": bestanden_aangepast,
        "fixes_toegepast": fixes_toegepast,
        "onopgelost": onopgelost,
        "fixes_per_bestand": {k: v for k, v in fixes_per_bestand.items()},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="Toon wat zou veranderen, schrijf niets")
    ap.add_argument("--json", metavar="PAD", help="Schrijf samenvatting als JSON")
    ap.add_argument("--fail-on-unresolved", action="store_true", help="Exit-code 1 als er onoplosbare fouten zijn")
    args = ap.parse_args()

    res = fix(dry_run=args.dry_run)

    print(f"Het Open Vizier — Link-fix rapport")
    print(f"=" * 60)
    print(f"Bestanden aangepast    : {res['bestanden_aangepast']}")
    print(f"Link-fixes toegepast   : {res['fixes_toegepast']}")
    print(f"Onopgelost             : {len(res['onopgelost'])}")
    if args.dry_run:
        print(f"(DRY-RUN: niets geschreven)")

    if res["onopgelost"]:
        from collections import Counter
        c = Counter(o["target"] for o in res["onopgelost"])
        print()
        print("Top onopgeloste doelen:")
        for t, n in c.most_common(15):
            print(f"  {n:3d}× {t}")

    if args.json:
        Path(args.json).write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nJSON: {args.json}")

    if args.fail_on_unresolved and res["onopgelost"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
