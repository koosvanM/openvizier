#!/usr/bin/env python3
"""
Voeg een 3-staps-transitie toe aan de Verkenner:
  1. Tegels fade-out (250ms)
  2. Terug-knop verschijnt (150ms)
  3. Nieuwe tegels fade-in via .entering

Aanpassingen:
A. CSS: .stage.uit-fade { opacity:0 } met transition op .stage
        en op .tile bij class .entering
B. JS: onClick → wrap met fade-uit-eerst voordat hash wordt aangepast

Werkt door:
- Bij elke onClick die naar nieuwe laag gaat, stage krijgt class 'fading'
- Na 280ms wordt hash aangepast (hash → render() → clear + nieuwe tegels)
- Render() haalt class 'fading' weg zodat stage weer zichtbaar wordt
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
TARGETS = [
    "nl/verkennen.html", "de/verkennen.html", "en/verkennen.html", "ru/verkennen.html",
    "es/verkennen.html", "fr/verkennen.html", "it/verkennen.html", "pt/verkennen.html",
    "nl/verkennen-embed.html", "de/verkennen-embed.html",
    "en/verkennen-embed.html", "ru/verkennen-embed.html",
]

# CSS-injectie: voeg toe aan </style>
CSS_INJECT = """
  /* 3-staps-transitie: tegels uit-faden bij navigatie */
  .stage { transition: opacity 0.25s ease; }
  .stage.fading { opacity: 0; }
  .stage.fading .tile { pointer-events: none; }
  /* Home-knop krijgt een fade-in als hij verschijnt */
  #home { transition: opacity 0.3s ease 0.15s, transform 0.3s ease; opacity: 0; transform: translateY(-4px); }
  #home.show { opacity: 1; transform: translateY(0); }
  /* Topbar-title soepel laten verschijnen */
  #topbar-title { transition: opacity 0.3s ease 0.15s; opacity: 0.85; }
"""

# JS-injectie: vervang de huidige hash-aanpassing in onClick
# Origineel patroon (drie plekken in onClick):
#   location.hash = nieuwHash;            (synthetische knop)
#   location.hash = "#code=" + node.code; (kinderen-navigatie)
#
# Beide krijgen een fade-wrapper.

# Vervang in JS-blok
JS_PATTERN_1 = re.compile(
    r'(if \(node\._synthVervolg \|\| node\._synthVorige\)\{\s*const nieuwHash = "#code=" \+ node\.code \+ "&p=" \+ node\._doelPagina;\s*)location\.hash = nieuwHash;',
    re.MULTILINE,
)
JS_REPLACE_1 = r'''\1const _stage = document.getElementById('stage');
    if (_stage) _stage.classList.add('fading');
    setTimeout(() => { location.hash = nieuwHash; }, 280);'''

JS_PATTERN_2 = re.compile(
    r'(if \(heeftLevendeKinderen\)\{\s*path\.push\(node\.code\);\s*)location\.hash = "#code=" \+ node\.code;',
    re.MULTILINE,
)
JS_REPLACE_2 = r'''\1const _stage2 = document.getElementById('stage');
    if (_stage2) _stage2.classList.add('fading');
    setTimeout(() => { location.hash = "#code=" + node.code; }, 280);'''

# Voor goBack/home-klik ook fade
JS_PATTERN_3 = re.compile(
    r'(document\.getElementById\(\'home\'\)\.addEventListener\(\'click\', \(e\)=>\{\s*e\.stopPropagation\(\);\s*)path\.length = 0;\s*path\.push\(WORTEL_CODE\);\s*location\.hash = "";\s*render\(\);\s*updateHome\(\);',
    re.MULTILINE,
)
JS_REPLACE_3 = r'''\1const _stageH = document.getElementById('stage');
  if (_stageH) _stageH.classList.add('fading');
  setTimeout(() => {
    path.length = 0;
    path.push(WORTEL_CODE);
    location.hash = "";
    render();
    updateHome();
  }, 280);'''

# Render-functie: na clearen van fading-class
# Zoek "function render(){" en voeg na de eerste regel "const stage = document.getElementById('stage'); clear(stage);"
# een stage.classList.remove('fading'); toe
RENDER_PATTERN = re.compile(
    r"(function render\(\)\{\s*const stage = document\.getElementById\('stage'\);\s*clear\(stage\);)",
)
RENDER_REPLACE = r"\1\n  stage.classList.remove('fading');"

# Center-overlay-klik (terug naar vorige laag) ook met fade
CENTER_PATTERN = re.compile(
    r"document\.getElementById\('center'\)\.addEventListener\('click',\(\)=>\{\s*if \(path\.length > 1\) goBack\(\);\s*\}\);",
)
CENTER_REPLACE = """document.getElementById('center').addEventListener('click',()=>{
  if (path.length > 1) {
    const _s = document.getElementById('stage');
    if (_s) _s.classList.add('fading');
    setTimeout(() => goBack(), 280);
  }
});"""

veranderd = []
voor_status = {}
for rel in TARGETS:
    p = REPO / rel
    if not p.exists():
        continue
    content = p.read_text(encoding="utf-8")
    orig = content

    # Injecteer CSS vóór </style>
    if ".stage.fading" not in content:
        content = content.replace("</style>", CSS_INJECT + "\n</style>", 1)

    # JS-vervangingen
    content, n1 = JS_PATTERN_1.subn(JS_REPLACE_1, content, count=1)
    content, n2 = JS_PATTERN_2.subn(JS_REPLACE_2, content, count=1)
    content, n3 = JS_PATTERN_3.subn(JS_REPLACE_3, content, count=1)
    content, n4 = RENDER_PATTERN.subn(RENDER_REPLACE, content, count=1)
    content, n5 = CENTER_PATTERN.subn(CENTER_REPLACE, content, count=1)

    voor_status[rel] = (n1, n2, n3, n4, n5)

    if content != orig:
        p.write_text(content, encoding="utf-8")
        veranderd.append(rel)

print(f"Bijgewerkt: {len(veranderd)}/{len(TARGETS)}")
for rel in TARGETS:
    s = voor_status.get(rel, "skip")
    print(f"  {rel}: replacements={s}")
