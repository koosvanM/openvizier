#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pt_boilerplate_map import BOILERPLATE

def apply_boilerplate(text):
    for nl, pt in BOILERPLATE:
        text = text.replace(nl, pt)
    return text

if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    with open(src, encoding="utf-8") as f:
        text = f.read()
    text = apply_boilerplate(text)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {dst}")
