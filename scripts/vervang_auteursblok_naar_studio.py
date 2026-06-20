#!/usr/bin/env python3
"""Vervang het oude 'gravure' auteursblok overal door het nieuwe 'studio' auteursblok.

- Behoudt structuur (img + 2 alinea's), kapt 'Malta'-regel en 'Meer over de schrijver'-link weg.
- Vervangt jvm_gravure_klein.jpg / jvm_gravure.jpg door jvm_studio.jpg.
- Vertaalt biografietekst per taal.
- Idempotent: pagina's die al 'jvm_studio.jpg' tonen worden overgeslagen.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Per taal: (naam, biografietekst)
BIO = {
    "nl": ("Jacobus van Merksteijn",
           "Hoofdredacteur van Het Open Vizier. Ondernemer, ontwikkelaar van industriële en governance-innovaties (Carbon-Alert Ltd, TerraClean Ltd, GuardSkin Ltd). Schrijft over economische, ecologische en politieke systeemvraagstukken vanuit ervaring met de Brusselse en Haagse besluitvormingsmachine."),
    "de": ("Jacobus van Merksteijn",
           "Chefredakteur von Het Open Vizier. Unternehmer, Entwickler industrieller und governance-bezogener Innovationen (Carbon-Alert Ltd, TerraClean Ltd, GuardSkin Ltd). Schreibt über wirtschaftliche, ökologische und politische Systemfragen — aus eigener Erfahrung mit der Brüsseler und Haager Entscheidungsmaschinerie."),
    "en": ("Jacobus van Merksteijn",
           "Editor-in-chief of Het Open Vizier. Entrepreneur, developer of industrial and governance innovations (Carbon-Alert Ltd, TerraClean Ltd, GuardSkin Ltd). Writes about economic, ecological and political system questions from first-hand experience with the Brussels and The Hague decision-making machinery."),
    "ru": ("Якобус ван Мерстеин",
           "Главный редактор Het Open Vizier. Предприниматель, разработчик промышленных и управленческих инноваций (Carbon-Alert Ltd, TerraClean Ltd, GuardSkin Ltd). Пишет об экономических, экологических и политических системных вопросах, опираясь на опыт работы с брюссельским и гаагским аппаратами принятия решений."),
    "es": ("Jacobus van Merksteijn",
           "Director de Het Open Vizier. Empresario, desarrollador de innovaciones industriales y de gobernanza (Carbon-Alert Ltd, TerraClean Ltd, GuardSkin Ltd). Escribe sobre cuestiones sistémicas económicas, ecológicas y políticas desde la experiencia con la maquinaria de decisión de Bruselas y La Haya."),
    "fr": ("Jacobus van Merksteijn",
           "Rédacteur en chef de Het Open Vizier. Entrepreneur, développeur d'innovations industrielles et de gouvernance (Carbon-Alert Ltd, TerraClean Ltd, GuardSkin Ltd). Écrit sur les questions systémiques économiques, écologiques et politiques à partir d'une expérience directe des machineries de décision de Bruxelles et de La Haye."),
    "it": ("Jacobus van Merksteijn",
           "Direttore di Het Open Vizier. Imprenditore, sviluppatore di innovazioni industriali e di governance (Carbon-Alert Ltd, TerraClean Ltd, GuardSkin Ltd). Scrive di questioni sistemiche economiche, ecologiche e politiche dall'esperienza diretta con le macchine decisionali di Bruxelles e dell'Aja."),
    "pt": ("Jacobus van Merksteijn",
           "Editor-chefe do Het Open Vizier. Empresário, desenvolvedor de inovações industriais e de governação (Carbon-Alert Ltd, TerraClean Ltd, GuardSkin Ltd). Escreve sobre questões sistémicas económicas, ecológicas e políticas a partir da experiência directa com as máquinas de decisão de Bruxelas e de Haia."),
}

# Map dir-prefix -> taalcode
LANG_DIRS = {
    "nl/": "nl", "de/": "de", "en/": "en", "ru/": "ru",
    "es/": "es", "fr/": "fr", "it/": "it", "pt/": "pt",
}

# Regex die het hele oude auteursblok matcht. Vangt:
#   - <div class="auteursblok"> of <aside class="auteursblok">
#   - img direct of binnen <a href="...">
#   - jvm_gravure*.jpg OF jvm_studio.jpg (laatste = al gemigreerd img, oude markup eromheen)
#   - <div> of <div class="auteursblok__tekst">
#   - 3 alinea's (naam/plaats/intro) + 1 link
BLOCK_RE = re.compile(
    r'<(?P<tag>div|aside) class="auteursblok">\s*'
    r'<div class="auteursblok__foto">\s*'
    r'(?:<a [^>]*>\s*)?'
    r'<img src="[^"]*jvm_(?:gravure|studio)[^"]*\.jpg"[^>]*>\s*'
    r'(?:</a>\s*)?'
    r'</div>\s*'
    r'<div(?:\s+class="auteursblok__tekst")?>\s*'
    r'<p class="auteursblok__naam">([^<]+)</p>\s*'
    r'<p class="auteursblok__plaats">[^<]*</p>\s*'
    r'<p class="auteursblok__intro">[^<]*</p>\s*'
    r'<a href="[^"]*" class="auteursblok__link">[^<]*</a>\s*'
    r'</div>\s*'
    r'</(?P=tag)>',
    re.DOTALL,
)

def detect_lang(path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    for prefix, lang in LANG_DIRS.items():
        if rel.startswith(prefix):
            return lang
    return None

def depth_prefix(path: Path) -> str:
    """Bereken hoeveel '../' nodig zijn om bij repo-root te komen."""
    rel = path.relative_to(ROOT).as_posix()
    # 'nl/wat-opkomt/foo.html' -> 2 levels => '../../'
    depth = rel.count("/")
    return "../" * depth

def build_new_block(lang: str, prefix: str, tag: str = "div") -> str:
    naam, bio = BIO[lang]
    return (
        f'<{tag} class="auteursblok">\n'
        f'  <div class="auteursblok__foto"><img src="{prefix}assets/auteur/jvm_studio.jpg" alt="{naam}" loading="lazy"></div>\n'
        f'  <div class="auteursblok__tekst">\n'
        f'    <p class="auteur-naam">{naam}</p>\n'
        f'    <p>{bio}</p>\n'
        f'  </div>\n'
        f'</{tag}>'
    )

def process_file(path: Path) -> bool:
    lang = detect_lang(path)
    if lang is None:
        return False
    txt = path.read_text(encoding="utf-8")
    prefix = depth_prefix(path)
    # 1) Vervang oude blok-markup; behoud div/aside tag-keuze
    def repl(m: re.Match) -> str:
        return build_new_block(lang, prefix, tag=m.group("tag"))
    new_txt, _ = BLOCK_RE.subn(repl, txt)
    # 2) Losse img-tags die nog naar gravure wijzen (og:image, over-hero)
    new_txt = re.sub(r'jvm_gravure_klein\.jpg', 'jvm_studio.jpg', new_txt)
    new_txt = re.sub(r'jvm_gravure\.jpg', 'jvm_studio.jpg', new_txt)
    if new_txt != txt:
        path.write_text(new_txt, encoding="utf-8")
        return True
    return False

def main() -> None:
    geraakt = 0
    blok_vervangen = 0
    for path in ROOT.rglob("*.html"):
        if "/node_modules/" in path.as_posix():
            continue
        txt_before = path.read_text(encoding="utf-8") if path.exists() else ""
        had_block = bool(BLOCK_RE.search(txt_before)) if "jvm_gravure" in txt_before else False
        if process_file(path):
            geraakt += 1
            if had_block:
                blok_vervangen += 1
    print(f"Bestanden aangepast: {geraakt}")
    print(f"Auteursblokken vervangen (regex-match): {blok_vervangen}")

if __name__ == "__main__":
    main()
