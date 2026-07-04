#!/usr/bin/env python3
"""Regel 137.5 / Regel 138 verificatie: check dekking van partij_posities voor alle apps.

Faalt (exit 1) als een echte partij minder dan 80% dekking (146/183) heeft.
Gebruik: python3 tools/verifieer_partij_dekking.py

Wordt aangeroepen door pre-deploy hook (Regel 137)."""
import json, sys
from pathlib import Path

WORKSPACE = Path('/home/user/workspace')
APPS = [
    ('NL', WORKSPACE / 'nl_app/client/src/data/gevolgenkaart-persona.json'),
    ('DE', WORKSPACE / 'de_app/client/src/data/gevolgenkaart-persona.json'),
    ('MT', WORKSPACE / 'mt_app/client/src/data/gevolgenkaart-persona.json'),
    ('CH', WORKSPACE / 'ch_app/client/src/data/gevolgenkaart-persona.json'),
]

DREMPEL = 146  # 80% van 183

all_ok = True
for land, path in APPS:
    if not path.exists():
        print(f"[{land}] {path} bestaat niet, overgeslagen")
        continue
    p = json.load(open(path))
    echte = [k for k, v in p.get('partijen', {}).items() if not v.get('referentie')]
    posities = p.get('partij_posities', {})
    print(f"\n[{land}] {len(echte)} echte partijen:")
    land_ok = True
    for partij in echte:
        pos = posities.get(partij, {})
        nz = sum(1 for eid, v in pos.items()
                 if isinstance(v, dict) and (v.get('positie', 0) != 0 or v.get('intensiteit', 0) != 0))
        symbol = '✓' if nz >= DREMPEL else '✗ FAIL'
        print(f"  {symbol} {partij}: {nz}/183 posities gescoord")
        if nz < DREMPEL:
            land_ok = False
    if not land_ok:
        all_ok = False
        print(f"  [{land}] DEKKINGS-FOUT — deploy stopzetten en Regel 138 doorlopen")

if not all_ok:
    print("\n=== FAIL: minstens één land heeft ontoereikende partij-dekking ===")
    sys.exit(1)
print("\n=== OK: alle landen ≥ 80% dekking per echte partij ===")
