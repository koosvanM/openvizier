# Vaste definities NEPK, NTPK en PBW

**Status:** bindend voor alle berekeningen, grafieken, apps en artikelen op openvizier.org
**Vastgelegd:** 20 oktober 2026, in opdracht van Jacobus van Merksteijn
**Rangorde:** dit bestand gaat vóór `regelbestand_v3.13.md` (§ NEPK) en `regelbestand_gevolgenkaart_V4.1.md` (§ 3) waar die afwijken.

Regel 2 blijft gelden: alles wat gebouwd wordt, eerst verifiëren, dan pas bouwen.

---

## 1. Formules

```
NEPK = E_tv × α × (1 − τ) × φ
NTPK = E_tv × α × (1 − τ)  =  NEPK / φ
PBW  = (BBP − TH − FISIM) × (W / B) − U + Okun-correctie
```

- **NEPK** is de primaire maat: het deel van de exportgebonden productieve kern dat na lasten in Nederlandse handen is.
- **NTPK** is de afgeleide maat: dezelfde kern ongeacht eigenaar. Het verschil NTPK − NEPK is de buitenlands-eigendom-schil.
- **PBW** (Productieve Brede Welvaart) is de productieve draagkrachtnoemer naast het officiële BBP.

## 2. Factoren NEPK en NTPK (vast factorcontract)

| Factor | Wat het meet | Vaste bron | Eenheid |
|---|---|---|---|
| E_tv | Binnenlandse toegevoegde waarde in de export, als deel van het BBP | OESO TiVA 2025-editie: EXGR_DVA / VALU (NLD, alle activiteiten, partner wereld), omgerekend naar BBP met CBS 85865NED (bruto toegevoegde waarde basisprijzen / BBP) | decimaal van BBP |
| α | Toegevoegde waarde van industrie, inclusief bouw en energie, als deel van het BBP | Wereldbank NV.IND.TOTL.ZS | decimaal van BBP |
| τ | Belastingen plus sociale premies, als deel van het BBP | OESO Revenue Statistics (DSD_REV_COMP_OECD@DF_RSOECD, TAX_REV, S13, totaal, % BBP) | decimaal van BBP |
| φ | Aandeel toegevoegde waarde onder binnenlandse zeggenschap, bedrijven B-N excl. K | 2015–2020: CBS 81358ned: 1 − TW buitenland / TW totaal. 2021–2024: Eurostat fats_activ (= CBS IFATS), som van secties B t/m N excl. K: TW binnenlands / TW alle landen; vertrouwelijke secties aan beide kanten weggelaten | decimaal |

Reproduceerbaar script: [`scripts/nepk_reeks.py`](../scripts/nepk_reeks.py).

**Breuk φ in 2021:** de sectordekking is gelijk gehouden (B-N excl. K). Alleen de statistische eenheid wijzigde (juridische eenheid → onderneming); de aansluiting 2020 → 2021 (0,715 → 0,702) wijst niet op een groot niveau-effect.

Geen andere bron of maatstaf per factor. Een waarde verandert alleen als een van deze vier bronnen nieuwe cijfers publiceert.

## 3. Rekenregels

1. **Noemer:** NEPK en NTPK zijn een percentage van het officiële BBP. Binnen één vergelijking wordt de noemer niet gewisseld naar PBW, loonsom, huishoudinkomen of geldinstroom zonder een apart vastgelegde brug.
2. **Jaarwaarde:** een jaarwaarde bestaat alleen als alle vier factoren uit hetzelfde jaar komen. Een combinatie van de nieuwste cijfers uit verschillende jaren heet **samengestelde stand** en wordt altijd zo gelabeld, nooit als meting van één jaar.
3. **Reeksen en dalingen:** een reeks of dalingssnelheid mag alleen uit waarden met dit factorcontract worden gevormd. Waarden uit een ander contract (zie § 6) worden er niet mee verbonden.
4. **Eén φ:** NTPK en NEPK gebruiken dezelfde φ en dezelfde populatie, zodat NTPK / NEPK = 1 / φ.
5. **Landen:** een landenvergelijking gebruikt per land hetzelfde factorcontract. Een land zonder vergelijkbare φ krijgt geen NEPK, alleen een NTPK.
6. **Toeschrijving:** berekeningen en scenario's van de assistent worden als assistentberekening gelabeld.

## 4. NEPK- en NTPK-jaarreeks Nederland (gemeten, dit contract)

| Jaar | E_tv | α | τ | φ | NTPK | NEPK |
|---|---|---|---|---|---|---|
| 2015 | 0,3612 | 0,1741 | 0,3652 | 0,7192 | 3,99% | 2,87% |
| 2016 | 0,3540 | 0,1696 | 0,3777 | 0,7091 | 3,74% | 2,65% |
| 2017 | 0,3629 | 0,1712 | 0,3805 | 0,7033 | 3,85% | 2,71% |
| 2018 | 0,3639 | 0,1732 | 0,3814 | 0,6995 | 3,90% | 2,73% |
| 2019 | 0,3566 | 0,1711 | 0,3847 | 0,6958 | 3,76% | 2,61% |
| 2020 | 0,3460 | 0,1738 | 0,3902 | 0,7153 | 3,67% | 2,62% |
| 2021 | 0,3586 | 0,1771 | 0,3826 | 0,7023 | 3,92% | 2,75% |
| 2022 | 0,3547 | 0,1866 | 0,3807 | 0,6817 | 4,10% | 2,79% |
| 2023 | n.b. | 0,1816 | 0,3926 | 0,6854 | n.b. | n.b. |
| 2024 | n.b. | 0,1754 | 0,3854 | 0,6805 | n.b. | n.b. |

n.b. = E_tv nog niet gepubliceerd (TiVA 2025-editie loopt tot 2022).

Extrapolatie (assistent, aanname E_tv = waarde 2022): 2023 NTPK 3,91% / NEPK 2,68%; 2024 NTPK 3,82% / NEPK 2,60%.

Trend 2015–2024 (assistent, lineair): NEPK −0,005 procentpunt per jaar; φ −0,0036 per jaar (buitenlands-eigendom-schil van 28% naar 32% van de kern).

Correctie samengestelde stand: de eerdere 2,87% gebruikte φ = 0,7425 op een bredere sectordekking (B-S excl. O en S94). Met de vaste dekking B-N excl. K (φ 2024 = 0,6805) wordt die stand 2,63%.

## 5. PBW-componenten

```
PBW = (BBP − TH − FISIM) × (W / B) − U − (u − u*) × β × BBP
```

| Component | Betekenis | Vaste bron (CBS StatLine) |
|---|---|---|
| BBP | Bruto binnenlands product, werkelijke prijzen | 85865NED, BrutoBinnenlandsProduct_21 |
| TH | Huurwaarde eigen woning (toegerekende huur) | 85873NED, HuurwaardeVanDeWoning_29 |
| FISIM | Productie van indirect gemeten diensten van financiële intermediairs (IGDFI), totale binnenlandse sectoren | 85882NED, ProductieVanIGDFI_9 |
| W / B | Werkzame beroepsbevolking / beroepsbevolking, 15–75 jaar | 85264NED, WerkzameBeroepsbevolking_3 / Beroepsbevolking_2 |
| U | Sociale uitkeringen in geld ontvangen door huishoudens (ESA D.62: sociale zekerheid + overige sociale verzekering + sociale voorziening) | 85882NED, kolommen 53 + 54 + 55, sector huishoudens incl. IZW |
| u | Werkloosheidspercentage, 15–75 jaar | 85264NED, Werkloosheidspercentage_21 |
| Okun-correctie | (u − u*) × β × BBP, met u* = 0,03 en β = 2 | vaste parameters (Okun, 1962) |

Reproduceerbaar script: [`scripts/pbw_berekening.py`](../scripts/pbw_berekening.py) haalt alle invoer rechtstreeks bij het CBS op.

### Referentiewaarden PBW (CBS-stand 23 september 2026, mln euro)

| Jaar | BBP | TH | FISIM | W/B | U | u | Okun | PBW | PBW % BBP |
|---|---|---|---|---|---|---|---|---|---|
| 2022 | 993.820 | 49.578 | 25.830 | 0,9646 | 154.721 | 3,5% | 9.938 | 721.277 | 72,6% |
| 2023 | 1.050.133 | 51.578 | 23.725 | 0,9644 | 173.537 | 3,6% | 12.602 | 754.028 | 71,8% |
| 2024 | 1.115.252 | 54.362 | 22.040 | 0,9634 | 186.424 | 3,7% | 15.614 | 798.813 | 71,6% |
| 2025 | 1.170.579 | 57.531 | 23.964 | 0,9613 | 197.287 | 3,9% | 21.070 | 828.564 | 70,8% |

Controle: script en een onafhankelijke handberekening met dezelfde CBS-waarden geven identieke uitkomsten.

**Vervallen waarden (juli 2026):** PBW 2024 = €709 mld (62,9%) rustte op TH €97 mld, FISIM €40 mld en U €229,9 mld zonder traceerbare bron, en op een inmiddels herzien BBP (€1.128,2 mld). Die waarden en de schuldlagen uit juli (44% / 65% / 250% / 110% op BBP; 68% / 104% / 400% / 170% op PBW) vervallen; zie § 5b.

**FISIM-overcorrectie (2024, uitgezocht):** alleen het deel van FISIM in finale bestedingen zit in het BBP. Uit CBS 85882NED (correctie voor IGDFI per sector, uitvoer en invoer van IGDFI): FISIM in het BBP ligt tussen €6,2 mld (zonder leningen van huishoudens, die grotendeels in de toegerekende huur zitten) en €17,2 mld (met). Aftrek van de totale productie (€22,0 mld) corrigeert dus €4,8–15,8 mld te veel. PBW 2024 ligt daardoor tussen €798,8 mld (71,6%) en €814,1 mld (73,0%). De vaste definitie blijft de totale productie (behoudende ondergrens).

## 5b. Schuldlagen (traceerbaar)

| Laag | Definitie | Bron |
|---|---|---|
| 1 | EMU-schuld | Eurostat gov_10dd_edpt1 |
| 2 | Laag 1 + uitstaande overheidsgaranties | Eurostat gov_cl_guar |
| 3 | Laag 2 + opgebouwde AOW-rechten (accrued-to-date) | Eurostat nasa_10_pens1 (S13PS), alleen 2015, 2018, 2021 |
| 4a | Laag 3 − financiële activa van de overheid | Eurostat nasa_10_f_bs (S13) |
| 4b | Laag 4a − 35% × pensioenvermogen (latente belastingclaim) | Eurostat nasa_10_f_bs (S129); 35% is een aanname |

Reproduceerbaar script: [`scripts/schuldlagen.py`](../scripts/schuldlagen.py). Garanties en AOW-rechten zijn volgens Eurostat voorwaardelijke verplichtingen, geen EMU-schuld.

| Jaar | Laag 1 | Laag 2 | Laag 3 | Laag 4a | Laag 4b |
|---|---|---|---|---|---|
| 2015, mld € | 446,2 | 751,4 | 1.904,6 | 1.557,4 | 1.121,4 |
| 2015, % BBP / % PBW | 64 / 117 | 107 / 197 | 272 / 498 | 223 / 408 | 160 / 293 |
| 2018, mld € | 405,9 | 722,8 | 2.248,0 | 1.894,6 | 1.385,4 |
| 2018, % BBP / % PBW | 52 / 78 | 92 / 140 | 286 / 435 | 241 / 366 | 176 / 268 |
| 2021, mld € | 450,2 | 773,4 | 2.638,3 | 2.205,5 | 1.513,7 |
| 2021, % BBP / % PBW | 51 / 74 | 87 / 126 | 296 / 431 | 247 / 360 | 170 / 247 |

Langdurige zorg en andere vergrijzingskosten: niet als voorraad gemeten, wel als officiële houdbaarheidsmaat. Europese Commissie, Debt Sustainability Monitor 2025: S2 = 3,9% BBP (begroting 1,0; vergrijzing 2,8, waarvan pensioenen 1,0, zorg 0,6, langdurige zorg 1,6). AOW-rechten na 2021: eerstvolgende verplichte meting 2024.

## 6. Afwijkende contracten (niet conform, niet mengen)

| Bestand | Afwijking | Gevolg |
|---|---|---|
| `regelbestand_gevolgenkaart_V4.1.md` § 3 | E_tv = bruto export; α = 0,39 "productieve kern na overhead"; φ = 0,53 breed eigendomsbegrip | ankers 4,5% (2026) en reeks 9,0% → 3,3% vallen buiten dit contract |
| `regelbestand_v3.13.md` regels 116–117 | E_tv = CBS DTFF zonder doorvoer (0,31); α = 0,40; φ = 0,53 | NEPK 3,75% valt buiten dit contract |
| NEPK-rapport april 2026 (1970–2050) | modelmatige reeks 6,4% → 7,2% → 4,2% | modelreeks, geen meting met dit contract |

Deze waarden blijven zichtbaar in de bestaande publicaties, maar worden niet met § 4 tot één reeks verbonden totdat ze met dit contract zijn herberekend.

---

## Vastgestelde namen

- **NEPK** — Nederlandse Economische Productie Kern
- **NTPK** — Netto Totale ProductieKern
- **PBW** — Productieve Brede Welvaart
- **NPK** valt buiten deze vaste definities zolang ψ geen vaste bron heeft.

## Nog te doen

> **Artikel bijwerken.** De PBW-cijfers en de schuldlagen in "Eerlijkheid maakt regeren mogelijk" aanpassen aan § 5 en § 5b.
