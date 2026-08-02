#!/usr/bin/env python3
"""Chirurgisch script: vervang het bestaande 'Delen'-dropdown-blok in de nav
door een interactief deel-menu met vier acties (PDF, Facebook, Kopieer, E-mail).

Werkwijze:
  1. Vind <div class="ov-nav__dropdown"> ... </div> waarin het hoofd-item het
     labelwoord 'Delen' / 'Share' / 'Teilen' / ... draagt en waarvan de eerste
     subitem naar een /*/delen.html-achtige pagina wijst.
  2. Vervang alleen die ene div door de deel-dropdown-versie met data-attributen
     (vertaalstrings uit menu-config.yaml).
  3. Injecteer <link> naar assets/deel-menu.css in <head> en <script defer> naar
     assets/deel-menu.js voor </body>, indien nog niet aanwezig.

Idempotent: pagina's die al ov-deel bevatten worden overgeslagen.
Alleen de <nav> wordt aangeraakt — alle andere content blijft ongewijzigd.

Gebruik:
  python3 scripts/deel_dropdown_inspuiten.py --check nl/pad/artikel.html
  python3 scripts/deel_dropdown_inspuiten.py --dry-run --only nl
  python3 scripts/deel_dropdown_inspuiten.py                  # alle talen
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO / "nl/_data/menu-config.yaml"

# Alle mogelijke labels + hun taalcode (voor woord-detectie in de nav)
DELEN_LABELS = {
    "nl": "Delen",
    "en": "Share",
    "de": "Teilen",
    "ru": "Поделиться",
    "es": "Compartir",
    "fr": "Partager",
    "it": "Condividere",
    "pt": "Partilhar",
}
# Alle URL-woorden die als eerste sub-item wijzen op de "Delen"-dropdown
DELEN_URL_WORDS = ["delen", "share", "teilen", "podelitsya", "compartir", "partager", "condividi", "condividere", "partilhar"]

DEEL_CSS_TAG = '  <link rel="stylesheet" href="{prefix}assets/deel-menu.css">'
DEEL_JS_TAG  = '  <script defer src="{prefix}assets/deel-menu.js"></script>'


def escape_attr(s: str) -> str:
    return (str(s or "")
            .replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_deel_item(config: dict) -> dict:
    for item in config.get("items", []):
        if item.get("is_deel_menu") or item.get("key") == "delen":
            return item
    raise RuntimeError("Geen delen-item gevonden in menu-config.yaml")


def build_deel_dropdown_html(deel_item: dict, taal: str) -> str:
    """Bouw de vervangings-HTML voor de deel-dropdown in de opgegeven taal."""
    msgs = deel_item.get("deel_msgs", {})
    acties = deel_item.get("deel_acties", {})

    def m(key: str) -> str:
        val = msgs.get(key, {})
        return val.get(taal, val.get("nl", "")) if isinstance(val, dict) else ""

    def actie_label(key: str) -> str:
        val = acties.get(key, {}).get("labels", {})
        return val.get(taal, val.get("nl", key))

    hoofd_label = deel_item.get("labels", {}).get(taal, "Delen")

    data_attrs = {
        "data-ov-deel":         "",
        "data-msg-copied":      m("copied"),
        "data-msg-copy-prompt": m("copyPrompt"),
        "data-mail-subject":    m("mailSubject"),
        "data-mail-footer":     m("mailFooter"),
        "data-pdf-building":    m("pdfBuilding"),
        "data-pdf-done":        m("pdfDone"),
        "data-pdf-fail":        m("pdfFail"),
        "data-pdf-source":      m("pdfSource"),
        "data-pdf-note":        m("pdfNote"),
        "data-msg-instagram-copied": m("msgInstagramCopied"),
        "data-msg-tik-tok-copied":   m("msgTikTokCopied"),
        "data-x-via":           m("xVia"),
        "data-gate-title":      m("gateTitle"),
        "data-gate-body":       m("gateBody"),
        "data-gate-submit":     m("gateSubmit"),
        "data-gate-cancel":     m("gateCancel"),
        "data-gate-checking":   m("gateChecking"),
        "data-gate-invalid":    m("gateInvalid"),
        "data-gate-wrong":      m("gateWrong"),
        "data-gate-server-error": m("gateServerError"),
        "data-gate-note":       m("gateNote"),
    }
    attr_str = " ".join(
        (k if v == "" else f'{k}="{escape_attr(v)}"')
        for k, v in data_attrs.items()
    )

    # Volgorde in het menu: PDF eerst, dan sociale netwerken, dan link/mail
    knoppen = [
        ("pdf",       "🔒 " + escape_attr(actie_label("pdf"))),
        ("facebook",  escape_attr(actie_label("facebook"))),
        ("x",         escape_attr(actie_label("x"))),
        ("linkedin",  escape_attr(actie_label("linkedin"))),
        ("whatsapp",  escape_attr(actie_label("whatsapp"))),
        ("telegram",  escape_attr(actie_label("telegram"))),
        ("instagram", escape_attr(actie_label("instagram"))),
        ("tiktok",    escape_attr(actie_label("tiktok"))),
        ("copy",      escape_attr(actie_label("copy"))),
        ("email",     escape_attr(actie_label("email"))),
    ]
    knop_rijen = "\n".join(
        f'        <a class="ov-nav__subitem" href="#" data-ov-deel-action="{actie}"><span class="ov-deel-label">{label}</span></a>'
        for actie, label in knoppen
    )
    return (
        f'<div class="ov-nav__dropdown ov-deel" {attr_str}>\n'
        f'      <a class="ov-nav__item" href="#">{escape_attr(hoofd_label)}<span class="ov-nav__caret">▾</span></a>\n'
        f'      <div class="ov-nav__submenu">\n'
        f'{knop_rijen}\n'
        f'      </div>\n'
        f'    </div>'
    )


def detect_taal(page_path: Path) -> str | None:
    """Taalcode = eerste path-segment (nl/en/de/…). Werkt met relatief én absoluut pad."""
    page_abs = page_path if page_path.is_absolute() else (REPO / page_path).resolve()
    try:
        rel = page_abs.relative_to(REPO)
    except ValueError:
        # Geen deel van repo, fallback op eerste segment van gegeven pad
        parts = page_path.parts
    else:
        parts = rel.parts
    if parts and parts[0] in DELEN_LABELS:
        return parts[0]
    return None


def compute_asset_prefix(page_path: Path) -> str:
    """Aantal '../' om vanaf de pagina bij assets/ te komen.

    /home/user/workspace/openvizier/nl/index.html            -> depth 1 -> '../'
    /home/user/workspace/openvizier/nl/wat-opkomt/foo.html   -> depth 2 -> '../../'
    """
    page_abs = page_path if page_path.is_absolute() else (REPO / page_path).resolve()
    rel = page_abs.relative_to(REPO)
    return "../" * (len(rel.parts) - 1)


# Regex om de "Delen"-dropdown-div te vinden. Match:
#   <div class="ov-nav__dropdown">   (mag ook extra classes hebben)
#     <a class="ov-nav__item" href="#">{Label}<span class="ov-nav__caret">▾</span></a>
#     <div class="ov-nav__submenu">
#       ... (subitems, waarvan minstens één link naar */delen.html of vergelijkbaar) ...
#     </div>
#   </div>
DELEN_DROPDOWN_RE = re.compile(
    r'<div class="ov-nav__dropdown[^"]*">\s*'
    r'<a class="ov-nav__item"[^>]*>([^<]+)<span class="ov-nav__caret">▾</span></a>\s*'
    r'<div class="ov-nav__submenu">\s*'
    r'(.*?)'
    r'</div>\s*'
    r'</div>',
    re.DOTALL,
)


def is_delen_dropdown(match_label: str, submenu_html: str, taal: str) -> bool:
    """Bepaal of dit de 'Delen'-dropdown is (i.p.v. een andere dropdown zoals Verkennen)."""
    expected = DELEN_LABELS.get(taal, "").lower()
    if expected and expected in match_label.strip().lower():
        return True
    # Fallback: zoek in het submenu een href naar */delen.html o.i.d.
    for word in DELEN_URL_WORDS:
        if re.search(rf'href="[^"]*/{word}\.html"', submenu_html):
            return True
    return False


# Regex om een BESTAAND ov-deel dropdown-blok te vinden (voor upgrade).
OV_DEEL_DROPDOWN_RE = re.compile(
    r'<div class="ov-nav__dropdown[^"]*ov-deel[^"]*"[^>]*>.*?</div>\s*</div>',
    re.DOTALL,
)


def inject_page(page_path: Path, deel_item: dict, verbose: bool = False) -> tuple[bool, str]:
    """Vervang het delen-dropdown-blok op één pagina. Return (changed, reason).

    Twee scenarios:
      A. Pagina heeft nog GEEN ov-deel → zoek oude delen-dropdown en vervang.
      B. Pagina heeft AL ov-deel → vervang het volledige ov-deel blok
         (upgrade naar nieuwe versie met extra knoppen).
    """
    taal = detect_taal(page_path)
    if not taal:
        return False, "geen taalcode in pad"

    html = page_path.read_text(encoding="utf-8", errors="ignore")
    nieuwe_html_snippet = build_deel_dropdown_html(deel_item, taal)

    # Scenario B: bestaand ov-deel blok upgraden
    if "data-ov-deel" in html:
        new_html, n = OV_DEEL_DROPDOWN_RE.subn(nieuwe_html_snippet, html, count=1)
        if n == 1 and new_html != html:
            # Assets zijn er waarschijnlijk al, maar checken kan geen kwaad
            prefix = compute_asset_prefix(page_path)
            if 'assets/deel-menu.css' not in new_html and '</head>' in new_html:
                new_html = new_html.replace('</head>', DEEL_CSS_TAG.format(prefix=prefix) + '\n</head>', 1)
            if 'assets/deel-menu.js' not in new_html and '</body>' in new_html:
                new_html = new_html.replace('</body>', DEEL_JS_TAG.format(prefix=prefix) + '\n</body>', 1)
            page_path.write_text(new_html, encoding="utf-8")
            return True, "upgrade van bestaand ov-deel"
        return False, "ov-deel-marker aanwezig maar blok niet matchbaar"

    # Scenario A: eerste installatie — zoek oude delen-dropdown
    replaced = False

    def _replace(match):
        nonlocal replaced
        if replaced:
            return match.group(0)
        label = match.group(1)
        submenu = match.group(2)
        if not is_delen_dropdown(label, submenu, taal):
            return match.group(0)
        replaced = True
        return nieuwe_html_snippet

    new_html = DELEN_DROPDOWN_RE.sub(_replace, html)

    if not replaced:
        return False, "geen delen-dropdown gevonden"

    # Assets toevoegen (idempotent)
    prefix = compute_asset_prefix(page_path)
    if 'assets/deel-menu.css' not in new_html and '</head>' in new_html:
        new_html = new_html.replace('</head>', DEEL_CSS_TAG.format(prefix=prefix) + '\n</head>', 1)
    if 'assets/deel-menu.js' not in new_html and '</body>' in new_html:
        new_html = new_html.replace('</body>', DEEL_JS_TAG.format(prefix=prefix) + '\n</body>', 1)

    if new_html == html:
        return False, "geen wijzigingen na regex-run"

    page_path.write_text(new_html, encoding="utf-8")
    return True, "OK"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Rapporteer wat er zou gebeuren, schrijf niet.")
    ap.add_argument("--only", metavar="TAAL", help="Beperk tot één taal (nl/en/de/...)")
    ap.add_argument("--check", metavar="PAD", help="Toon voor één pagina wat gedetecteerd wordt (geen wijziging)")
    args = ap.parse_args()

    config = load_config()
    deel_item = find_deel_item(config)

    if args.check:
        page = Path(args.check)
        if not page.is_absolute():
            page = REPO / page
        taal = detect_taal(page)
        print(f"Taal: {taal}")
        html = page.read_text(encoding="utf-8", errors="ignore")
        matches = list(DELEN_DROPDOWN_RE.finditer(html))
        print(f"Dropdowns gevonden: {len(matches)}")
        for i, m in enumerate(matches):
            label = m.group(1).strip()
            hit = is_delen_dropdown(label, m.group(2), taal or "nl")
            print(f"  {i+1}. label='{label}' — is_delen={hit}")
        print(f"\nVervangings-HTML voor taal {taal}:\n")
        print(build_deel_dropdown_html(deel_item, taal or "nl"))
        return

    talen = [args.only] if args.only else list(DELEN_LABELS.keys())
    totaal_ok = 0
    totaal_skip = 0
    per_taal = {}

    for taal in talen:
        taal_dir = REPO / taal
        if not taal_dir.is_dir():
            continue
        pages = list(taal_dir.rglob("*.html"))
        ok = 0
        skip = 0
        redenen = {}
        for page in pages:
            # Skip corrupte pagina's zonder </head>
            head = page.read_text(encoding="utf-8", errors="ignore")
            if "</head>" not in head or "</body>" not in head:
                skip += 1
                redenen["geen </head>/</body>"] = redenen.get("geen </head>/</body>", 0) + 1
                continue
            if args.dry_run:
                # Simuleer: heeft de pagina een delen-dropdown?
                has_delen = False
                for m in DELEN_DROPDOWN_RE.finditer(head):
                    if is_delen_dropdown(m.group(1), m.group(2), taal):
                        has_delen = True
                        break
                if has_delen and "data-ov-deel" not in head:
                    ok += 1
                else:
                    skip += 1
                    reden = "al voorzien" if "data-ov-deel" in head else "geen delen-dropdown"
                    redenen[reden] = redenen.get(reden, 0) + 1
            else:
                changed, reden = inject_page(page, deel_item)
                if changed:
                    ok += 1
                else:
                    skip += 1
                    redenen[reden] = redenen.get(reden, 0) + 1
        per_taal[taal] = (ok, skip, redenen)
        totaal_ok += ok
        totaal_skip += skip
        print(f"[{taal}] {ok} gewijzigd, {skip} overgeslagen")
        for reden, aantal in redenen.items():
            print(f"    · {aantal}× {reden}")

    print(f"\n{'DRY-RUN' if args.dry_run else 'KLAAR'}: {totaal_ok} pagina's gewijzigd, {totaal_skip} overgeslagen")


if __name__ == "__main__":
    main()
