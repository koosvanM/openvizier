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
| E_tv | Binnenlandse toegevoegde waarde in de export, als deel van het BBP | OESO TiVA | decimaal van BBP |
| α | Toegevoegde waarde van industrie, inclusief bouw en energie, als deel van het BBP | Wereldbank (industry value added) | decimaal van BBP |
| τ | Belastingen plus sociale premies, als deel van het BBP | OESO Revenue Statistics | decimaal van BBP |
| φ | 1 − aandeel toegevoegde waarde van bedrijven onder buitenlandse zeggenschap | CBS 85821NED | decimaal |

Geen andere bron of maatstaf per factor. Een waarde verandert alleen als een van deze vier bronnen nieuwe cijfers publiceert.

## 3. Rekenregels

1. **Noemer:** NEPK en NTPK zijn een percentage van het officiële BBP. Binnen één vergelijking wordt de noemer niet gewisseld naar PBW, loonsom, huishoudinkomen of geldinstroom zonder een apart vastgelegde brug.
2. **Jaarwaarde:** een jaarwaarde bestaat alleen als alle vier factoren uit hetzelfde jaar komen. Een combinatie van de nieuwste cijfers uit verschillende jaren heet **samengestelde stand** en wordt altijd zo gelabeld, nooit als meting van één jaar.
3. **Reeksen en dalingen:** een reeks of dalingssnelheid mag alleen uit waarden met dit factorcontract worden gevormd. Waarden uit een ander contract (zie § 6) worden er niet mee verbonden.
4. **Eén φ:** NTPK en NEPK gebruiken dezelfde φ en dezelfde populatie, zodat NTPK / NEPK = 1 / φ.
5. **Landen:** een landenvergelijking gebruikt per land hetzelfde factorcontract. Een land zonder vergelijkbare φ krijgt geen NEPK, alleen een NTPK.
6. **Toeschrijving:** berekeningen en scenario's van de assistent worden als assistentberekening gelabeld.

## 4. Referentiewaarden Nederland (dit contract)

| Stand | E_tv | α | τ | φ | NTPK | NEPK |
|---|---|---|---|---|---|---|
| 2021 | | | | 0,817 | 3,98% | 3,25% |
| 2022 | 0,355 | | | | 4,10% | 3,01% |
| Samengestelde stand (E_tv 2022, α 2025, τ 2024, φ 2023) | 0,355 | 0,177 | 0,385 | 0,744 | 3,86% | 2,87% |

Controle samengestelde stand: 0,355 × 0,177 × 0,615 = 0,03864 → NTPK 3,86%; × 0,744 = 0,02875 → NEPK 2,87%.

Lege cellen: factorwaarden per jaar nog in het bronregister vast te leggen.

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

**Vervallen waarden (juli 2026):** PBW 2024 = €709 mld (62,9%) rustte op TH €97 mld, FISIM €40 mld en U €229,9 mld zonder traceerbare bron, en op een inmiddels herzien BBP (€1.128,2 mld). Die waarden en de schuldlagen op PBW (68% / 104% / 400% / 170%) vervallen.

**Bekende beperking FISIM:** alleen het deel van FISIM dat in finale bestedingen terechtkomt, zit in het BBP. Aftrek van de totale productie van IGDFI corrigeert daarom iets te veel (maximaal circa 2% van het BBP).

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

> **Artikel bijwerken.** De PBW-cijfers en de schuldlagen op PBW in "Eerlijkheid maakt regeren mogelijk" aanpassen aan § 5.
