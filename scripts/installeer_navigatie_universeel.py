#!/usr/bin/env python3
"""Installeer een uniforme, Apple-stijl navigatie op ÉLKE HTML-pagina:

1. Top-nav krijgt een slimme TAAL-popover met alle 8 talen.
   Elke link wijst naar het exacte equivalent van die pagina in die taal
   (of valide fallback uit _pad_mapping.json).

2. Onderaan élke artikel-/sectiepagina (alles behalve splash, verkennen-embed)
   komt een uniforme bottom-bar:
      ← Terug naar [sectie]    ⌂ Voorpagina    ↻ Verkennen

3. Idempotent: bestaande inline TAAL-link wordt vervangen, bestaande
   bottom-bar wordt vervangen.

Werkt voor alle 8 talen, gebruikt scripts/_pad_mapping.json voor cross-link.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPPING = json.loads((ROOT / "scripts" / "_pad_mapping.json").read_text(encoding="utf-8"))

LANGS = ["nl", "de", "en", "ru", "es", "fr", "it", "pt"]

LANG_LABEL = {
    "nl": "Nederlands",
    "de": "Deutsch",
    "en": "English",
    "ru": "Русский",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
    "pt": "Português",
}

DIR_NORM = {
    "nl": {"wat-opkomt": "wat-opkomt", "dossiers": "dossiers", "onderzoek": "onderzoek",
           **{f"editie-{i}": f"editie-{i}" for i in range(7)}},
    "de": {"was-aufkommt": "wat-opkomt", "dossiers": "dossiers", "forschung": "onderzoek",
           **{f"ausgabe-{i}": f"editie-{i}" for i in range(7)}},
    "en": {"what-surfaces": "wat-opkomt", "dossiers": "dossiers", "research": "onderzoek",
           **{f"edition-{i}": f"editie-{i}" for i in range(7)}},
    "ru": {"chto-vsplyvaet": "wat-opkomt", "dossiers": "dossiers", "issledovanie": "onderzoek",
           **{f"vypusk-{i}": f"editie-{i}" for i in range(7)}},
    "es": {"lo-que-emerge": "wat-opkomt", "edicion-0": "editie-0"},
    "fr": {"ce-qui-emerge": "wat-opkomt", "edition-0": "editie-0"},
    "it": {"cio-che-emerge": "wat-opkomt", "edizione-0": "editie-0"},
    "pt": {"o-que-emerge": "wat-opkomt", "edicao-0": "editie-0"},
}

# Per taal: termen voor bottom-bar
T = {
    "nl": {"terug": "Terug naar", "voor": "Voorpagina", "verk": "Verkennen", "taal": "Taal",
           "sec": {"wat-opkomt": "Wat opkomt", "verkennen.html": "Verkennen",
                   "editie-0": "Editie Europa", "editie-1": "Editie 1", "editie-2": "Editie 2",
                   "editie-3": "Editie 3", "editie-4": "Editie 4", "editie-5": "Editie 5",
                   "editie-6": "Editie 6", "dossiers": "Dossiers", "onderzoek": "Onderzoek"}},
    "de": {"terug": "Zurück zu", "voor": "Startseite", "verk": "Erkunden", "taal": "Sprache",
           "sec": {"wat-opkomt": "Was aufkommt", "verkennen.html": "Erkunden",
                   "editie-0": "Ausgabe Europa", "editie-1": "Ausgabe 1", "editie-2": "Ausgabe 2",
                   "editie-3": "Ausgabe 3", "editie-4": "Ausgabe 4", "editie-5": "Ausgabe 5",
                   "editie-6": "Ausgabe 6", "dossiers": "Dossiers", "onderzoek": "Forschung"}},
    "en": {"terug": "Back to", "voor": "Front page", "verk": "Explore", "taal": "Language",
           "sec": {"wat-opkomt": "What surfaces", "verkennen.html": "Explore",
                   "editie-0": "Edition Europe", "editie-1": "Edition 1", "editie-2": "Edition 2",
                   "editie-3": "Edition 3", "editie-4": "Edition 4", "editie-5": "Edition 5",
                   "editie-6": "Edition 6", "dossiers": "Dossiers", "onderzoek": "Research"}},
    "ru": {"terug": "Назад в", "voor": "Главная", "verk": "Обзор", "taal": "Язык",
           "sec": {"wat-opkomt": "Что всплывает", "verkennen.html": "Обзор",
                   "editie-0": "Выпуск Европа", "editie-1": "Выпуск 1", "editie-2": "Выпуск 2",
                   "editie-3": "Выпуск 3", "editie-4": "Выпуск 4", "editie-5": "Выпуск 5",
                   "editie-6": "Выпуск 6", "dossiers": "Досье", "onderzoek": "Исследование"}},
    "es": {"terug": "Volver a", "voor": "Portada", "verk": "Explorar", "taal": "Idioma",
           "sec": {"wat-opkomt": "Lo que emerge", "verkennen.html": "Explorar",
                   "editie-0": "Edición Europa"}},
    "fr": {"terug": "Retour à", "voor": "Accueil", "verk": "Explorer", "taal": "Langue",
           "sec": {"wat-opkomt": "Ce qui émerge", "verkennen.html": "Explorer",
                   "editie-0": "Édition Europe"}},
    "it": {"terug": "Torna a", "voor": "Home", "verk": "Esplora", "taal": "Lingua",
           "sec": {"wat-opkomt": "Ciò che emerge", "verkennen.html": "Esplora",
                   "editie-0": "Edizione Europa"}},
    "pt": {"terug": "Voltar a", "voor": "Início", "verk": "Explorar", "taal": "Idioma",
           "sec": {"wat-opkomt": "O que emerge", "verkennen.html": "Explorar",
                   "editie-0": "Edição Europa"}},
}

# Markers
LANG_BLOCK_START = "<!-- LANGSWITCH_BEGIN -->"
LANG_BLOCK_END   = "<!-- LANGSWITCH_END -->"
BOTTOM_START     = "<!-- NAV_BOTTOM_BEGIN -->"
BOTTOM_END       = "<!-- NAV_BOTTOM_END -->"

# Patroon voor bestaande nav__lang div
NAV_LANG_RE = re.compile(
    r'<div class="nav__lang">.*?</div>',
    re.DOTALL,
)
# Idempotent: bestaande LANGSWITCH block
LANG_BLOCK_RE = re.compile(
    re.escape(LANG_BLOCK_START) + r'.*?' + re.escape(LANG_BLOCK_END),
    re.DOTALL,
)
BOTTOM_BLOCK_RE = re.compile(
    re.escape(BOTTOM_START) + r'.*?' + re.escape(BOTTOM_END),
    re.DOTALL,
)
WO_TERUG_RE = re.compile(r'<div class="wo-artikel__terug">.*?</div>', re.DOTALL)


def detect_lang_logical(rel: str) -> tuple[str | None, str | None]:
    """('nl/wat-opkomt/foo.html') -> ('nl', 'wat-opkomt/foo.html')."""
    parts = rel.split("/")
    if not parts or parts[0] not in LANGS:
        return None, None
    lang = parts[0]
    rest = parts[1:]
    if not rest:
        return lang, "index.html"
    norm = DIR_NORM.get(lang, {})
    first = rest[0]
    if first in norm:
        canon_first = norm[first]
        if len(rest) == 1:
            return lang, canon_first
        return lang, canon_first + "/" + "/".join(rest[1:])
    # bestand op taal-root (over.html, delen.html, verkennen.html, archief.html, ...)
    return lang, "/".join(rest)


def depth_prefix(rel: str) -> str:
    """relpath -> aantal '../' om bij repo-root te komen."""
    return "../" * rel.count("/")


def build_langswitch_html(rel: str) -> str:
    """Render een popover-knop met alle 8 talen, met linkjes naar de equivalente pagina."""
    lang, logical = detect_lang_logical(rel)
    if lang is None:
        return ""
    prefix = depth_prefix(rel)
    cur_label = LANG_LABEL[lang]
    label = T[lang]["taal"]

    # Verzamel target-url per taal
    targets: dict[str, str] = {}
    if logical and logical in MAPPING:
        for lg, target_rel in MAPPING[logical].items():
            targets[lg] = prefix + target_rel
    else:
        # Pagina niet in mapping (bv. een speciale pagina). Fallback: taal-root.
        for lg in LANGS:
            targets[lg] = prefix + lg + "/"

    items = []
    for lg in LANGS:
        href = targets.get(lg, prefix + lg + "/")
        active = ' aria-current="true"' if lg == lang else ""
        items.append(
            f'        <li><a href="{href}" lang="{lg}" hreflang="{lg}"{active}>{LANG_LABEL[lg]}</a></li>'
        )
    items_html = "\n".join(items)

    return (
        f'{LANG_BLOCK_START}\n'
        f'<div class="nav__lang">\n'
        f'  <details class="lang-pop">\n'
        f'    <summary aria-label="{label}"><span aria-hidden="true">⌂</span> {label} · <span class="lang-pop__cur">{cur_label}</span></summary>\n'
        f'    <ul class="lang-pop__lijst">\n'
        f'{items_html}\n'
        f'    </ul>\n'
        f'  </details>\n'
        f'</div>\n'
        f'{LANG_BLOCK_END}'
    )


def section_for(logical: str) -> str | None:
    """Geef de top-level sectie (zonder slug)."""
    if not logical or "/" not in logical:
        return None
    return logical.split("/")[0]


def build_bottom_bar(rel: str) -> str:
    """Render de uniforme bottom-bar: terug-naar-sectie, voorpagina, verkennen."""
    lang, logical = detect_lang_logical(rel)
    if lang is None:
        return ""
    prefix = depth_prefix(rel)
    t = T[lang]
    section = section_for(logical or "")
    parts = []
    if section and section in t.get("sec", {}):
        # Vind sectie-pad in deze taal
        section_target_in_lang = None
        if (section + "/index.html") in MAPPING:
            section_target_in_lang = MAPPING[section + "/index.html"].get(lang)
        if not section_target_in_lang:
            # Bouw direct
            from_logical = {
                "nl": {"wat-opkomt": "wat-opkomt", "editie-0": "editie-0", "editie-1": "editie-1",
                       "editie-2": "editie-2", "editie-3": "editie-3", "editie-4": "editie-4",
                       "editie-5": "editie-5", "editie-6": "editie-6", "dossiers": "dossiers",
                       "onderzoek": "onderzoek"},
                "de": {"wat-opkomt": "was-aufkommt", "editie-0": "ausgabe-0", "editie-1": "ausgabe-1",
                       "editie-2": "ausgabe-2", "editie-3": "ausgabe-3", "editie-4": "ausgabe-4",
                       "editie-5": "ausgabe-5", "editie-6": "ausgabe-6", "dossiers": "dossiers",
                       "onderzoek": "forschung"},
                "en": {"wat-opkomt": "what-surfaces", "editie-0": "edition-0", "editie-1": "edition-1",
                       "editie-2": "edition-2", "editie-3": "edition-3", "editie-4": "edition-4",
                       "editie-5": "edition-5", "editie-6": "edition-6", "dossiers": "dossiers",
                       "onderzoek": "research"},
                "ru": {"wat-opkomt": "chto-vsplyvaet", "editie-0": "vypusk-0", "editie-1": "vypusk-1",
                       "editie-2": "vypusk-2", "editie-3": "vypusk-3", "editie-4": "vypusk-4",
                       "editie-5": "vypusk-5", "editie-6": "vypusk-6", "dossiers": "dossiers",
                       "onderzoek": "issledovanie"},
                "es": {"wat-opkomt": "lo-que-emerge", "editie-0": "edicion-0"},
                "fr": {"wat-opkomt": "ce-qui-emerge", "editie-0": "edition-0"},
                "it": {"wat-opkomt": "cio-che-emerge", "editie-0": "edizione-0"},
                "pt": {"wat-opkomt": "o-que-emerge", "editie-0": "edicao-0"},
            }
            local_sec = from_logical.get(lang, {}).get(section)
            if local_sec and (ROOT / lang / local_sec).exists():
                section_target_in_lang = f"{lang}/{local_sec}/"
            else:
                # Fallback naar taal-root
                section_target_in_lang = f"{lang}/"
        sec_href = prefix + section_target_in_lang
        sec_label = t["sec"][section]
        parts.append(f'<a href="{sec_href}" class="navbar__terug">← {t["terug"]} {sec_label}</a>')
    # Voorpagina
    parts.append(f'<a href="{prefix}{lang}/" class="navbar__home">⌂ {t["voor"]}</a>')
    # Verkennen
    parts.append(f'<a href="{prefix}{lang}/verkennen.html" class="navbar__verk">↻ {t["verk"]}</a>')

    inner = "\n  ".join(parts)
    return (
        f'{BOTTOM_START}\n'
        f'<nav class="navbar-bottom" aria-label="{t["voor"]}">\n'
        f'  {inner}\n'
        f'</nav>\n'
        f'{BOTTOM_END}'
    )


# Pagina's die GEEN bottom-bar krijgen
SKIP_BOTTOMBAR = {
    "index.html",                       # root splash
    "nl/verkennen-embed.html", "de/verkennen-embed.html", "en/verkennen-embed.html",
    "ru/verkennen-embed.html", "es/verkennen-embed.html", "fr/verkennen-embed.html",
    "it/verkennen-embed.html", "pt/verkennen-embed.html",
}


def process_file(path: Path) -> tuple[bool, bool]:
    """Return (langswitch_changed, bottombar_changed)."""
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return False, False  # splash heeft eigen taalkeuze al
    lang, _ = detect_lang_logical(rel)
    if lang is None:
        return False, False

    txt = path.read_text(encoding="utf-8")
    orig = txt
    ls_changed = False
    bb_changed = False

    # 1) Taal-switcher in nav__lang
    new_lang_block = build_langswitch_html(rel)
    if new_lang_block:
        if LANG_BLOCK_START in txt:
            new_txt = LANG_BLOCK_RE.sub(new_lang_block, txt, count=1)
        elif NAV_LANG_RE.search(txt):
            new_txt = NAV_LANG_RE.sub(new_lang_block, txt, count=1)
        else:
            # geen plek gevonden — niet forceren
            new_txt = txt
        if new_txt != txt:
            ls_changed = True
            txt = new_txt

    # 2) Bottom-bar
    if rel not in SKIP_BOTTOMBAR:
        new_bottom = build_bottom_bar(rel)
        if new_bottom:
            if BOTTOM_START in txt:
                new_txt = BOTTOM_BLOCK_RE.sub(new_bottom, txt, count=1)
            else:
                # Verwijder de oude wo-artikel__terug div als die bestaat, vervang door bottom-bar
                # of voeg toe vóór </main>, of vóór <footer>, of vóór </body>
                if WO_TERUG_RE.search(txt):
                    new_txt = WO_TERUG_RE.sub(new_bottom, txt, count=1)
                elif "</main>" in txt:
                    new_txt = txt.replace("</main>", new_bottom + "\n</main>", 1)
                elif re.search(r'<footer[^>]*>', txt):
                    new_txt = re.sub(r'(<footer[^>]*>)', new_bottom + r'\n\1', txt, count=1)
                else:
                    new_txt = txt.replace("</body>", new_bottom + "\n</body>", 1)
            if new_txt != txt:
                bb_changed = True
                txt = new_txt

    if txt != orig:
        path.write_text(txt, encoding="utf-8")
    return ls_changed, bb_changed


def main() -> None:
    ls_count = 0
    bb_count = 0
    total = 0
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("node_modules/") or rel.startswith("scripts/"):
            continue
        total += 1
        ls_chg, bb_chg = process_file(path)
        if ls_chg: ls_count += 1
        if bb_chg: bb_count += 1
    print(f"Totaal HTML's bezocht: {total}")
    print(f"Taal-switcher bijgewerkt: {ls_count}")
    print(f"Bottom-bar bijgewerkt:    {bb_count}")


if __name__ == "__main__":
    main()
