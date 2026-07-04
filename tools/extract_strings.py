#!/usr/bin/env python3
"""
Extractor voor zichtbare NL-strings uit de NL-app.
Output: JSON met {sleutel: {nl, bestand, regel, context}}.

Sleutel-conventie: bestandsnaam_zonder_ext.slug_van_eerste_woorden
Voorbeeld: chrome.stemgedrag_app_openvizier

Alleen echt zichtbare UI-tekst wordt geëxtraheerd:
- JSX-tekst tussen > en <
- Quoted strings in props: title=, placeholder=, label=, ariaLabel=, alt=
- Return statements van hulpfuncties die tekst leveren

We negeren:
- import/export paden
- className/id/data-testid/href/src waarden
- console.log, throw new Error (technische strings)
- comments
- shadcn/ui/ map (taal-neutrale gegenereerde code)
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from unicodedata import normalize

SRC = Path("/home/user/workspace/nl_app/client/src")

# Alleen app-eigen bestanden, niet shadcn/ui
KERN_BESTANDEN = [
    "components/Chrome.tsx",
    "components/MatrixSectie.tsx",
    "components/HistorischeTrend.tsx",
    "components/LevensloopGrafiek.tsx",
    "components/GezondheidsgrafiekNL.tsx",
    "components/PartijDetail.tsx",
    "components/MiniHero.tsx",
    "components/PersoonlijkeWeging.tsx",
    "components/Logo.tsx",
    "pages/Hoofdpagina.tsx",
    "pages/Methodologie.tsx",
    "pages/PersonaFlow.tsx",
    "pages/Sector.tsx",
    "pages/Kaart.tsx",
    "pages/not-found.tsx",
    "lib/personaEngine.ts",
    "lib/pdf.ts",
    "lib/levensloopEngine.ts",
]

# Regex-patronen voor zichtbare tekst
PATRONEN = [
    # JSX-tekst: >Nederlands hier<
    (re.compile(r">([^<>{}\n]+?)<"), "jsx"),
    # Prop-strings: title="...", placeholder="...", label="..."
    (re.compile(r'\b(?:title|placeholder|label|ariaLabel|aria-label|alt|description|subtitle|caption)=["\']([^"\'<>]+?)["\']'), "prop"),
    # Toast / alert titles in objects: title: "...", description: "..."
    (re.compile(r'\b(?:title|description|message|label|naam|beschrijving)\s*:\s*["\']([^"\'<>]+?)["\']'), "obj"),
]

# NL-markers om te detecteren of een string echt NL is
NL_MARKERS = re.compile(
    r'\b('
    r'de|het|een|is|zijn|wordt|worden|niet|geen|voor|met|van|naar|door|op|in|uit|aan|bij|om|te|dat|die|dit|deze|wat|hoe|waarom|waar|wanneer|wie|welk|welke|jouw|uw|jullie|onze|hun|ook|maar|of|als|dan|zo|nog|al|zeer|erg|heel|meer|minder|veel|weinig|elk|elke|geen|alleen|samen|zelf|eigen|nieuw|oud|goed|slecht|groot|klein'
    r')\b',
    re.IGNORECASE,
)

# Skip als een van deze patronen voorkomt
SKIP_INHOUD = re.compile(r'^(https?://|/|#|\{|\.|,|\s|-|\+|=|\d|[a-z_]+\(|null|true|false|undefined)$|^[A-Z_]+$', re.IGNORECASE)


def slugify(tekst: str, max_len: int = 30) -> str:
    """Maak stabiele sleutel-slug van tekst."""
    tekst = normalize("NFKD", tekst).encode("ascii", "ignore").decode("ascii")
    tekst = re.sub(r"[^a-zA-Z0-9\s]", "", tekst).lower()
    woorden = tekst.split()[:5]
    slug = "_".join(woorden)[:max_len].strip("_")
    return slug or "leeg"


def is_zichtbare_nl(tekst: str) -> bool:
    """Beslissing: is dit echt zichtbare NL-tekst?"""
    tekst = tekst.strip()
    if not tekst or len(tekst) < 3:
        return False
    if len(tekst) > 500:
        return False
    if SKIP_INHOUD.match(tekst):
        return False
    # Skip HTML entities alleen
    if re.fullmatch(r"(&[a-z]+;|\s)+", tekst):
        return False
    # Skip als het pure code lijkt (veel {}, JS-operatoren)
    if tekst.count("{") + tekst.count("}") > 2:
        return False
    if re.search(r'=>|===|!==|&&|\|\|', tekst):
        return False
    # Minstens 1 NL-marker of duidelijk NL-teken (accenten, hoofdletter-gevolgd-door-tekst)
    if NL_MARKERS.search(tekst):
        return True
    # Losse hoofdletter-woorden ("Volgende", "Terug") — accepteren als >4 letters
    if re.fullmatch(r"[A-ZÀ-ÿ][a-zà-ÿ]{3,}(\s[A-Za-zÀ-ÿ]+)*[.!?]?", tekst):
        return True
    return False


def extract_uit_bestand(pad: Path) -> list[dict]:
    """Retourneer lijst van {sleutel, nl, regel, context, patroon}."""
    if not pad.exists():
        return []
    inhoud = pad.read_text(encoding="utf-8")
    regels = inhoud.splitlines()
    modulenaam = pad.stem.lower().replace("-", "_")

    hits: list[dict] = []
    gezien: set[str] = set()

    for regelnr, regel in enumerate(regels, 1):
        # Skip pure comment-regels
        gestript = regel.strip()
        if gestript.startswith("//") or gestript.startswith("*") or gestript.startswith("/*"):
            continue
        # Skip import/export regels
        if re.match(r"^\s*(import|export\s+(default\s+)?(from|type|\*|\{))", gestript):
            continue

        for patroon, ptype in PATRONEN:
            for match in patroon.finditer(regel):
                tekst = match.group(1).strip()
                # Ontsnappen van HTML entities lezen we niet — laat ze staan zoals ze in de tsx-bron staan
                if not is_zichtbare_nl(tekst):
                    continue
                if tekst in gezien:
                    continue
                gezien.add(tekst)
                sleutel = f"{modulenaam}.{slugify(tekst)}"
                # Uniek maken bij collision
                basis_sleutel = sleutel
                teller = 2
                while any(h["sleutel"] == sleutel for h in hits):
                    sleutel = f"{basis_sleutel}_{teller}"
                    teller += 1
                hits.append({
                    "sleutel": sleutel,
                    "nl": tekst,
                    "bestand": str(pad.relative_to(SRC)),
                    "regel": regelnr,
                    "patroon": ptype,
                })
    return hits


def main() -> None:
    alle: list[dict] = []
    for rel in KERN_BESTANDEN:
        pad = SRC / rel
        hits = extract_uit_bestand(pad)
        alle.extend(hits)
        print(f"  {rel}: {len(hits)} strings", file=sys.stderr)
    print(f"\nTotaal: {len(alle)} unieke NL-strings", file=sys.stderr)
    print(json.dumps(alle, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
