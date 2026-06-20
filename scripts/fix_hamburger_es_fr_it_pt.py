#!/usr/bin/env python3
"""
Fix het hamburger-menu op ES/FR/IT/PT voorpagina's.

Probleem: inline .nav__links { display: flex } in <style> overschrijft de
globale @media-rule. Oplossing: voeg een mediaquery toe direct ná de
inline .nav__links regels.
"""
import re
from pathlib import Path

REPO = Path("/tmp/gh-repo")
TARGETS = ["es/index.html", "fr/index.html", "it/index.html", "pt/index.html"]

# CSS-injectie: mediaquery die op iPhone het inline-menu verbergt
# en de hamburger-CSS dezelfde namespace geeft
MEDIAQUERY_CSS = """
  @media (max-width: 720px) {
    .nav__inner { padding: 0.6rem 1rem; flex-wrap: nowrap; justify-content: space-between; gap: 0.6rem; }
    .nav__links {
      display: none;
      position: absolute; top: 100%; left: 0; right: 0;
      flex-direction: column;
      background: #fdfbf7;
      border-bottom: 1px solid #d4d1ca;
      border-top: 1px solid #d4d1ca;
      padding: 0.5rem 0; margin: 0; gap: 0;
      box-shadow: 0 8px 20px rgba(0,0,0,0.10);
      z-index: 100;
    }
    .nav__links li { width: 100%; }
    .nav__links a {
      display: block;
      padding: 0.85rem 1.25rem;
      font-size: 1rem;
      border-bottom: 1px solid rgba(212,209,202,0.4);
    }
    .nav__links li:last-child a { border-bottom: 0; }
    .nav--open .nav__links { display: flex; }
    .nav__burger {
      display: inline-flex !important;
      background: transparent;
      border: 1px solid #d4d1ca;
      border-radius: 6px;
      width: 44px; height: 38px;
      cursor: pointer;
      padding: 0;
      align-items: center; justify-content: center;
      color: #1c5760;
    }
    .nav__burger-icon,
    .nav__burger-icon::before,
    .nav__burger-icon::after {
      content: ""; display: block; width: 20px; height: 2px;
      background: currentColor; position: relative;
      transition: transform 0.2s ease, opacity 0.2s ease;
    }
    .nav__burger-icon::before { position: absolute; top: -7px; left: 0; }
    .nav__burger-icon::after { position: absolute; top: 7px; left: 0; }
    .nav--open .nav__burger-icon { background: transparent; }
    .nav--open .nav__burger-icon::before { transform: translateY(7px) rotate(45deg); }
    .nav--open .nav__burger-icon::after { transform: translateY(-7px) rotate(-45deg); }
    .nav__lang a { font-size: 0.75rem; padding: 0.25rem 0.5rem; }
  }
  /* Hamburger op desktop verbergen */
  .nav__burger { display: none; }
"""

MARKER = "/* hamburger-mediaquery v1 */"

veranderd = []
for rel in TARGETS:
    path = REPO / rel
    if not path.exists():
        continue
    content = path.read_text(encoding="utf-8")
    if MARKER in content:
        continue
    # Voeg toe vlak vóór </style>
    if "</style>" not in content:
        print(f"  geen </style> in {rel}")
        continue
    new_content = content.replace("</style>", MARKER + MEDIAQUERY_CSS + "\n</style>", 1)
    path.write_text(new_content, encoding="utf-8")
    veranderd.append(rel)

print(f"Bijgewerkt: {len(veranderd)}")
for v in veranderd:
    print(f"  - {v}")
