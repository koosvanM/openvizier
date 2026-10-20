#!/usr/bin/env python3
"""NEPK- en NTPK-jaarreeks Nederland volgens regelbestand/vaste_definities_NEPK_NTPK_PBW.md

NEPK = E_tv x alpha x (1 - tau) x phi ;  NTPK = E_tv x alpha x (1 - tau)

Bronnen (alle rechtstreeks opgehaald):
  E_tv  OESO TiVA 2025-editie (DSD_TIVA_MAINLV@DF_MAINLV): EXGR_DVA / VALU (NLD, _T, W, USD)
        x CBS 85865NED (bruto toegevoegde waarde basisprijzen / bbp) -> aandeel van het bbp
  alpha Wereldbank NV.IND.TOTL.ZS (industrie incl. bouw en energie, % bbp)
  tau   OESO Revenue Statistics (DSD_REV_COMP_OECD@DF_RSOECD): totale belastingopbrengst, % bbp
  phi   2015-2020: CBS 81358ned, B-N excl. K incl. 95: 1 - TW buitenland / TW totaal
        2021-2024: Eurostat fats_activ (= CBS IFATS; 2024 identiek aan CBS 85821NED), B-S excl. O en S94:
                   TW binnenlandse zeggenschap / TW alle landen
        Methodebreuk 2021 (juridische eenheid -> onderneming, bredere sectordekking).
Gebruik: python3 scripts/nepk_reeks.py
"""
import csv
import io
import json
import urllib.request

UA = {"User-Agent": "Mozilla/5.0"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8")


def oecd_csv(url):
    return list(csv.DictReader(io.StringIO(fetch(url))))


def e_tv():
    rows = oecd_csv("https://sdmx.oecd.org/sti-public/rest/data/OECD.STI.PIE,DSD_TIVA_MAINLV@DF_MAINLV,1.1/"
                    "EXGR_DVA+VALU.NLD._T.W..A?startPeriod=2015&format=csvfilewithlabels")
    v = {}
    for r in rows:
        v.setdefault(r["MEASURE"], {})[int(r["TIME_PERIOD"])] = float(r["OBS_VALUE"])
    cbs = json.loads(fetch("https://opendata.cbs.nl/ODataApi/odata/85865NED/TypedDataSet?"
                           "$select=Perioden,Totaal_3,BrutoBinnenlandsProduct_21&$format=json"))["value"]
    ratio = {int(r["Perioden"][:4]): r["Totaal_3"] / r["BrutoBinnenlandsProduct_21"] for r in cbs if "JJ" in r["Perioden"]}
    return {y: v["EXGR_DVA"][y] / v["VALU"][y] * ratio[y] for y in v["VALU"] if y in v.get("EXGR_DVA", {})}


def alpha():
    d = json.loads(fetch("https://api.worldbank.org/v2/country/NLD/indicator/NV.IND.TOTL.ZS?format=json&date=2015:2025&per_page=50"))
    return {int(x["date"]): x["value"] / 100 for x in d[1] if x["value"] is not None}


def tau():
    rows = oecd_csv("https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_OECD@DF_RSOECD,2.0/"
                    "NLD.TAX_REV.S13._T._T.PT_B1GQ.A?startPeriod=2015&format=csvfilewithlabels")
    return {int(r["TIME_PERIOD"]): float(r["OBS_VALUE"]) / 100 for r in rows}


def phi():
    out = {}
    d = json.loads(fetch("https://opendata.cbs.nl/ODataApi/odata/81358ned/TypedDataSet?"
                         "$filter=BedrijfstakkenBranchesSBI2008%20eq%20%27800011%27&"
                         "$select=LandVanUiteindelijkeZeggenschapUCI,Perioden,ToegevoegdeWaardeTegenFactorkosten_5&$format=json"))["value"]
    t = {}
    for r in d:
        t.setdefault(int(r["Perioden"][:4]), {})[r["LandVanUiteindelijkeZeggenschapUCI"].strip()] = r["ToegevoegdeWaardeTegenFactorkosten_5"]
    for y, x in t.items():
        if y >= 2015:
            out[y] = (1 - x["A042601"] / x["T001047"], "CBS 81358ned B-N excl. K")
    e = json.loads(fetch("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/fats_activ?"
                         "geo=NL&nace_r2=B-S_X_O_S94&indic_sbs=AV_MEUR&c_ctrl=DOM&c_ctrl=WORLD&format=JSON"))
    dims, sizes = e["id"], e["size"]
    lab = {k: e["dimension"][k]["category"]["index"] for k in dims}

    def g(c, t_):
        sel = {k: 0 for k in dims}
        sel["c_ctrl"], sel["time"] = lab["c_ctrl"][c], lab["time"][t_]
        i = 0
        for k, s in zip(dims, sizes):
            i = i * s + sel[k]
        return e["value"].get(str(i))
    for t_ in lab["time"]:
        dom, wld = g("DOM", t_), g("WORLD", t_)
        if dom and wld:
            out[int(t_)] = (dom / wld, "Eurostat fats_activ B-S excl. O, S94")
    return out


if __name__ == "__main__":
    E, A, T, P = e_tv(), alpha(), tau(), phi()
    print("jaar;E_tv;alpha;tau;phi;NTPK_%bbp;NEPK_%bbp;bron_phi")
    for y in range(2015, 2025):
        e = E.get(y)
        a, t, (p, src) = A.get(y), T.get(y), P.get(y, (None, ""))
        if None in (a, t, p):
            continue
        if e is None:
            print(f"{y};-;{a:.4f};{t:.4f};{p:.4f};-;-;{src} (E_tv nog niet gepubliceerd)")
            continue
        ntpk = e * a * (1 - t)
        print(f"{y};{e:.4f};{a:.4f};{t:.4f};{p:.4f};{ntpk*100:.2f};{ntpk*p*100:.2f};{src}")
