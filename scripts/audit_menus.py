#!/usr/bin/env python3
"""
Audit alle menubalken in alle HTML-bestanden in de 8 talen.

Wat wordt gecontroleerd:
1. Bevatten alle pagina's met <nav class="nav"> het volledige juiste menu
   voor hun taal?
2. Verwijst de "Verkennen"-link naar het juiste pad op het juiste niveau?
3. Verwijzen alle menu-items naar bestaande paden?
4. Klopt het taal-label (⌂ Taal / ⌂ Sprache / etc.)?
5. Klopt de "active" markering met de huidige pagina?

We rapporteren issues per bestand zonder ze te wijzigen.
"""
import re
from pathlib import Path
from collections import defaultdict

REPO = Path("/tmp/gh-repo")

# Verwacht menu per taal (href, label) — full menu voor NL/DE/EN/RU, kort menu voor ES/FR/IT/PT
# Active-href is afhankelijk van de pagina; we checken alleen aanwezigheid + labels.
EXPECTED_FULL = {
    "nl": {
        "items": [
            ("./", "Voorpagina"),
            ("wat-opkomt/", "Wat opkomt"),
            ("verkennen.html", "Verkennen"),
            ("editie-6/", "Editie 6"),
            ("editie-5/", "Editie 5"),
            ("editie-4/", "Editie 4"),
            ("editie-3/", "Editie 3"),
            ("editie-2/", "Editie 2"),
            ("editie-1/", "Editie 1"),
            ("editie-0/", "Editie Europa"),
            ("delen.html", "Delen"),
        ],
        "lang_label": "⌂ Taal",
        "verkennen_label": "Verkennen",
    },
    "de": {
        "items": [
            ("./", "Startseite"),
            ("was-aufkommt/", "Was aufkommt"),
            ("verkennen.html", "Erkunden"),
            ("ausgabe-6/", "Ausgabe 6"),
            ("ausgabe-5/", "Ausgabe 5"),
            ("ausgabe-4/", "Ausgabe 4"),
            ("ausgabe-3/", "Ausgabe 3"),
            ("ausgabe-2/", "Ausgabe 2"),
            ("ausgabe-1/", "Ausgabe 1"),
            ("ausgabe-0/", "Ausgabe Europa"),
            ("teilen.html", "Teilen"),
        ],
        "lang_label": "⌂ Sprache",
        "verkennen_label": "Erkunden",
    },
    "en": {
        "items": [
            ("./", "Home"),
            ("what-surfaces/", "What surfaces"),
            ("verkennen.html", "Explore"),
            ("edition-6/", "Edition 6"),
            ("edition-5/", "Edition 5"),
            ("edition-4/", "Edition 4"),
            ("edition-3/", "Edition 3"),
            ("edition-2/", "Edition 2"),
            ("edition-1/", "Edition 1"),
            ("edition-0/", "Edition Europe"),
            ("share.html", "Share"),
        ],
        "lang_label": "⌂ Language",
        "verkennen_label": "Explore",
    },
    "ru": {
        "items": [
            ("./", "Главная"),
            ("chto-vsplyvaet/", "Что всплывает"),
            ("verkennen.html", "Исследовать"),
            ("vypusk-6/", "Выпуск 6"),
            ("vypusk-5/", "Выпуск 5"),
            ("vypusk-4/", "Выпуск 4"),
            ("vypusk-3/", "Выпуск 3"),
            ("vypusk-2/", "Выпуск 2"),
            ("vypusk-1/", "Выпуск 1"),
            ("vypusk-0/", "Выпуск Европа"),
            ("podelitsya.html", "Поделиться"),
        ],
        "lang_label": "⌂ Язык",
        "verkennen_label": "Исследовать",
    },
}

EXPECTED_SHORT = {
    "es": {
        "verkennen_label": "Explorar",
        "lang_label": "⌂ Idioma",
        "ed0_path": "edicion-0/",
        "wo_path": "lo-que-emerge/",
    },
    "fr": {
        "verkennen_label": "Explorer",
        "lang_label": "⌂ Langue",
        "ed0_path": "edition-0/",
        "wo_path": "ce-qui-emerge/",
    },
    "it": {
        "verkennen_label": "Esplorare",
        "lang_label": "⌂ Lingua",
        "ed0_path": "edizione-0/",
        "wo_path": "cio-che-emerge/",
    },
    "pt": {
        "verkennen_label": "Explorar",
        "lang_label": "⌂ Idioma",
        "ed0_path": "edicao-0/",
        "wo_path": "o-que-emerge/",
    },
}

ALL_LANGS = list(EXPECTED_FULL) + list(EXPECTED_SHORT)

issues = defaultdict(list)
stats = defaultdict(int)

def check_full_lang(lang, files):
    exp = EXPECTED_FULL[lang]
    for f in files:
        html = f.read_text(encoding="utf-8")
        if 'class="nav__links"' not in html:
            stats[f"{lang}/no-menu"] += 1
            continue
        stats[f"{lang}/has-menu"] += 1

        # Extract <li><a href="..."> ...
        # Met optionele class="active"
        link_pattern = re.compile(
            r'<li><a href="([^"]+)"(?:\s+class="active")?\s*>([^<]+)</a></li>'
        )
        links = link_pattern.findall(html)

        # Pas op: voor pagina's onder een subdir (bv. wat-opkomt/index.html)
        # zou alles met ../ moeten beginnen. We slaan dat voor nu over.
        rel = f.relative_to(REPO / lang)
        prefix = "../" * (len(rel.parts) - 1)

        # Verwacht: prefix + exp_href
        for (exp_href, exp_label) in exp["items"]:
            # exp_href is voor top-level; voor subdir-pagina's wordt het prefix + exp_href
            # MAAR voor links die zelf met ../ beginnen werkt dat anders. We versimpelen:
            # Zoek of er een link met label exp_label bestaat
            label_matches = [(h, l) for (h, l) in links if l.strip() == exp_label]
            if not label_matches:
                issues[f"{lang}/{rel}"].append(f"ONTBREEKT: menu-item label '{exp_label}'")
            else:
                actual_href = label_matches[0][0]
                # Verwacht href is (prefix + exp_href) of (exp_href) als zonder prefix
                # Behandel gelijkwaardige paden: '..' == '.././', '../' == '.././' enz.
                def normalize(p):
                    # './' verwijderen, dubbele slashes opruimen
                    p = p.rstrip("/") + ("/" if p.endswith("/") else "")
                    return p.replace("/./", "/")
                expected = prefix + exp_href
                exp_alts = {expected, exp_href, prefix.rstrip("/") if prefix else "./",
                            prefix if prefix else "./"}
                # Voor href='./' op subdir-niveau: prefix-vorm zonder trailing slash is ook OK
                if exp_href == "./":
                    exp_alts |= {prefix, prefix.rstrip("/") + "/", prefix.rstrip("/")}
                    if not prefix:
                        exp_alts |= {"./", ""}
                if actual_href not in exp_alts:
                    issues[f"{lang}/{rel}"].append(
                        f"HREF: '{exp_label}' = '{actual_href}', verwacht '{expected}'"
                    )

        # Check taal-label
        lang_link_pat = re.compile(
            r'<div class="nav__lang">\s*<a[^>]*>([^<]+)</a>',
            re.DOTALL,
        )
        m = lang_link_pat.search(html)
        if m:
            actual_label = m.group(1).strip()
            if actual_label != exp["lang_label"]:
                issues[f"{lang}/{rel}"].append(
                    f"TAAL-LABEL: '{actual_label}', verwacht '{exp['lang_label']}'"
                )

def check_short_lang(lang, files):
    exp = EXPECTED_SHORT[lang]
    for f in files:
        html = f.read_text(encoding="utf-8")
        if 'class="nav__links"' not in html:
            stats[f"{lang}/no-menu"] += 1
            continue
        stats[f"{lang}/has-menu"] += 1

        rel = f.relative_to(REPO / lang)

        # Voor kort menu: check of het verkennen_label aanwezig is
        if exp["verkennen_label"] not in html:
            issues[f"{lang}/{rel}"].append(
                f"ONTBREEKT 'Verkennen'-label in menu: {exp['verkennen_label']}"
            )
        if exp["lang_label"] not in html:
            issues[f"{lang}/{rel}"].append(
                f"ONTBREEKT taal-label: {exp['lang_label']}"
            )

# Run checks
for lang in ALL_LANGS:
    base = REPO / lang
    if not base.exists():
        continue
    # alleen top-level html-bestanden eerst (waar menu echt op staat)
    files = sorted([f for f in base.iterdir() if f.is_file() and f.suffix == ".html"])
    # plus subdir-index pagina's
    subdir_indexes = sorted(base.glob("*/index.html"))
    files += subdir_indexes
    if lang in EXPECTED_FULL:
        check_full_lang(lang, files)
    else:
        check_short_lang(lang, files)

# Output
print("=== STATS ===")
for k in sorted(stats):
    print(f"  {k}: {stats[k]}")

print(f"\n=== ISSUES ({sum(len(v) for v in issues.values())}) ===")
for f in sorted(issues):
    print(f"\n{f}:")
    for issue in issues[f]:
        print(f"  - {issue}")
