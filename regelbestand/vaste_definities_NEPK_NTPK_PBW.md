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

| Component | Betekenis | Vaste bron |
|---|---|---|
| BBP | Officieel bruto binnenlands product, lopende prijzen | CBS nationale rekeningen |
| TH | Geïmputeerde (toegerekende) huur eigen woning, als productie | CBS nationale rekeningen |
| FISIM | Indirect gemeten financiële diensten | CBS nationale rekeningen |
| W / B | Werkzame beroepsbevolking gedeeld door beroepsbevolking | CBS |
| U | Sociale uitkeringen in geld | CBS nationale rekeningen |
| Okun-correctie | −(u − u*) × β × BBP, met u = werkloosheidspercentage (CBS, jaar), u* = 0,03, β = 2 | Okun (1962); vaste parameters |

**Correctie 20 oktober 2026:** de oorspronkelijke PBW-berekening (juli 2026) gebruikte TH = €97 miljard voor 2024. Die waarde heeft geen bron. Het CBS geeft voor 2024 een geïmputeerde huur van €54 miljard. De waarden PBW 2024 = €709 miljard (62,9%) en de schuldlagen op PBW (68% / 104% / 400% / 170%) vervallen daarmee als referentie.

**Voorlopige herberekening 2024 (assistentberekening):** BBP €1.122,5 mld (CBS) − TH €54 mld − FISIM €40 mld = €1.028,5 mld; × W/B 0,963 = €990,4 mld; − U €229,9 mld; − Okun (0,7 pp × 2 × BBP) €15,7 mld = **PBW ≈ €745 mld = 66,4% van het BBP**. Schuldlagen op deze PBW: 67% / 99% / 380% / 167%. FISIM, U en W/B zijn de juliwaarden en moeten nog bij het CBS worden nagecontroleerd voordat dit de vaste referentie wordt.

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

> **Controle PBW-invoer 2024.** FISIM, sociale uitkeringen in geld en W/B nacontroleren bij het CBS; daarna wordt de herberekening in § 5 de vaste referentie en worden de PBW-cijfers in "Eerlijkheid maakt regeren mogelijk" aangepast.
