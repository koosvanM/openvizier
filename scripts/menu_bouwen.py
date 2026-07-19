#!/usr/bin/env python3
"""
Canonieke menuconfigurator — Het Open Vizier
============================================

Leest nl/_data/menu-config.yaml en produceert:
  1. nl/_data/menu/{taal}.json   — machine-leesbare menu-structuur per taal
  2. Vervangt <nav>-blok in {taal}/index.html op alle voorpagina's
  3. Injecteert de ov-nav CSS + JS als aparte blokken in <head>/</body>

Gebruik:
    python3 scripts/menu_bouwen.py                # regenereer alles
    python3 scripts/menu_bouwen.py --dry-run      # print alleen
    python3 scripts/menu_bouwen.py --only nl,en   # deelselectie talen

Elke wijziging aan het menu begint met bewerken van menu-config.yaml, gevolgd
door het draaien van dit script. De HTML wordt daaruit gegenereerd — niet
handmatig aangepast.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Fout: python-yaml niet geïnstalleerd. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO / "nl" / "_data" / "menu-config.yaml"
JSON_DIR    = REPO / "nl" / "_data" / "menu"

# ---------------------------------------------------------------------------
# CSS + JS — canonieke assets, geïnjecteerd op elke voorpagina
# ---------------------------------------------------------------------------

NAV_CSS = """<style>
  /* ov-nav v2 — canoniek dropdown-menu (gegenereerd via menu_bouwen.py) */
  .ov-nav { background:#faf8f3; border-top:1px solid #d4d1ca; border-bottom:1px solid #d4d1ca; }
  .ov-nav__inner { max-width:1180px; margin:0 auto; padding:0.35rem 1rem; display:flex; gap:0.25rem; justify-content:center; flex-wrap:wrap; }
  .ov-nav__group { position:relative; }
  .ov-nav__toggle { background:none; border:0; padding:0.75rem 1rem; font:inherit; color:#1a1a1a; font-weight:600; letter-spacing:0.02em; cursor:pointer; border-radius:4px; }
  .ov-nav__toggle:hover, .ov-nav__toggle[aria-expanded="true"] { background:#f0ede4; color:#7a1f2b; }
  .ov-nav__menu { display:none; position:absolute; top:100%; left:0; min-width:230px; background:#ffffff; border:1px solid #d4d1ca; box-shadow:0 6px 18px rgba(0,0,0,0.08); padding:0.4rem 0; z-index:50; }
  .ov-nav__menu--wide { min-width:260px; }
  .ov-nav__group:hover .ov-nav__menu,
  .ov-nav__group:focus-within .ov-nav__menu { display:block; }
  .ov-nav__menu a { display:block; padding:0.55rem 1.1rem; color:#1a1a1a !important; text-decoration:none !important; font-size:0.94rem; line-height:1.35; }
  .ov-nav__menu a:hover { background:#f5f3ee; color:#7a1f2b !important; }
  .ov-nav__menu hr { border:0; border-top:1px solid #e4e1d8; margin:0.35rem 0; }
  .ov-nav__sub { display:block; padding:0.15rem 0; background:#faf8f3; border-top:1px solid #efece3; border-bottom:1px solid #efece3; }
  .ov-nav__sub a { padding-left:1.8rem !important; font-size:0.88rem; color:#4a5263 !important; }
  .ov-nav__sub a::before { content:"› "; color:#9ca3af; }
  .ov-nav__fallback { color:#9ca3af !important; font-style:italic; }
  @media (max-width:720px) {
    .ov-nav__inner { flex-direction:column; align-items:stretch; padding:0.25rem 0.5rem; }
    .ov-nav__group { border-bottom:1px solid #efece3; }
    .ov-nav__group:last-child { border-bottom:0; }
    .ov-nav__toggle { width:100%; text-align:left; padding:0.85rem 1rem; }
    .ov-nav__menu { position:static; box-shadow:none; border:0; padding:0 0 0.5rem 0; min-width:0; background:#f5f3ee; }
    .ov-nav__group:hover .ov-nav__menu, .ov-nav__group:focus-within .ov-nav__menu { display:block; }
  }
</style>
"""

NAV_JS = """<script>
/* ov-nav v2 — click-toggle voor touch/mobile */
(function(){
  document.querySelectorAll('.ov-nav__toggle').forEach(function(btn){
    btn.addEventListener('click', function(e){
      var open = btn.getAttribute('aria-expanded') === 'true';
      document.querySelectorAll('.ov-nav__toggle').forEach(function(b){ b.setAttribute('aria-expanded','false'); });
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      e.stopPropagation();
    });
  });
  document.addEventListener('click', function(){
    document.querySelectorAll('.ov-nav__toggle').forEach(function(b){ b.setAttribute('aria-expanded','false'); });
  });
})();
</script>
"""

# Markers om oude/nieuwe blokken te herkennen bij regenereren
CSS_MARKER = "/* ov-nav v2"
JS_MARKER  = "/* ov-nav v2 — click-toggle"


# ---------------------------------------------------------------------------
# Kern-logica
# ---------------------------------------------------------------------------

def resolve_url(item: dict, taal: str, fallback: str = "nl") -> tuple[str, bool]:
    """Return (url, is_fallback). Als url leeg is voor taal → val terug op fallback."""
    urls = item.get("urls", {})
    url = urls.get(taal, "")
    if url:
        return url, False
    # Fallback: prefix '../{fallback}/' voor de fallback-URL
    fb_url = urls.get(fallback, "")
    if not fb_url:
        return "#", True
    if fb_url == "./":
        return f"../{fallback}/", True
    return f"../{fallback}/{fb_url}", True


def build_menu_data(config: dict) -> dict[str, dict]:
    """Bouw per taal een dict {groepen: [...]} met resolved URLs."""
    result = {}
    for taal in config["talen"]:
        groepen_out = []
        for groep in config["groepen"]:
            items_out = []
            for item in groep["items"]:
                url, is_fallback = resolve_url(item, taal)
                items_out.append({
                    "key": item["key"],
                    "label": item["labels"].get(taal, item["labels"]["nl"]),
                    "url": url,
                    "sub_van": item.get("sub_van"),
                    "scheiding_boven": item.get("scheiding_boven", False),
                    "is_fallback": is_fallback,
                })
            groepen_out.append({
                "key": groep["key"],
                "label": groep["labels"].get(taal, groep["labels"]["nl"]),
                "items": items_out,
            })
        result[taal] = {"taal": taal, "groepen": groepen_out}
    return result


def render_nav_html(menu_data: dict) -> str:
    """Genereer <nav>-HTML voor één taal."""
    groepen = menu_data["groepen"]
    parts = ['<nav class="ov-nav" aria-label="Hoofdmenu">']
    parts.append('  <div class="ov-nav__inner">')
    for groep in groepen:
        parts.append(f'    <div class="ov-nav__group" data-group="{groep["key"]}">')
        parts.append(
            f'      <button type="button" class="ov-nav__toggle" '
            f'aria-haspopup="true" aria-expanded="false">'
            f'{groep["label"]} <span aria-hidden="true">▾</span></button>'
        )
        # Groep 'edities' krijgt --wide voor bredere dropdown
        menu_cls = "ov-nav__menu ov-nav__menu--wide" if groep["key"] == "edities" else "ov-nav__menu"
        parts.append(f'      <div class="{menu_cls}" role="menu">')
        # Groepeer sub_van items direct achter hun ouder
        rendered_keys = set()
        items = groep["items"]
        for i, item in enumerate(items):
            if item["key"] in rendered_keys or item.get("sub_van"):
                continue
            if item["scheiding_boven"]:
                parts.append('        <hr>')
            fb_cls = ' class="ov-nav__fallback"' if item["is_fallback"] else ""
            parts.append(f'        <a href="{item["url"]}"{fb_cls}>{item["label"]}</a>')
            rendered_keys.add(item["key"])
            # Zoek eventuele sub_van-kinderen
            children = [c for c in items if c.get("sub_van") == item["key"]]
            if children:
                parts.append('        <span class="ov-nav__sub">')
                for child in children:
                    fb_cls = ' class="ov-nav__fallback"' if child["is_fallback"] else ""
                    parts.append(f'          <a href="{child["url"]}"{fb_cls}>{child["label"]}</a>')
                    rendered_keys.add(child["key"])
                parts.append('        </span>')
        parts.append('      </div>')
        parts.append('    </div>')
    parts.append('  </div>')
    parts.append('</nav>')
    return "\n".join(parts)


def inject_nav(html: str, new_nav_html: str) -> str:
    """Vervang eerste <nav>...</nav>. Voegt CSS+JS toe als markers ontbreken."""
    # 1. Vervang <nav>-blok
    new_html, count = re.subn(
        r"<nav\b[^>]*>.*?</nav>",
        lambda m: new_nav_html,
        html, count=1, flags=re.S,
    )
    if count == 0:
        raise RuntimeError("Geen <nav>-blok gevonden om te vervangen")

    # 2. Verwijder eerder geïnjecteerde ov-nav v2 CSS/JS blokken
    new_html = re.sub(
        r"<style>\s*\n\s*/\* ov-nav v2.*?</style>\s*",
        "",
        new_html, flags=re.S,
    )
    new_html = re.sub(
        r"<script>\s*/\* ov-nav v2.*?</script>\s*",
        "",
        new_html, flags=re.S,
    )
    # 3. Injecteer verse CSS vóór </head>
    if "</head>" not in new_html:
        raise RuntimeError("Geen </head> gevonden")
    new_html = new_html.replace("</head>", NAV_CSS + "</head>", 1)
    # 4. Injecteer JS vóór </body>
    if "</body>" not in new_html:
        raise RuntimeError("Geen </body> gevonden")
    new_html = new_html.replace("</body>", NAV_JS + "</body>", 1)

    return new_html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Canonieke menuconfigurator")
    ap.add_argument("--dry-run", action="store_true", help="Print alleen; schrijf niets")
    ap.add_argument("--only", help="Kommagescheiden talen (bv. 'nl,en')")
    args = ap.parse_args()

    if not CONFIG_PATH.exists():
        print(f"Fout: {CONFIG_PATH} niet gevonden", file=sys.stderr)
        sys.exit(1)

    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    talen = config["talen"]
    if args.only:
        keep = set(t.strip() for t in args.only.split(","))
        talen = [t for t in talen if t in keep]

    print(f"Talen: {talen}")
    print(f"Groepen: {len(config['groepen'])}")
    for g in config["groepen"]:
        print(f"  · {g['key']:12} — {len(g['items'])} items")

    # 1. Bouw menu-data
    menu_data = build_menu_data(config)

    # 2. Schrijf JSON per taal
    if not args.dry_run:
        JSON_DIR.mkdir(parents=True, exist_ok=True)
    for taal in talen:
        json_path = JSON_DIR / f"{taal}.json"
        payload = json.dumps(menu_data[taal], ensure_ascii=False, indent=2)
        if args.dry_run:
            print(f"\n[dry-run] Zou schrijven: {json_path}")
        else:
            json_path.write_text(payload, encoding="utf-8")
            print(f"  ✓ {json_path.relative_to(REPO)}")

    # 3. Render HTML en injecteer
    total_fallbacks = 0
    for taal in talen:
        nav_html = render_nav_html(menu_data[taal])
        index_path = REPO / taal / "index.html"
        if not index_path.exists():
            print(f"  ! Skip: {index_path.relative_to(REPO)} bestaat niet")
            continue
        html = index_path.read_text(encoding="utf-8")
        try:
            new_html = inject_nav(html, nav_html)
        except RuntimeError as e:
            print(f"  ! [{taal}] fout: {e}")
            continue

        # Tel fallbacks in deze taal
        fbs = sum(1 for g in menu_data[taal]["groepen"] for it in g["items"] if it["is_fallback"])
        total_fallbacks += fbs
        fb_note = f" — {fbs} fallback(s) naar NL" if fbs else ""

        if args.dry_run:
            print(f"\n[dry-run] [{taal}] Zou schrijven: {index_path.relative_to(REPO)}{fb_note}")
        else:
            index_path.write_text(new_html, encoding="utf-8")
            print(f"  ✓ [{taal}] {index_path.relative_to(REPO)}{fb_note}")

    print(f"\nKlaar. Totale fallbacks: {total_fallbacks}")


if __name__ == "__main__":
    main()
