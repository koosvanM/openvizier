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

| Component | Betekenis | Bron |
|---|---|---|
| BBP | Officieel bruto binnenlands product, lopende prijzen | CBS |
| TH | Toegerekende huur van eigenaar-bewoners | CBS nationale rekeningen |
| FISIM | Indirect gemeten bankdiensten | CBS nationale rekeningen |
| W / B | Werkzame beroepsbevolking gedeeld door beroepsbevolking | CBS |
| U | Uitkeringen | CBS |
| Okun-correctie | Correctie voor de productiekosten van werkloosheid (Okun, 1962) | zie open blok |

Artikelwaarden 2024: TH €97 of €54 miljard (zie open blok 2), FISIM €40 miljard, U €230 miljard.

Referentie: PBW 2024 = €709 miljard = 62,9% van het officiële BBP (bron: "Eerlijkheid maakt regeren mogelijk"). Schuldlagen op PBW: 68% / 104% / 400% / 170%.

## 6. Afwijkende contracten (niet conform, niet mengen)

| Bestand | Afwijking | Gevolg |
|---|---|---|
| `regelbestand_gevolgenkaart_V4.1.md` § 3 | E_tv = bruto export; α = 0,39 "productieve kern na overhead"; φ = 0,53 breed eigendomsbegrip | ankers 4,5% (2026) en reeks 9,0% → 3,3% vallen buiten dit contract |
| `regelbestand_v3.13.md` regels 116–117 | E_tv = CBS DTFF zonder doorvoer (0,31); α = 0,40; φ = 0,53 | NEPK 3,75% valt buiten dit contract |
| NEPK-rapport april 2026 (1970–2050) | modelmatige reeks 6,4% → 7,2% → 4,2% | modelreeks, geen meting met dit contract |

Deze waarden blijven zichtbaar in de bestaande publicaties, maar worden niet met § 4 tot één reeks verbonden totdat ze met dit contract zijn herberekend.

---

## Open blokken

> **Open 1 — Okun-correctie.** De operationele rekenregel (welke werkloosheidsmaat, welke Okun-coëfficiënt, welk teken) staat niet in de bron. Vast te leggen vóór herberekening van PBW.

> **Open 2 — Toegerekende huur.** Het artikel "Eerlijkheid maakt regeren mogelijk" noemt voor TH zowel €97 miljard als €54 miljard. Eén waarde en bron vast te leggen.

> **Open 3 — PBW-aandeel 2024.** Hetzelfde artikel noemt 62,9% en "richting 64%" voor 2024. Eén waarde vast te leggen.

> **Open 4 — Uitgeschreven namen.** NEPK verschijnt als "Nederlandse Economische Productie Kern" en als "Netto Economisch Productiekapitaal"; NTPK als "Netto Totale ProductieKern" en (V4.1) "Nationaal Tetsuo Productief Kapitaal". Eén naam per maat vast te stellen door de auteur.

> **Open 5 — NPK.** `NPK = NTPK × (1 + ψ)` valt buiten deze vaste definities zolang ψ geen vaste bron heeft.
