#!/usr/bin/env python3
"""PBW-berekening Nederland volgens regelbestand/vaste_definities_NEPK_NTPK_PBW.md

PBW = (BBP - TH - FISIM) x (W / B) - U - (u - u*) x beta x BBP

Alle invoer wordt rechtstreeks uit CBS StatLine (OData) gehaald:
  BBP    85865NED  BrutoBinnenlandsProduct_21 (werkelijke prijzen, mln euro)
  TH     85873NED  HuurwaardeVanDeWoning_29 (consumptie huurwaarde eigen woning, mln euro)
  FISIM  85882NED  ProductieVanIGDFI_9, Totale binnenlandse sectoren, niet-geconsolideerd (mln euro)
  U      85882NED  huishoudens incl. IZW (middelen): UitkeringenSocialeZekerheidInGeld_53
                   + UitkeringenOverigeSocialeVerzekering_54 + UitkeringenSocialeVoorzieningInGeld_55
                   (= sociale uitkeringen in geld, ESA D.62, mln euro)
  W, B, u 85264NED Werkzame beroepsbevolking_3, Beroepsbevolking_2, Werkloosheidspercentage_21
                   (15-75 jaar, totaal, jaarcijfers)
Vaste parameters: u* = 3,0 %, beta = 2 (Okun, 1962).
Gebruik: python3 scripts/pbw_berekening.py [jaar ...]
"""
import json
import sys
import urllib.request

API = "https://opendata.cbs.nl/ODataApi/odata"
U_STAR = 0.03
BETA = 2.0


def get(table, flt, select):
    url = f"{API}/{table}/TypedDataSet?$filter={flt}&$select={select}&$format=json"
    url = url.replace(" ", "%20").replace("'", "%27")
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)["value"]


def per(year):
    return f"Perioden eq '{year}JJ00'"


def inputs(year):
    p = per(year)
    bbp = get("85865NED", p, "BrutoBinnenlandsProduct_21")[0]["BrutoBinnenlandsProduct_21"]
    th = get("85873NED", p, "HuurwaardeVanDeWoning_29")[0]["HuurwaardeVanDeWoning_29"]
    nc = "NietGeconsolideerdOfGeconsolideerd eq 'A045217'"
    fisim = get("85882NED", f"{p} and {nc} and InstitutioneleSectoren eq 'A044924'",
                "ProductieVanIGDFI_9")[0]["ProductieVanIGDFI_9"]
    hh = get("85882NED", f"{p} and {nc} and InstitutioneleSectoren eq 'A044945'",
             "UitkeringenSocialeZekerheidInGeld_53,UitkeringenOverigeSocialeVerzekering_54,"
             "UitkeringenSocialeVoorzieningInGeld_55")[0]
    u_geld = (hh["UitkeringenSocialeZekerheidInGeld_53"] + hh["UitkeringenOverigeSocialeVerzekering_54"]
              + hh["UitkeringenSocialeVoorzieningInGeld_55"])
    ar = get("85264NED", f"{p} and Geslacht eq 'T001038' and Leeftijd eq '52052' and "
                         "HoogstBehaaldOnderwijsniveau eq 'T001143'",
             "Beroepsbevolking_2,WerkzameBeroepsbevolking_3,Werkloosheidspercentage_21")[0]
    return dict(BBP=bbp, TH=th, FISIM=fisim, U=u_geld, W=ar["WerkzameBeroepsbevolking_3"],
                B=ar["Beroepsbevolking_2"], u=ar["Werkloosheidspercentage_21"] / 100)


def pbw(x):
    kern = x["BBP"] - x["TH"] - x["FISIM"]
    wb = x["W"] / x["B"]
    okun = (x["u"] - U_STAR) * BETA * x["BBP"]
    waarde = kern * wb - x["U"] - okun
    return dict(kern=kern, wb=wb, productief=kern * wb, okun=okun, PBW=waarde, aandeel=waarde / x["BBP"])


if __name__ == "__main__":
    jaren = sys.argv[1:] or ["2022", "2023", "2024", "2025"]
    print("jaar;BBP;TH;FISIM;W/B;U;u;Okun;PBW;PBW_%BBP  (mln euro)")
    for j in jaren:
        x = inputs(j)
        r = pbw(x)
        print(f"{j};{x['BBP']:.0f};{x['TH']:.0f};{x['FISIM']:.0f};{r['wb']:.4f};{x['U']:.0f};"
              f"{x['u']*100:.1f};{r['okun']:.0f};{r['PBW']:.0f};{r['aandeel']*100:.1f}")
