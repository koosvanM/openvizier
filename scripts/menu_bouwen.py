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
  /* ov-nav v6 — platte horizontale nav met zachte, rustige dropdown-overgangen */
  .ov-nav { background:#faf8f3; border-top:1px solid #d4d1ca; border-bottom:1px solid #d4d1ca; position:relative; z-index:200; }
  .ov-nav__inner { max-width:1180px; margin:0 auto; padding:0.35rem 0.5rem; display:flex; gap:0.15rem; justify-content:center; flex-wrap:wrap; }
  .ov-nav__item {
    display:inline-block; padding:0.7rem 1rem; font:inherit; color:#1a1a1a !important;
    font-weight:600; letter-spacing:0.02em; text-decoration:none !important; border-radius:4px;
    font-size:0.95rem; line-height:1.2;
    transition: background-color 180ms ease-out, color 180ms ease-out;
  }
  .ov-nav__item:hover { background:#f0ede4; color:#7a1f2b !important; }
  .ov-nav__item--current { color:#7a1f2b !important; border-bottom:2px solid #d4af37; }
  .ov-nav__item--fallback { color:#9ca3af !important; font-style:italic; }

  /* Dropdown — zachte fade + subtiele glide, geen snap-open */
  .ov-nav__dropdown { position:relative; display:inline-block; }
  .ov-nav__caret { font-size:0.8em; margin-left:0.15rem; opacity:0.6; }
  .ov-nav__submenu {
    position:absolute; top:100%; left:0; min-width:220px;
    background:#ffffff; border:1px solid #d4d1ca;
    box-shadow:0 8px 24px rgba(0,0,0,0.10);
    padding:0.4rem 0; z-index:1000; border-radius:4px;
    /* Startpositie: onzichtbaar, licht omhoog, geen interactie */
    opacity:0; visibility:hidden;
    transform: translateY(-4px);
    transition: opacity 180ms ease-out, transform 180ms ease-out, visibility 0s linear 180ms;
  }
  /* Buffer-strook direct onder het menu-item voorkomt "gap-flicker" */
  .ov-nav__dropdown::after {
    content:""; position:absolute; top:100%; left:0; right:0; height:8px;
    pointer-events:auto;
  }
  .ov-nav__dropdown:hover .ov-nav__submenu,
  .ov-nav__dropdown:focus-within .ov-nav__submenu {
    opacity:1; visibility:visible; transform: translateY(0);
    transition: opacity 180ms ease-out, transform 180ms ease-out, visibility 0s linear 0s;
  }

  .ov-nav__subitem {
    display:block; padding:0.55rem 1.1rem; color:#1a1a1a !important;
    text-decoration:none !important; font-size:0.94rem; font-weight:500; line-height:1.35;
    transition: background-color 150ms ease-out, color 150ms ease-out;
  }
  .ov-nav__subitem:hover { background:#f5f3ee; color:#7a1f2b !important; }
  .ov-nav__subitem--fallback { color:#9ca3af !important; font-style:italic; }

  @media (max-width:720px) {
    .ov-nav__inner { padding:0.25rem 0.5rem; gap:0; }
    .ov-nav__item { padding:0.55rem 0.75rem; font-size:0.9rem; }
    .ov-nav__submenu {
      position:static; box-shadow:none; border:0; padding:0 0 0.35rem 1rem;
      min-width:0; background:transparent;
      /* Op mobiel geen fade/translate — gewoon direct tonen bij tap */
      opacity:1; visibility:visible; transform:none; transition:none;
      display:none;
    }
    .ov-nav__dropdown::after { display:none; }
    .ov-nav__dropdown:hover .ov-nav__submenu,
    .ov-nav__dropdown:focus-within .ov-nav__submenu { display:block; }
  }

  /* Respecteer 'reduced motion' — zet alle overgangen uit */
  @media (prefers-reduced-motion: reduce) {
    .ov-nav__item, .ov-nav__subitem, .ov-nav__submenu { transition:none !important; }
    .ov-nav__submenu { transform:none !important; }
  }
</style>
"""

NAV_JS = """"""

# Markers om oude/nieuwe blokken te herkennen bij regenereren
CSS_MARKER = "/* ov-nav v5"
JS_MARKER  = None  # geen JS meer nodig in v5

# Deel-menu assets (aparte CSS/JS, opgenomen op elke pagina met een <nav>)
DEEL_CSS_LINK = '<link rel="stylesheet" href="{prefix}assets/deel-menu.css">'
DEEL_JS_TAG   = '<script defer src="{prefix}assets/deel-menu.js"></script>'
DEEL_ASSET_MARKER = 'assets/deel-menu.'


# ---------------------------------------------------------------------------
# Kern-logica
# ---------------------------------------------------------------------------

def resolve_url(item: dict, taal: str, fallback: str = "nl") -> tuple[str, bool]:
    """Return (url_relatief_aan_taalroot, is_fallback).

    Als url leeg is voor de gevraagde taal → val terug op fallback-taal.
    De teruggegeven URL is altijd relatief aan de taal-root (bv. 'wat-opkomt/'
    of '../nl/toekomst/'). De pagina-diepte-prefix wordt later toegepast in
    apply_depth_prefix().
    """
    urls = item.get("urls", {})
    url = urls.get(taal, "")
    if url:
        return url, False
    fb_url = urls.get(fallback, "")
    if not fb_url:
        return "#", True
    if fb_url == "./":
        return f"../{fallback}/", True
    return f"../{fallback}/{fb_url}", True


def apply_depth_prefix(url: str, depth: int) -> str:
    """Pas '../' per niveau diepte toe. depth=0 voor {taal}/index.html.

    - './' → '../' × depth (voor depth=0 blijft './')
    - 'wat-opkomt/' → '../×depth' + 'wat-opkomt/'
    - '../nl/toekomst/' → '../×depth' + '../nl/toekomst/'
    - Absolute URLs (http, mailto, #) blijven ongewijzigd
    """
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return url
    if depth == 0:
        return url
    prefix = "../" * depth
    if url == "./":
        return prefix
    return prefix + url


def build_menu_data(config: dict) -> dict[str, dict]:
    """Bouw per taal een dict {items: [...]} met resolved URLs (v4 plat, met optionele sub-items)."""
    result = {}
    for taal in config["talen"]:
        items_out = []
        for item in config["items"]:
            url, is_fallback = resolve_url(item, taal)
            item_data = {
                "key": item["key"],
                "label": item["labels"].get(taal, item["labels"]["nl"]),
                "url": url,
                "is_fallback": is_fallback,
            }
            # Sub-items zijn optioneel (dropdown-menu)
            if "sub_items" in item and item["sub_items"]:
                subs_out = []
                for sub in item["sub_items"]:
                    sub_url, sub_fb = resolve_url(sub, taal)
                    subs_out.append({
                        "key": sub["key"],
                        "label": sub["labels"].get(taal, sub["labels"]["nl"]),
                        "url": sub_url,
                        "is_fallback": sub_fb,
                    })
                item_data["sub_items"] = subs_out
            # Deel-menu (speciaal): kopieer acties + msgs voor deze taal
            if item.get("is_deel_menu"):
                item_data["is_deel_menu"] = True
                acties = item.get("deel_acties", {})
                item_data["deel_acties"] = {
                    key: {"label": val.get("labels", {}).get(taal, val.get("labels", {}).get("nl", key))}
                    for key, val in acties.items()
                }
                msgs = item.get("deel_msgs", {})
                item_data["deel_msgs"] = {
                    key: val.get(taal, val.get("nl", ""))
                    for key, val in msgs.items()
                }
            items_out.append(item_data)
        result[taal] = {"taal": taal, "items": items_out}
    return result


def _escape_attr(s: str) -> str:
    return (str(s)
            .replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def render_deel_dropdown(item: dict) -> list[str]:
    """Render het speciale deel-menu als dropdown met 4 actie-knoppen.

    Metadata (vertalingen, aanmeld-pad) worden op de container gezet via
    data-* attributen, zodat assets/deel-menu.js ze kan lezen.
    """
    msgs = item.get("deel_msgs", {})
    acties = item.get("deel_acties", {})

    # data-* attributen (leeg attribuut = boolean-marker voor JS-detectie)
    data_attrs = {
        "data-ov-deel":         "",
        "data-msg-copied":      msgs.get("copied", ""),
        "data-msg-copy-prompt": msgs.get("copyPrompt", ""),
        "data-mail-subject":    msgs.get("mailSubject", ""),
        "data-mail-footer":     msgs.get("mailFooter", ""),
        "data-pdf-building":    msgs.get("pdfBuilding", ""),
        "data-pdf-done":        msgs.get("pdfDone", ""),
        "data-pdf-fail":        msgs.get("pdfFail", ""),
        "data-pdf-source":      msgs.get("pdfSource", ""),
        "data-pdf-note":        msgs.get("pdfNote", ""),
        "data-gate-title":      msgs.get("gateTitle", ""),
        "data-gate-body":       msgs.get("gateBody", ""),
        "data-gate-submit":     msgs.get("gateSubmit", ""),
        "data-gate-cancel":     msgs.get("gateCancel", ""),
        "data-gate-checking":   msgs.get("gateChecking", ""),
        "data-gate-invalid":    msgs.get("gateInvalid", ""),
        "data-gate-wrong":      msgs.get("gateWrong", ""),
        "data-gate-server-error": msgs.get("gateServerError", ""),
        "data-gate-note":       msgs.get("gateNote", ""),
    }
    # data-* attributen renderen (leeg attribuut = boolean)
    attr_str = " ".join(
        (k if v == "" else f'{k}="{_escape_attr(v)}"')
        for k, v in data_attrs.items()
    )

    pdf_label      = acties.get("pdf", {}).get("label", "PDF")
    facebook_label = acties.get("facebook", {}).get("label", "Facebook")
    copy_label     = acties.get("copy", {}).get("label", "Copy")
    email_label    = acties.get("email", {}).get("label", "E-mail")

    label = item["label"]
    return [
        f'    <div class="ov-nav__dropdown ov-deel" {attr_str}>',
        f'      <a class="ov-nav__item ov-nav__item--has-dropdown" href="{item["url"]}">{label} <span aria-hidden="true" class="ov-nav__caret">▾</span></a>',
        f'      <div class="ov-nav__submenu">',
        f'        <a class="ov-nav__subitem" href="#" data-ov-deel-action="pdf"><span class="ov-deel-label">🔒 {_escape_attr(pdf_label)}</span></a>',
        f'        <a class="ov-nav__subitem" href="#" data-ov-deel-action="facebook"><span class="ov-deel-label">{_escape_attr(facebook_label)}</span></a>',
        f'        <a class="ov-nav__subitem" href="#" data-ov-deel-action="copy"><span class="ov-deel-label">{_escape_attr(copy_label)}</span></a>',
        f'        <a class="ov-nav__subitem" href="#" data-ov-deel-action="email"><span class="ov-deel-label">{_escape_attr(email_label)}</span></a>',
        f'      </div>',
        f'    </div>',
    ]


def render_nav_html(menu_data: dict) -> str:
    """Genereer platte <nav>-HTML voor één taal (v4+). Ondersteunt optionele dropdown per item."""
    items = menu_data["items"]
    parts = ['<nav class="ov-nav" aria-label="Hoofdmenu">']
    parts.append('  <div class="ov-nav__inner">')
    for item in items:
        # Speciaal item: deel-menu
        if item.get("is_deel_menu"):
            parts.extend(render_deel_dropdown(item))
            continue
        classes = ["ov-nav__item"]
        if item["is_fallback"]:
            classes.append("ov-nav__item--fallback")
        subs = item.get("sub_items")
        if subs:
            classes.append("ov-nav__item--has-dropdown")
            cls = " ".join(classes)
            parts.append(f'    <div class="ov-nav__dropdown">')
            parts.append(f'      <a class="{cls}" href="{item["url"]}">{item["label"]} <span aria-hidden="true" class="ov-nav__caret">▾</span></a>')
            parts.append(f'      <div class="ov-nav__submenu">')
            for sub in subs:
                sub_classes = ["ov-nav__subitem"]
                if sub["is_fallback"]:
                    sub_classes.append("ov-nav__subitem--fallback")
                sub_cls = " ".join(sub_classes)
                parts.append(f'        <a class="{sub_cls}" href="{sub["url"]}">{sub["label"]}</a>')
            parts.append(f'      </div>')
            parts.append(f'    </div>')
        else:
            cls = " ".join(classes)
            parts.append(f'    <a class="{cls}" href="{item["url"]}">{item["label"]}</a>')
    parts.append('  </div>')
    parts.append('</nav>')
    return "\n".join(parts)


def inject_nav(html: str, new_nav_html: str, deel_prefix: str = "") -> str:
    """Vervang eerste <nav>...</nav>. Voegt CSS+JS toe als markers ontbreken.

    Werkt zowel voor <nav class="ov-nav"> (nieuw) als <nav class="nav">
    (legacy) en elke andere <nav>-vorm. Idempotent.

    Voegt ook éénmalig de deel-menu assets toe (assets/deel-menu.css/.js),
    tenzij die er al staan.
    """
    new_html, count = re.subn(
        r"<nav\b[^>]*>.*?</nav>",
        lambda m: new_nav_html,
        html, count=1, flags=re.S,
    )
    if count == 0:
        raise RuntimeError("Geen <nav>-blok gevonden om te vervangen")

    # Verwijder alle eerder geïnjecteerde ov-nav CSS/JS blokken (v2 t/m v5)
    new_html = re.sub(
        r"<style>\s*\n?\s*/\* ov-nav v[2345].*?</style>\s*",
        "",
        new_html, flags=re.S,
    )
    new_html = re.sub(
        r"<script>\s*/\* ov-nav v[2345].*?</script>\s*",
        "",
        new_html, flags=re.S,
    )
    if "</head>" not in new_html:
        raise RuntimeError("Geen </head> gevonden")
    new_html = new_html.replace("</head>", NAV_CSS + "</head>", 1)
    # v4: geen JS meer nodig, skip injectie
    if NAV_JS.strip():
        if "</body>" not in new_html:
            raise RuntimeError("Geen </body> gevonden")
        new_html = new_html.replace("</body>", NAV_JS + "</body>", 1)

    # Deel-menu assets (CSS in <head>, JS voor </body>)
    if DEEL_ASSET_MARKER not in new_html:
        css_link = DEEL_CSS_LINK.format(prefix=deel_prefix)
        js_tag   = DEEL_JS_TAG.format(prefix=deel_prefix)
        new_html = new_html.replace("</head>", "  " + css_link + "\n</head>", 1)
        if "</body>" in new_html:
            new_html = new_html.replace("</body>", "  " + js_tag + "\n</body>", 1)
        else:
            new_html = new_html + "\n" + js_tag + "\n"
    return new_html


def find_pages(taal: str) -> list[Path]:
    """Alle HTML-paginas onder {taal}/ die een <nav>-blok bevatten.

    Uitzonderingen: talenring-, splash- en embed-paginas die eigen layout hebben.
    """
    root = REPO / taal
    if not root.exists():
        return []
    pages = []
    for p in root.rglob("*.html"):
        # Skip specials
        name = p.name.lower()
        if "talenring" in name or "splash" in name or "embed" in name:
            continue
        # Skip _data en assets
        if "_data" in p.parts or "assets" in p.parts:
            continue
        # Alleen paginas met een <nav>-blok
        try:
            html = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not re.search(r"<nav\b", html):
            continue
        pages.append(p)
    return pages


def page_depth(page: Path, taal: str) -> int:
    """Aantal directories tussen page en taalroot.

    - {taal}/index.html → 0
    - {taal}/toekomst/index.html → 1
    - {taal}/wat-opkomt/artikel.html → 1
    """
    rel = page.relative_to(REPO / taal)
    # Aantal parent-directories (rel.parents heeft altijd tenminste '.').
    parts = rel.parts
    return len(parts) - 1  # laatste is de filename


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
    print(f"Items: {len(config['items'])}")
    for it in config["items"]:
        print(f"  · {it['key']:14} — {it['labels'].get('nl','?')}")

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

    # 3. Render HTML en injecteer op ALLE paginas per taal
    total_pages = 0
    total_fails = 0
    for taal in talen:
        pages = find_pages(taal)
        print(f"\n[{taal}] {len(pages)} pagina's met een <nav>-blok")
        ok = 0
        fails = 0
        for page in pages:
            depth = page_depth(page, taal)
            # Bouw menu-data met correcte prefix voor deze diepte
            def _adjust(it):
                out = {**it, "url": apply_depth_prefix(it["url"], depth)}
                if it.get("sub_items"):
                    out["sub_items"] = [
                        {**s, "url": apply_depth_prefix(s["url"], depth)}
                        for s in it["sub_items"]
                    ]
                return out
            adjusted = {
                "taal": taal,
                "items": [_adjust(it) for it in menu_data[taal]["items"]],
            }
            nav_html = render_nav_html(adjusted)
            # Diepte-prefix voor de deel-menu assets (../× depth naar site-root, dan taal/../ = één omhoog vanaf taal)
            deel_prefix = ("../" * (depth + 1))  # +1 om uit de taalmap te komen
            try:
                html = page.read_text(encoding="utf-8", errors="ignore")
                new_html = inject_nav(html, nav_html, deel_prefix=deel_prefix)
            except RuntimeError as e:
                fails += 1
                print(f"  ! {page.relative_to(REPO)}: {e}")
                continue
            if args.dry_run:
                pass
            else:
                page.write_text(new_html, encoding="utf-8")
            ok += 1
        print(f"  ✓ {ok} pagina's, {fails} mislukt")
        total_pages += ok
        total_fails += fails

    print(f"\nKlaar. Totaal aangepast: {total_pages} — mislukt: {total_fails}")


if __name__ == "__main__":
    main()
