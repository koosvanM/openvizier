#!/usr/bin/env python3
"""Vier schuldlagen Nederland met traceerbare bronnen (mln euro).

Laag 1  EMU-schuld                                   Eurostat gov_10dd_edpt1 (S13, GD)
Laag 2  + overheidsgaranties (uitstaand)             Eurostat gov_cl_guar (S13, FGT)
Laag 3  + opgebouwde AOW-rechten (accrued-to-date)    Eurostat nasa_10_pens1 (S13PS, F63_LE) - 2015/2018/2021
Laag 4a - financiele activa overheid                 Eurostat nasa_10_f_bs (S13, ASS, F, NCO)
Laag 4b - latente belastingclaim pensioenvermogen    Eurostat nasa_10_f_bs (S129, ASS, F) x 35% (AANNAME)
Noemers: CBS 85865NED (bbp) en scripts/pbw_berekening.py (PBW).
Let op: garanties en AOW-rechten zijn volgens Eurostat voorwaardelijke verplichtingen, geen EMU-schuld.
"""
import json
import sys
import urllib.request

E = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
BELASTING = 0.35  # aanname, zie regelbestand


def es(ds, q):
    with urllib.request.urlopen(E + ds + "?" + q + "&format=JSON", timeout=120) as r:
        d = json.load(r)
    tl = d["dimension"]["time"]["category"]["index"]
    n = len(tl)
    return {int(t): d["value"].get(str(i)) for t, i in tl.items() if d["value"].get(str(i)) is not None}


def series():
    return dict(
        emu=es("gov_10dd_edpt1", "geo=NL&sector=S13&na_item=GD&unit=MIO_EUR"),
        gar=es("gov_cl_guar", "geo=NL&sector=S13&na_item=FGT&unit=MIO_NAC"),
        aow=es("nasa_10_pens1", "geo=NL&penscheme=S13PS&na_item=F63_LE&unit=MIO_EUR"),
        fa=es("nasa_10_f_bs", "geo=NL&sector=S13&finpos=ASS&na_item=F&unit=MIO_EUR&co_nco=NCO"),
        pf=es("nasa_10_f_bs", "geo=NL&sector=S129&finpos=ASS&na_item=F&unit=MIO_EUR&co_nco=NCO"),
    )


if __name__ == "__main__":
    s = series()
    for y in [int(a) for a in sys.argv[1:]] or [2021]:
        l1 = s["emu"][y]
        l2 = l1 + s["gar"][y]
        l3 = l2 + s["aow"][y]
        l4a = l3 - s["fa"][y]
        l4b = l4a - BELASTING * s["pf"][y]
        print(f"{y}: L1 {l1:.0f}; L2 {l2:.0f}; L3 {l3:.0f}; L4a {l4a:.0f}; L4b {l4b:.0f}")
