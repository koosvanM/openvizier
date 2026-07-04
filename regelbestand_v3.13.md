# Regelbestand Gevolgenkaart — versie 3.12c (canoniek)

**Datum:** 4 juli 2026
**Auteur:** Jacobus van Merksteijn
**Status:** Canoniek — alles wat vanaf nu wordt gebouwd volgt deze regels.

**Wijziging t.o.v. v3.11:** vier-factor NEPK-formule vervangt scalar-model; drie-orde-modulatie per partij per factor; NTPK als afgeleide grootheid; bundel-visualisatie met 8 vergelijkingspartijen; kleur-oplossing NL→hex; historische baseline; vragen-flow-volgorde vast.

**Formule-anker:**
$$\text{NEPK}\% = E_{tv} \times \alpha \times (1-\tau) \times \varphi$$
$$\text{NTPK}\% = E_{tv} \times \alpha \times (1-\tau) = \text{NEPK} / \varphi$$

**Startwaarden 2026 (eigen berekening uit CBS/OECD):**
- E_tv = 31,0 % BBP (CBS DTFF 2024, doorvoer eruit)
- α = 0,40 (canonieke schatting productieve kern na overhead-aftrek)
- τ = 0,43 (OECD Revenue Statistics + regeldruk + rigiditeit)
- φ = 0,53 (CBS StatLine 85821ENG, foreign-controlled aandeel productieve activa)
- **NTPK 2026 = 7,07 % BBP · NEPK 2026 = 3,75 % BBP**

**Grondregel (traagheid):** alle partij-effecten zijn traag. Geen enkele partij levert shock. Zelfs een 100% consequente partij verzet in de eerste drie jaar nauwelijks meer dan 0,01–0,20 pp op één factor. Ombuigen kost tijd.

**Grondregel (verificatie):** alles wat wordt gebouwd moet zelfstandig verifieerbaar zijn. Bron per waarde. Bij discrepantie met documenten: transparant documenteren, niet stilzwijgend aanpassen.

---

## Regels 1-115

Behouden zoals vastgesteld in v3.7 t/m v3.11. Zie `regelbestand_v3.11.md`. De belangrijkste regels die actief blijven:

- **Regel 102**: NL v2 juli-1 als canonieke referentie
- **Regel 103**: baseline-drift voor UI-weergave (nullijn)
- **Regel 105**: referentiemodellen VMP-Nova en CARB als aparte grafiek-lijnen
- **Regel 106/107**: statistical parity audit tussen matrices
- **Regel 108**: leverbaarheid-gewogen coalitie-vulling voor niet-gescoorde cellen
- **Regel 111**: canonieke NL-schaal v/5000 × envelope (schaal-fix)
- **Regel 113/114**: NEPK-tijdreeks als macro-anker + sociaal kantelpunt bij NEPK < 3,0
- **Regel 115**: drie-weg partij-modulatie NEPK/FDI/schuld — nu vervangen door regels 116-120

---

## Nieuwe regels v3.12c

### Regel 116 — Canonieke vier-factor NEPK-formule

De Netto Externe Productieve Kern wordt berekend als een multiplicatief product van vier onafhankelijke factoren:

$$\text{NEPK}\% = E_{tv} \times \alpha \times (1 - \tau) \times \varphi$$

Bronbevestiging: [nepk-indicator-methodologie.pdf](https://novademocratia.com/assets/docs/nepk-indicator-methodologie.pdf), [de-nederlandse-ondergang.pdf p.5](https://novademocratia.com/assets/docs/de-nederlandse-ondergang.pdf), [nepk-evaluatie-nederland-2024-2026.pdf p.2](https://novademocratia.com/assets/docs/nepk-evaluatie-nederland-2024-2026.pdf).

**Factordefinities (verbatim uit brondocumenten):**

| Factor | Betekenis | Eenheid | Bron |
|---|---|---|---|
| E_tv | Export-toegevoegde waarde als % BBP, exclusief doorvoer (Rotterdam-effect: ~52% van bruto-export is doorvoer) | % BBP | CBS DTFF 2024 |
| α | Aandeel productieve kern in economie, exclusief overhead, compliance en management | index 0-1 | canoniek |
| τ | Effectieve collectieve lastendruk (belasting + premies + btw + regeldruk + arbeidsmarktrigiditeit) | index 0-1 | OECD Revenue Statistics |
| φ | Aandeel productieve activa in nationale handen | index 0-1 | CBS StatLine 85821ENG |

**Belangrijke uitsluiting:** De opdracht overwoog een vijfde factor ψ (buitenlandse-productie-in-NL-handen). Deze factor bestaat **niet** in de canonieke formule. Winstrepatriëring is een mechanisme *binnen* φ, geen zelfstandige term. NEPK blijft strikt vier-factor.

### Regel 117 — NTPK als afgeleide grootheid

De Netto Totale ProductieKern is de productie op Nederlands grondgebied die voor het buitenland produceert, ongeacht eigenaar. Formeel:

$$\text{NTPK} = E_{tv} \times \alpha \times (1 - \tau) = \text{NEPK} / \varphi$$

NTPK meet dus wat er potentieel productief is; NEPK meet wat daarvan in Nederlandse handen blijft. Het verschil (NTPK − NEPK) is de buitenlands-eigendom-schil.

**Startwaarden 2026:**

| Factor | Waarde | Bron |
|---|---:|---|
| E_tv | 31,0 % | CBS DTFF 2024: domestic goods+services value added, doorvoer eruit |
| α | 0,40 | Canonieke schatting, Wereldbank industrie+bouw+landbouw = 23% BBP, waarvan ~40% productief-kern |
| τ | 0,43 | OECD Revenue Statistics NL 2023 = 38,6 % + regeldruk 3-5 % + rigiditeit 1-2 % |
| φ | 0,53 | CBS StatLine 85821ENG: 25,6 % foreign-controlled in productieve activa |
| **NTPK** | **7,07 %** | E_tv × α × (1−τ) |
| **NEPK** | **3,75 %** | NTPK × φ |

**Discrepantie met documenten (transparant):** de canonieke documenten noemen NEPK 2026 = 4,5 % centraal (band 4,1-4,9 %) en methodologie-doc 5,2 %. Eigen reconstructie geeft 3,75 %. Verschil zit in E_tv-definitie (doorvoer strikt eruit vs deels-inclusief). Engine gebruikt 3,75 % als strikt-verifieerbare startwaarde.

### Regel 118 — Drie-orde-modulatie per partij per factor

Elke partij moduleert de vier factoren via drie ordes van tijdrespons:

| Orde | Actief in jaar | Betekent | Cumulatief gewicht |
|---|---|---|---:|
| 1e orde | jaar 1-3 | onmiddellijke intentie, aanloop | 3 jaar |
| 2e orde | jaar 4-8 | doorwerking na eerste beleidscyclus | 5 jaar |
| 3e orde | jaar 9-15 | structurele verankering | 7 jaar |

Voor factor $X$ door partij $P$ wordt de cumulatieve verschuiving na 15 jaar:

$$\Delta X_{15j} = (\text{orde1} \times 3 + \text{orde2} \times 5 + \text{orde3} \times 7) \times \text{leverbaarheid}$$

De factor evolueert lineair binnen elk orde-blok:
$$X(t+1) = X(t) + \text{orde-actief}(t) \times \text{leverbaarheid}$$

### Regel 119 — Kalibratie-plafonds (traagheidsprincipe)

**Historisch tempo NL 2000-2026 (26 jaar):**
- α: −0,0077 pp/jaar (gedaald 0,60 → 0,40)
- τ: +0,0031 pp/jaar (gestegen 0,35 → 0,43)
- φ: −0,0104 pp/jaar (gedaald 0,80 → 0,53)
- E_tv: +0,15 pp/jaar (gestegen 29 % → ~34 %)

**Plafond VMP-Nova (referentiemodel, leverbaarheid 1,0) = 2× historisch tempo:**

| Factor | 3e orde | 2e orde (60%) | 1e orde (30%) |
|---|---:|---:|---:|
| E_tv | ±0,20 pp/j | ±0,12 pp/j | ±0,06 pp/j |
| α | ±0,010 pp/j | ±0,006 pp/j | ±0,003 pp/j |
| τ | ±0,005 pp/j | ±0,003 pp/j | ±0,002 pp/j |
| φ | ±0,015 pp/j | ±0,009 pp/j | ±0,004 pp/j |

Alle andere partijen gebruiken een fractie van deze plafonds op basis van hun politieke positie.

### Regel 120 — Politieke as: links-rechts-heuristiek

**Grondregel (gebruiker, 4 juli 2026):**
> "Links wil eerst uitgeven en dan proberen te verdienen. Rechts is conservatief, eerst verdienen voor je uitgeeft."

**Toepassing op NEPK-factoren:**

| Kant | Effect op τ | Effect op α/φ | Effect op E_tv |
|---|---|---|---|
| **Rechts** (eerst verdienen) | ↓ omlaag | ↑ omhoog (verdien-kracht) | wisselend (afhankelijk van EU/nationalisme) |
| **Links** (eerst uitgeven) | ↑ omhoog | ↓ omlaag (uitgeven erodeert verdien-kracht) | wisselend (afhankelijk van EU/internationalisme) |
| **Populistisch** | speciaal — lastenverlaging + anti-EU (E_tv omlaag) |

**Specifiek voor PRO (progressief-links):** 1e orde bijna nul, 2e en 3e orde erg negatief. Vermogens-/bedrijfsbelasting en stikstof bouwen op na eerste cyclus. DGA-emigratie versnelt na jaar 4.

**Specifiek voor VVD/JA21 (rechts-progressief):** sterker positief dan v3.12a. Actieve lastenverlaging + herlokalisatie via ondernemersklimaat.

### Regel 121 — Drie-orde-scoring alle 17 partijen (canoniek v3.12c)

**Referentiemodellen:**

| Partij | Lev | E_tv (1/2/3) | α (1/2/3) | τ (1/2/3) | φ (1/2/3) |
|---|---:|---|---|---|---|
| VMP-Nova | 1,00 | +0,06 / +0,12 / +0,20 | +0,003 / +0,006 / +0,010 | −0,002 / −0,003 / −0,005 | +0,004 / +0,009 / +0,015 |
| CARB | 1,00 | +0,03 / +0,06 / +0,10 | +0,003 / +0,006 / +0,010 | 0 / −0,001 / −0,002 | +0,002 / +0,004 / +0,008 |

**Rechts (eerst verdienen):**

| Partij | Lev | E_tv | α | τ | φ |
|---|---:|---|---|---|---|
| SGP | 0,80 | +0,02 / +0,04 / +0,06 | +0,002 / +0,004 / +0,006 | −0,001 / −0,002 / −0,003 | +0,005 / +0,010 / +0,015 |
| JA21 | 0,40 | +0,04 / +0,08 / +0,12 | +0,003 / +0,006 / +0,010 | −0,003 / −0,004 / −0,005 | +0,003 / +0,006 / +0,010 |
| VVD | 0,75 | +0,03 / +0,08 / +0,15 | +0,001 / +0,003 / +0,006 | −0,003 / −0,004 / −0,005 | 0 / −0,004 / −0,008 |
| BBB | 0,30 | +0,02 / +0,04 / +0,08 | +0,003 / +0,006 / +0,010 | −0,001 / −0,003 / −0,005 | +0,004 / +0,008 / +0,012 |
| PVV | 0,30 | −0,030 / −0,060 / −0,100 | +0,001 / +0,002 / +0,003 | −0,003 / −0,004 / −0,005 | +0,002 / +0,004 / +0,008 |
| FvD | 0,15 | −0,04 / −0,10 / −0,20 | +0,002 / +0,003 / +0,005 | −0,003 / −0,004 / −0,005 | +0,003 / +0,006 / +0,010 |

**Midden:**

| Partij | Lev | E_tv | α | τ | φ |
|---|---:|---|---|---|---|
| CDA | 0,60 | +0,02 / +0,04 / +0,06 | +0,001 / +0,003 / +0,005 | 0 / +0,001 / +0,002 | +0,003 / +0,006 / +0,010 |
| CU | 0,55 | +0,01 / +0,02 / +0,03 | 0 / +0,001 / +0,002 | +0,001 / +0,002 / +0,003 | +0,003 / +0,006 / +0,010 |
| NSC | 0,25 | +0,01 / +0,02 / +0,04 | 0 / +0,001 / +0,002 | +0,001 / +0,002 / +0,003 | +0,001 / +0,002 / +0,004 |

**Links (eerst uitgeven):**

| Partij | Lev | E_tv | α | τ | φ |
|---|---:|---|---|---|---|
| D66 | 0,35 | +0,030 / +0,050 / +0,080 | +0,001 / +0,002 / +0,003 | +0,001 / +0,002 / +0,003 | 0 / −0,003 / −0,008 |
| Volt | 0,30 | +0,04 / +0,08 / +0,15 | +0,001 / +0,002 / +0,003 | +0,001 / +0,002 / +0,003 | −0,002 / −0,004 / −0,008 |
| GL-PvdA | 0,50 | 0 / +0,02 / +0,04 | −0,001 / −0,003 / −0,006 | +0,002 / +0,003 / +0,005 | 0 / −0,001 / −0,003 |
| PRO | 0,30 | 0 / −0,05 / −0,15 | 0 / −0,005 / −0,010 | +0,001 / +0,004 / +0,005 | 0 / −0,003 / −0,010 |
| DENK | 0,25 | 0 / −0,01 / −0,02 | 0 / −0,001 / −0,002 | +0,001 / +0,003 / +0,005 | 0 / 0 / +0,001 |
| PvdD | 0,35 | −0,01 / −0,03 / −0,06 | −0,002 / −0,006 / −0,010 | +0,002 / +0,003 / +0,005 | 0 / −0,002 / −0,006 |
| SP | 0,40 | 0 / −0,03 / −0,08 | +0,003 / +0,005 / +0,008 | +0,004 / +0,005 / +0,005 | +0,002 / +0,005 / +0,010 |

### Regel 122 — Bundel-visualisatie NEPK-grafiek

Naast de NEPK/NTPK-lijnen van de gekozen partij toont de grafiek een **vergelijkingsbundel** van 8 andere partijen als dunne referentie-lijnen (opacity 0,45):

**Bundel-partijen:** VMP, CARB, VVD, JA21, BBB, D66, GL-PvdA, PVV, PRO

Elk krijgt een eigen hex-kleur die duidelijk onderscheidbaar is:
- VMP goud `#eab308` · CARB cyaan `#0891b2` · VVD blauw `#1e40af`
- JA21 turkoois `#14b8a6` · BBB groen-geel `#84cc16` · D66 groen `#84cc16`
- GL-PvdA rood `#dc2626` · PVV geel `#facc15` · PRO magenta `#ec4899`

**Labels worden vertikaal ge-stackt** met minimum 11 px verticale ruimte om overlap te voorkomen. Kleine verbindingslijnen tonen welk label bij welk eind-punt hoort. Elk label toont de partij-ID plus de eind-NEPK-waarde (bijv. "VMP 7,3 %").

De **gekozen partij** wordt getekend als dikke lijn (3,6 px) mét witte halo eronder (6,5 px), zodat de partij-lijn duidelijk boven de bundel uitkomt.

### Regel 123 — Historische baseline in grafiek

De grafiek toont naast de partij-lijn een **grijze historische baseline** (dashed) die de trend 2000-2026 doorzet zonder ombuiging:
- E_tv +0,15 pp/j · α −0,0077 pp/j · τ +0,0031 pp/j · φ −0,0104 pp/j
- Baseline zakt door 3 % rond 2028-2030 en door 2 % rond 2032-2034
- Dient als vergelijkingsanker: elke partij wordt visueel afgezet tegen "wat gebeurt zonder ombuiging".

### Regel 124 — Y-as en drempels grafiek

**Enkele Y-as in absolute % BBP** (geen dubbele-as-verwarring):
- Bereik: 0 tot 11 % BBP
- Ticks op 0, 2, 3, 4, 6, 8, 10
- Rode drempellijnen bij 3,0 % (sociaal kantelpunt) en 2,0 % (point-of-no-return)
- Kritische zone 2-3 % lichtrood; onder-2 % donkerrood gearceerd

### Regel 125 — Kleur-mapping Nederlands → hex

Partij-kleuren staan in `persona.json` als Nederlandse woorden. Deze worden in de UI vertaald naar hex-codes via de mapping:

| NL-naam | Hex |
|---|---|
| rood | #dc2626 |
| blauw | #2563eb |
| donkerblauw | #1e3a8a |
| groen | #16a34a |
| oranje | #ea580c |
| geel | #facc15 |
| goud | #ca8a04 |
| paars | #7c3aed |
| kastanje | #7f1d1d |
| turkoois | #0891b2 |
| smaragd | #059669 |
| cyaan | #06b6d4 |
| roze / magenta | #ec4899 / #d946ef |
| grijs | #64748b |

Fallback: `#7c3aed` (paars).

### Regel 126 — UI-flow: vraag-tegels blijven boven

**Layout-volgorde in `PersonaFlow`:**
1. Header (logo + reset)
2. Intro (verdwijnt na eerste antwoord)
3. **Huidige vraag met tegels** — altijd boven zolang er nog vragen zijn
4. Eigen-keuze-blok (verschijnt na eerste antwoord, ónder de vraag)
5. Levensloop-projectie + grafieken

**Reden (gebruiker, 4 juli 2026):**
> "Als ik de eerste tegel selecteer komt door het showen van de grafiek de volgende tegels pas terug als ik omhoog scrol. Dat is vervelend, ik wil de tegels steeds in beeld houden totdat de volledige keuze is gemaakt, of dat is zelf scrol."

Er wordt geen auto-scroll uitgevoerd bij het antwoorden op een vraag. Gebruiker scrolt zelf naar de grafieken indien gewenst.

### Regel 127 — Netto-gezondheid als banner, niet als lijn

De netto-gezondheid (NEPK − schuld-service − uitmergel-drift) wordt **niet meer** als aparte lijn in de grafiek getoond, maar als **banner onder de grafiek**:

> Netto-gezondheid eindjaar 2041: X,XX % BBP (= NEPK − schuld-service − uitmergel-drift)
> NEPK daalt/stijgt met Y,YY pp BBP (van 3,75 % naar Z,ZZ %)

Kleur van de waarde: rood bij < 3 %, oranje bij 3-4 %, groen bij ≥ 4 %.

**Reden:** de netto-gezondheids-lijn eindigt vaak op 0 % door uitmergel-drift, wat visueel als "alle partijen even slecht" leest terwijl de nuance in de tijdlijn zit. Banner-vorm is duidelijker.

### Regel 128 — Discrepantie-audit als vereiste

Waar mijn eigen berekening afwijkt van de brondocumenten, wordt dat in het regelbestand expliciet vermeld met beide waarden en de reden. Voorbeelden in v3.12c:

- NEPK-startwaarde: eigen 3,75 % vs documenten 4,5 % (centraal) — verschil in E_tv-definitie
- α-schatting: canonieke keuze 0,40 vs Wereldbank-industry-share (~0,175) — verschil door "productieve kern na overhead-aftrek"

**Regel:** engine gebruikt eigen berekening als canonieke waarde (strikt verifieerbaar); bandbreedte en documenten-waarde worden in `persona.json` metadata opgenomen en in de grafiek-tekst getoond.

### Regel 129 — Traagheid als systeemeigenschap

**Gebruikersuitspraak (canoniek):**
> "Alle partijen geven gewoon de vertraging die de VMP ook geeft, niets geeft een shock effect. Ombuigen kost tijd."

Consequenties in engine:
- Geen enkele 1e-orde-modulatie mag boven ±0,10 pp/j uitkomen (met leverbaarheid × plafond)
- Zelfs radicale partijen (SP, VMP-Nova) bereiken pas in de 3e orde hun maximum
- Baseline (regel 123) toont wat "geen ombuiging" doet — geen partij kan snel omkeren

### Regel 130 — Verificatie voor bouwen

**Gebruikersuitspraak (canoniek):**
> "Alles wat je bouwt moet je zelf achter staan, dus verifiëren, dan pas bouwen. Dit is de standaard regel, anders verzanden we in data die niet klopt."

Consequenties in workflow:
- Elke nieuwe factor of scoring moet vooraf onderbouwd worden met bron
- Bij discrepantie tussen bron en berekening: transparant documenteren (regel 128)
- Bij interpretatieve keuze: aan gebruiker voorleggen voor akkoord

---

## Kalibratie-audit v3.12c

### Reproductie historische tijdreeks

Toepassing van de vier-factor-formule op eigen documenten:

| Jaar | E_tv | α | τ | φ | Berekend NEPK | Doc NEPK | Δ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2000 | 29,0 | 0,60 | 0,35 | 0,80 | 9,05 % | 9,0 % | +0,05 |
| 2005 | 31,0 | 0,55 | 0,37 | 0,75 | 8,06 % | 8,1 % | −0,04 |
| 2010 | 31,5 | 0,50 | 0,39 | 0,70 | 6,73 % | 6,7 % | +0,03 |
| 2015 | 33,0 | 0,47 | 0,40 | 0,65 | 6,05 % | 6,0 % | +0,05 |
| 2020 | 32,5 | 0,42 | 0,41 | 0,58 | 4,67 % | 4,8 % | −0,13 |
| 2023 | 35,5 | 0,40 | 0,42 | 0,55 | 4,53 % | 4,9 % | −0,37 |
| 2026 | 31,0 | 0,40 | 0,43 | 0,53 | 3,75 % | 4,5 % | −0,75 |

Discrepantie 2023-2026 komt door strikt doorvoer-eruit in E_tv.

### Verwachte NEPK 2041 (15 jaar) per partij

| Partij | Lev | NEPK 2041 | NTPK 2041 | Onder 3% grens? |
|---|---:|---:|---:|---|
| VMP-Nova | 1,00 | 7,32 % | 10,57 % | nee — sterk herstel |
| VMP-partij | 0,60 | 5,69 % | 9,08 % | nee — herstel |
| SGP | 0,80 | ~4,7 % | ~8,0 % | nee — solide+ |
| CARB | 1,00 | ~4,5 % | ~8,5 % | nee — solide |
| JA21 | 0,40 | ~4,3 % | ~7,5 % | nee — licht positief |
| BBB | 0,30 | 4,19 % | 7,49 % | nee — licht positief |
| VVD | 0,75 | ~4,2 % | ~7,1 % | nee — licht positief |
| CDA | 0,60 | 4,16 % | 7,30 % | nee — stabiel |
| CU | 0,55 | ~3,8 % | ~7,0 % | nee — stabiel |
| Volt | 0,30 | ~3,8 % | ~7,2 % | nee — stabiel |
| D66 | 0,35 | 3,66 % | 7,22 % | nee — vlak |
| PVV | 0,30 | ~3,7 % | ~7,1 % | nee — vlak |
| NSC | 0,25 | ~3,7 % | ~7,1 % | nee — vlak |
| DENK | 0,25 | ~3,6 % | ~7,0 % | nee — vlak |
| SP | 0,40 | ~3,4 % | ~7,1 % | nee — licht dalen |
| GL-PvdA | 0,50 | ~3,3 % | ~6,5 % | nee — dalen |
| FvD | 0,15 | ~3,1 % | ~6,9 % | nee — dalen |
| **PRO** | 0,30 | **~2,9 %** | ~6,3 % | **JA — kantelpunt** |
| PvdD | 0,35 | ~2,9 % | ~6,2 % | JA — kantelpunt |

**Baseline (geen ombuiging):** ~1,85 % BBP — ver onder point-of-no-return na 15 jaar.

---

## Bronnen v3.12c

**Nova Democratia / VMP-documenten (canoniek):**
- [nepk-indicator-methodologie.pdf](https://novademocratia.com/assets/docs/nepk-indicator-methodologie.pdf) — formule + factordefinities
- [de-nederlandse-ondergang.pdf](https://novademocratia.com/assets/docs/de-nederlandse-ondergang.pdf) — historische tijdreeks 2000-2026
- [nepk-evaluatie-nederland-2024-2026.pdf](https://novademocratia.com/assets/docs/nepk-evaluatie-nederland-2024-2026.pdf) — internationale benchmark
- [vmp-partijprogramma-2026.pdf](https://novademocratia.com/assets/docs/vmp-partijprogramma-2026.pdf) — 16 beleidsterreinen
- [vmp-eenssysteem-belasting.pdf](https://novademocratia.com/assets/docs/vmp-eenssysteem-belasting.pdf) — één-belastingstelsel
- [vmp-arbeid-belasting-verhulde-onttrekking.pdf](https://novademocratia.com/assets/docs/vmp-arbeid-belasting-verhulde-onttrekking.pdf) — tax wedge

**Externe data (verifieerbaar):**
- [CBS DTFF 2024](https://longreads.cbs.nl/dutch-trade-in-facts-and-figures-2024/dutch-earnings-from-exports/) — export-VA % BBP
- [CBS StatLine 85821ENG](https://www.cbs.nl/en-gb/figures/detail/85821ENG) — foreign-controlled VA
- [OECD Revenue Statistics NL](https://www.oecd.org/tax/revenue-statistics.htm) — belastingdruk
- [Wereldbank](https://data.worldbank.org/indicator/NV.IND.MANF.ZS?locations=NL) — industry share

### Regel 131 — Land-specifieke persona.json lokalisatie

Wanneer een app naar een ander land wordt geport (NL → DE, MT, ...), moeten **alle Q1-Q7 vragen en antwoorden in `gevolgenkaart-persona.json`** land-specifiek zijn:
- **Q1_sector**: 22 sectoren die de matrix-structuur behouden, maar labels + delta_gewichten aangepast aan de land-economie (bv. Malta voegt iGaming, financial services, shipping toe).
- **Q2_wonen**: hypotheek-/huurregels van dat land (NL: box3+hypotheekrenteaftrek; MT: first-time-buyer scheme; DE: Wohngeld+Mietpreisbremse).
- **Q3_gezin**: universele opties (single/couple/family/single-parent) blijven, maar delta_gewichten context-afhankelijk.
- **Q4_leeftijd**: pensioenleeftijd-drempels per land (NL: 67; MT: 65-67; DE: 67).
- **Q5_regio**: **verplicht opnieuw opgesteld** — regio-namen 1:1 van dat land (NL: Randstad/krimpregio; MT: Valletta/Sliema/Gozo; DE: Bundesländer-clusters).
- **Q6_bedrijfslaag** en **Q7_netwerk**: verplicht land-context. NL heeft "boer met stikstof-zone"; Malta heeft "multinational-hub / interconnector-afhankelijk"; DE heeft "Mittelstand / Energie-Transformation".

**Bronvereiste**: elke sector/regio/bedrijfslaag komt uit primaire bronnen van dat land (NSO/Destatis/CBS + Eurostat + land-specifieke wetgeving). Geen "vertaling van NL" mag blijven staan.

### Regel 132 — Geen conditionele Q6/Q7 op Q1

De oude NL-flow had `conditioneel_op_Q1` voor Q6 en Q7 (alleen tonen bij bepaalde sectoren). Dit **breekt** bij portering naar andere landen omdat de sector-lijst verschilt. Nieuwe regel:
- Q6 en Q7 zijn **altijd verplicht getoond**, met een expliciete "n.v.t."-optie als antwoord voor gebruikers zonder relevant profiel.
- Alternatief: als een land specifieke conditionaliteit wil, moet dat in dat land's persona.json apart worden gedefinieerd — niet gehardcodeerd in de PersonaFlow.tsx-component.

### Regel 133 — Land-portering: checklist voor werkende app

Bij het bouwen van een land-versie (NL → DE, MT, ...), moet **elk van deze zaken land-specifiek zijn**:
1. **Startwaarden vier factoren** (E_tv, α, τ, φ) uit primaire bronnen van dat land — subagent-onderzoek verplicht.
2. **Partijen** (aantal, namen, kleuren, cluster, leverbaarheid) uit dat land's politieke landschap.
3. **Partij-posities matrix** (N partijen × 183 elementen) via Optie Y (per partij programma-analyse).
4. **Q1-Q7 vragen en antwoorden** — Regel 131.
5. **UI-teksten** in de nationale/EU-taal van dat land (Engels als 2e taal vaak acceptabel voor kleine landen zoals Malta).
6. **Grafiek Y-as** aangepast aan NEPK/NTPK-schaal van dat land (NL: 0-11%; DE: 0-12%; MT: 0-14%).
7. **Bundel-kleuren** aangepast aan partij-kleuren van dat land.
8. **Cache-versie** in service worker uniek per land (bv. `gk-mt-v3.12b`).
9. **URL-slot** in openvizier-repo: `/de/wahlfolgen-app/`, `/mt/wahlfolgen-app/`, etc.
10. **Regel 87**: cellen zonder bron blijven op positie=0, intensiteit=0. Geen verzonnen scores.

**Verificatie voor deployment (Regel 130 herbevestigd voor portering):**
- Persona-flow doorloopt Q1 t/m Q7 zonder stalling (browser-test verplicht).
- Tweede grafiek (NEPK/NTPK) rendert voor elke partij zonder runtime-error.
- Alle partijen zijn zichtbaar in de partij-keuze-knoppen bovenin.
- Cijfers in de intro-alinea onder de kop komen overeen met `nepk_tijdreeks.factoren` startwaarden.

### Regel 134 — Exacte NEPK-definitie & empirische engine-ankers (v3.12f)

**Aanleiding:** In v3.12e zaten twee kalibratie-parameters (`nepkDriftIndex^0.4` voor koopkracht-koppeling en `v/50000` voor partij-cascade) die niet aan externe bronnen te herleiden waren — zuivere curve-fitting om de grafiek plausibel te maken. Volgens de grondregel *"verifieren, dan pas bouwen"* is dat onaanvaardbaar. Regel 134 legt de exacte NEPK-definitie én de empirische engine-parameters vast met bronnen.

#### 134.1 — Exacte NEPK-definitie (canoniek)

**NEPK = Netto Externe Productieve Kern.** Definitie is niet gelijk aan enige standaard tax-to-GDP-maat (OECD, Eurostat, IMF). NEPK meet het aandeel van het BBP dat door de nationaal-productieve kern **na overhead- en fiscale-drukverlies** wordt geleverd én in nationale handen blijft. Formule:

$$\text{NEPK}\% = E_{tv} \times \alpha \times (1-\tau) \times \varphi$$

Met:
- **E_tv** = exportgedreven toegevoegde waarde (% BBP, doorvoer eruit)
- **α** = productieve-kern-fractie na overhead-aftrek
- **τ** = effectieve netto-belastingdruk op productieve activiteit (0-1)
- **φ** = aandeel in nationale handen (na buitenlands eigendom eruit)

**Waarom NEPK ≠ tax-to-GDP:** OECD tax-to-GDP telt álle belastingen (btw, inkomsten, sociale premies) op álle activiteit (inclusief transferconsumptie, publieke sector, buitenlands-gecontroleerde bedrijven). NEPK isoleert de nationaal-productieve waardestroom en meet de nettodruk daarop. NL-NEPK 2026 = 3,75 % (eigen berekening) vs NL tax-to-GDP ≈ 39 % (OECD) — meten fundamenteel iets anders.

**Startwaarden 2026 per land (definitie-parameters, canoniek vastgelegd):**
- **NL:** NEPK = 3,75 % BBP (E_tv=31,0 % · α=0,40 · τ=0,43 · φ=0,53)
- **DE:** NEPK = 6,83 % BIP (E_tv=31,6 % · α=0,45 · τ=0,414 · φ=0,82)
- **MT:** NEPK = 4,40 % BIP (E_tv=46,3 % · α=0,30 · τ=0,297 · φ=0,45; hub-economie)

Deze startwaarden zijn engine-interne definities die niet aan externe standaardmaten worden gekoppeld. Ze zijn intern consistent (zelfde formule voor alle drie landen), maar niet extern verifieerbaar.

#### 134.2 — Empirisch onderbouwde engine-parameters

De volgende engine-constanten hebben minimaal twee onafhankelijke bronnen en zijn vanaf v3.12f canoniek:

**A. NEPK → koopkracht-koppeling (β):**
- **Coëfficiënt:** −1,25 % reëel beschikbaar inkomen per procentpunt-BIP NEPK-stijging (jaar 1, mechanisch)
- **Toepassing:** lineair, NIET exponentieel; `koopkracht_index(t) = 100 × (1 − 0,0125 × ΔNEPK_pp × lag_tax(t))`
- **Bronnen:** [DIW Berlin Economic Bulletin 31+32.2017](https://www.diw.de/documents/publikationen/73/diw_01.c.562950.de/diw_econ_bull_2017-31-1.pdf) (β=1,26 en 1,44 in twee sub-metingen); [Ramey 2019, JEP](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) (tax-multiplier −2 tot −3 cumulatief)

**B. Fiscale multipliers per beleidscategorie:**

| Categorie | Multiplier (impact → long-run) | Empirische status |
|---|---|---|
| Belastingverlaging | −0,25 → −2,0 | Onderbouwd — [IMF TNM/14/04](https://www.imf.org/external/pubs/ft/tnm/2014/tnm1404.pdf), [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) |
| Groen-investeren | 0,5 → 1,5 | Onderbouwd — [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf), [Ilzetzki/Mendoza/Végh 2013](https://www.nber.org/system/files/working_papers/w16479/revisions/w16479.rev1.pdf) |
| Sociaal-transfer (permanent) | 0,6 | Onderbouwd — [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) |
| Sociaal-transfer (tijdelijk) | ~0 | Onderbouwd — [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) |
| Bestedingen benchmark | 0,75 (j1); 0,6-1,0 (cum.) | Onderbouwd — [IMF TNM/14/04](https://www.imf.org/external/pubs/ft/tnm/2014/tnm1404.pdf), [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) |
| **EU-integratie** | **RESERVE — model-tuning-parameter** | Geen fiscale-multiplier-literatuur beschikbaar |
| **Deregulering** | **RESERVE — model-tuning-parameter** | Geen fiscale-schok, geen multiplier-literatuur |

**C. Policy-lag profielen (jaar 1 / 3 / 5 als % van eindeffect):**
- **Bestedingen (snel):** j1=0,80 / j3=0,95 / j5=1,00 — [IMF WP 12/286](https://www.imf.org/-/media/Websites/IMF/imported-full-text-pdf/external/pubs/ft/wp/2012/_wp12286.ashx), [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf)
- **Belasting (traag, dieper):** j1=0,40 / j3=0,85 / j5=1,00 — [Alesina/Favero/Giavazzi 2019](https://didattica.unibocconi.it/mypage/upload/48917_20190504_114457_JEP.33.2.141.PDF), [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf)

#### 134.3 — Gereserveerde tuning-parameters

Twee categorieën in de partij-matrix hebben géén empirische multiplier-literatuur en worden **expliciet gereserveerd als model-tuning-parameters**:

1. **EU-integratie** — effect van meer/minder EU-supranationaal beleid op nationale NEPK. Geen fiscale-multiplier-studies beschikbaar.
2. **Deregulering** — regelverlichting is geen fiscale schok en heeft geen bijbehorende multiplier-literatuur. Effecten op productiviteit zijn hoog-omstreden en niet empirisch stabiel.

**Behandeling in code:** deze twee categorieën gebruiken een tuning-multiplier van 0,3 als default (conservatief, subeenheids) met expliciete comment `MODEL_TUNING — geen empirische basis`. Ze mogen niet als "onderbouwd" worden gepresenteerd in UI-tooltips of documentatie.

#### 134.4 — Macro-context DE 2026 (correcties op v3.12e)

- **BIP-groei 2026:** 0,6 % kalendergecorrigeerd (was: 0-0,5 %) — [Bundesbank Forecast dec-2025](https://www.bundesbank.de/en/press/press-releases/bundesbank-s-forecast-for-germany-economy-will-gradually-recover-965032), [EU-Commissie DE](https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/germany/economic-forecast-germany_en)
- **Industrie-ontslagen:** 266.000-342.000 cumulatief sinds 2019 (was: 500.000+, overschat) — [dpa/EY 2026](https://www.reuters.com/business/german-industry-keeps-cutting-jobs-despite-first-sales-rise-three-years-ey-says-2026-05-25/)
- **HICP-inflatie 2026:** 2,2 %; overheidstekort 3,7 % BIP — Bundesbank + EU-Commissie

#### 134.5 — Macro-context MT 2026 (bevestigd)

- **Pillar 2 (15 % min. effectief tarief):** uitgesteld tot eind-2029; potentieel +2 % BIP fiscale opbrengst — [IMF Malta 2025 Article IV](https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf)
- **CBI-einde:** ECJ-arrest 29 apr 2025, programma beëindigd — [Reuters](https://www.reuters.com/world/europe/eu-top-court-rules-against-maltas-golden-passport-scheme-2025-04-29/)
- **AMLA iGaming:** operationeel jan-2026, opex +8-15 % — [MGA/AMLA consultaties](https://sccgmanagement.com/sccg-news/2026/3/3/mga-calls-on-licensees-to-engage-in-eu-aml-consultations/)
- **BIP-groei 2026:** ~4 % (EU-topper); tekort 3,2 %; schuld ~47 % BIP — IMF Article IV

#### 134.6 — Verwijzing bron-document

Volledig onderbouwingsrapport: `/home/user/workspace/engine_parameters_empirisch_v3.12.md` — bevat bron-quotes, tijdshorizons en overwegingen voor elke parameter.

**Wat mag NIET meer in code:**
- `nepkDriftIndex^0.4` of vergelijkbare verzonnen exponent voor koopkracht-koppeling (VERBODEN — vervang door lineaire β=−1,25 %/pp)
- `v/50000`, `v/5000` of andere ongeoorloofde schaal-cascade (VERBODEN — vervang door multiplier × lag-profiel)
- Elke andere "kalibratie op ooggevoel" zonder bron-comment in de code

**Wat MOET in code-comment bij elke engine-constante:**
```
// EMPIRISCHE ANKER: <parameter> = <waarde>
// Bron: <URL>
// Aard: [ONDERBOUWD | MODEL_TUNING | DEFINITIE_PARAMETER]
```

---

### Regel 135 — Zwitserse (CH) app-portering (v3.13)

De CH-app is de derde land-versie, met Duits als hoofdtaal (naast DE).

**Canonieke matrix-slot:** cluster `x.1.3.1.3.5` in `nl/_data/vizier.xlsx`:
- NL rij 1125, ID `1.1.3.1.3.5`, "De Zwitserse Folgenkarte"
- DE rij 1126, ID `2.1.3.1.3.5`, "Die Schweizer Folgenkarte"
- EN rij 1127, ID `3.1.3.1.3.5`, "The Swiss Consequence Map"

**URL-slot:** `/de-CH/folgenkarte-app/` (BCP-47 `de-CH` onderscheidt CH-Duits van DE-Duits).

**Verplichte matrix-kolommen bij toevoegen van een nieuwe app-rij** (v3.13d correctie op v3.13a-bug):
- Kolom 2 (`Code`), 3 (`Ouder`), 4 (`Taal`), 5 (`Type=artikel`), 6 (`Naam`), 7 (`Ondertitel`), 8 (`Beschrijving`), 9 (`URL`), 10 (`Hero`)
- **én verplicht:** kolom 18 (`Status='live'`), 19 (`Volgorde='<n>'`), 20 (`Actief=True`)
- Ontbrekende status/actief → rij wordt door `xlsx_naar_json.py` **overgeslagen** en verschijnt niet in het menu.

**Menu-integratie (HTML-landing-pagina's):** de statische pagina's `nl/stemgedrag.html`, `de/wahlfolgen.html`, `en/vote-impact.html` bevatten één `apps-grid` div waar de landsknoppen staan. Nieuwe apps toevoegen aan alle drie pagina's is verplicht — anders is de app niet vindbaar vanuit de andere taal-menu's, ondanks matrix-registratie.

**CH-startwaarden 2026:** zie Regel 134 + `/home/user/workspace/CH_startwaarden_v312.md` (SECO TiVA, BFS, OECD, admin.ch, KOF).

**9 CH-partijen:** SVP, SP, Mitte, FDP, Grüne, GLP, EVP, EDU, Lega + VMP/CARB referentie.

**7 CH-Grossregionen:** Zürich, Espace Mittelland, Genfersee, Nordwest, Ostschweiz, Zentralschweiz, Tessin.

**22 CH-sectoren met land-specifieke aanpassingen:** S13 = Pharma & Life Sciences (i.p.v. iGaming/MT), S17 = Präzisionsindustrie/Uhrenindustrie (i.p.v. Shipping/MT).

---

### Regel 136 — Meertalige sector-mapping in SectorIcons.tsx (v3.13)

`SectorIcons.tsx` (SVG-iconen) en `MiniHero.tsx` (emoji-fallbacks) MOETEN **één meertalige sleutel-set bevatten** die alle land-varianten dekt. Ontbrekende sleutels leiden tot lege 150×150-tegels (bug uit MT v3.12k) of witte-pagina-crashes (getClusterStyle undefined).

**Canoniek sleutel-schema:**
- NL: `S1_zorg`, `S2_onderwijs`, ..., `S22_student`
- DE: `S1_gesundheit`, `S5_automotive`, `S13_chemie_pharma`, `S17_maschinenbau`, ..., `S22_rentner_student`
- MT: `S1_health`, `S13_igaming`, `S17_shipping_maritime`, ..., `S22_not_employed_student_retired`
- CH: `S1_gesundheit`, `S13_pharma`, `S17_uhrenindustrie`, ..., `S22_nicht_aktiv`

**Verplicht per portering:**
1. Voeg alle 22 sleutels toe aan `SECTOR_ICONS` én `SECTOR_CLUSTERS` in `SectorIcons.tsx`
2. Voeg alle Q2-Q7 antwoord-sleutels toe aan `iconVoorAntwoord` map in `MiniHero.tsx`
3. Zorg dat `getVraagLabel` op het juiste veldnaam-veld leest (`vraag` in NL/CH/DE, gebruik consistent één veldnaam)
4. **Nooit oude land-sleutels verwijderen** — alleen toevoegen, zodat gedeelde componenten multi-land werken.

---

### Regel 137 — Pre-deploy checks (v3.13)

Elke build voor productie MOET voor deploy deze checks doorlopen. Ontstaan uit v3.12k MT-crash (`nepkParty is not defined` — 5 typo's die de app hard lieten crashen bij eerste klik) én v3.13a CH-uitkomsten-nul-bug (leeg `partij_posities`).

**Verplicht vóór elke deploy:**

1. **TypeScript-lint:** `npx tsc --noEmit -p .` in de app-map. **Onbekende identifiers zoals `nepkParty`, `uitlegParty`, `iconVoorQuestion`, `start_party_advies`, `actieveParty`, `gekozenParty` mogen niet in errors verschijnen** — dat zijn refactor-typo's die runtime-crashes veroorzaken. Andere TS-warnings mogen doorheen; die blokkeren de Vite-build niet.
2. **Build-test:** `npm run build` moet slagen.
3. **Grep-check onvertaalde inhoud:** grep het `dist/public/index.html` voor niet-passende taal-tokens (bv. Nederlandse tekst in Malta-app, Malta-partijnamen in CH-app).
4. **Numeriek-consistentie:** aantal partijen en elementen in de UI-badge/intro-tekst moet overeenkomen met `gevolgenkaart-persona.json`.
5. **Data-dekkingscheck (Regel 138.2 verplicht):** run dit script en fail-fast bij assertion-fout:
   ```python
   import json, sys
   p = json.load(open('<APP>/client/src/data/gevolgenkaart-persona.json'))
   echte = [k for k, v in p['partijen'].items() if not v.get('referentie')]
   errors = []
   for partij in echte:
       pos = p['partij_posities'].get(partij, {})
       nz = sum(1 for eid, v in pos.items()
                if v.get('positie', 0) != 0 or v.get('intensiteit', 0) != 0)
       if nz < 146:  # 80% van 183
           errors.append(f"{partij}: slechts {nz}/183 posities gescoord")
   if errors:
       print('DATA-DEKKING-FOUT:'); [print('  '+e) for e in errors]; sys.exit(1)
   print(f'OK: alle {len(echte)} echte partijen ≥ 80% dekking')
   ```
6. **Browser-test na deploy:** minstens één hard-refresh + één antwoord-klik in de production-URL vanuit een cloud- of local-browser, checken op witte pagina en console-fouten.
7. **Cascade-verschil-check (Regel 138.4):** vergelijk twee tegenpartijen met identieke persona-antwoorden. Eerste-orde-scores moeten ≥ 30 punten verschillen. Zo niet: deploy stopzetten en Regel 138 opnieuw doorlopen.

**Nooit deployen zonder deze checks.** "Verifieer uitvoering + gevolg + gevolg van gevolg" begint bij het niet-crashen én bij niet-nul-scoren van de app.

---

### Regel 138 — Partij_posities: geen leeg-vulling, altijd 100% dekking (v3.13d)

**Aanleiding:** In CH v3.13a stond de heuristiek: "vul partij_posities per element als het `domein`- of `cat`-veld een van deze programma-zoektermen bevat (bijv. `migration`, `klima`, `landwirtschaft`)." Maar het `domein`-veld bevat **codes** (`D1` t/m `D14`), geen tekst. Resultaat: ~0 matches, ~alle 183 posities bleven (0,0), cascade-scores werden bijna nul, uitkomsten leken "neutraal". Dat is een stille faalmodus die geen crash geeft maar wel de hele app zinloos maakt. Regel 138 sluit deze bugklasse uit.

#### 138.1 — Dekkingseis 100 %

**Elke `partij_posities`-tabel MOET voor iedere echte partij** (dus exclusief referentiemodellen VMP/CARB, die eigen scoring hebben) **alle 183 elementen expliciet scoren.**

- Ieder element krijgt `{positie: X, intensiteit: Y}` met `X ∈ [-2, -1, 0, 1, 2]` en `Y ∈ [0..10]`.
- **`positie = 0` én `intensiteit = 0` samen is verboden** voor een echte partij, tenzij een expliciete `reden`-veld staat als `"Bewusst neutral, kein Programmpunkt"` (of taal-equivalent) én dit voor **maximaal 20 %** (37 van 183) van de elementen geldt.
- **Coalitie-vulling** (Regel 108) blijft de terugval bij oprechte 0-scores. Coalitie-vulling mag echter niet worden gebruikt als excuus om een partij lege posities te geven — die vulling is er voor incidentele gaten, niet voor structureel ontbrekende scoring.

#### 138.2 — Score-methode per portering (verplicht in deze volgorde)

1. **Domein-basis (14 domeinen, D1–D14):** ken per partij per domein een `(positie, intensiteit)`-paar toe, gebaseerd op de door onderzoek onderbouwde partij-profielen uit `<LAND>_startwaarden_v312.md` Vraag 3. Dit vult direct alle 183 elementen die tot dat domein behoren.
2. **Element-overrides:** voor de 5-15 elementen per partij die duidelijk afwijken van het domein-gemiddelde (kern-standpunten, kern-tegenstellingen), zet expliciet een override op de element-ID. Documenteer met `reden`-veld.
3. **Verificatie-script (verplicht vóór build):**
   ```python
   for partij in echte_partijen:
       nz = sum(1 for eid, v in partij_posities[partij].items()
                if v.get('positie', 0) != 0 or v.get('intensiteit', 0) != 0)
       assert nz >= 146, f"{partij}: slechts {nz}/183 posities gescoord (< 80 % dekking)"
   ```
   **Faalt de assertion, deploy niet.** Terug naar stap 1.

#### 138.3 — Expliciete instructies aan de subagent die partij_posities genereert

Wanneer een subagent wordt ingezet om `partij_posities` te genereren voor een nieuwe portering, **moet de opdracht letterlijk deze zes eisen bevatten** (kopieerbare template):

> **Opdracht partij_posities-generator (v3.13d canoniek):**
>
> 1. Lees `/home/user/workspace/<LAND>_startwaarden_v312.md` Vraag 3 voor de partij-profielen.
> 2. Voor elke echte partij (geen VMP/CARB) MOET je een `(positie, intensiteit)`-paar toewijzen aan **ELK van de 183 elementen**. Positie ∈ [-2,-1,0,1,2], intensiteit ∈ [0..10].
> 3. Gebruik domein-brede toewijzing (D1..D14) als basis, met element-overrides voor kern-standpunten. Domein afleiden uit `element.id.split('.')[0]`, **NIET** uit het `domein`-tekstveld (dat bevat codes, geen woorden).
> 4. Verboden: matching op `element.domein` als string-zoekactie (bv. `"migration" in element['domein']`). Het veld is `D11`, niet `Migration`. Match altijd op `element.naam` als je op tekst wilt zoeken.
> 5. Referentiemodellen (VMP, CARB) krijgen `"referentie": true` in `partijen`-meta. Hun `partij_posities` mogen uit een NL-referentie worden overgenomen.
> 6. **Verificatie na afloop:** voor elke echte partij `sum(pos!=0 or intens!=0) >= 146` (80 % dekking). Rapporteer dit getal per partij. Als het niet wordt gehaald, ga terug naar stap 2.

#### 138.4 — Zichtbaar-in-UI-check (waarom stille faalmodus juist gevaarlijk was)

`besteVoor()` in `levensloopEngine.ts` neemt de best-scorende échte partij uit de Ranglijst. Bij (0,0)-posities scoren álle partijen ~0 in de cascade, wat *lijkt* op "neutrale uitkomst" maar in werkelijkheid "engine heeft niets om mee te rekenen" is. **Verplicht post-deploy sanity check:**

1. Kies twee tegenpartijen (bv. SVP en SP voor CH; CDU/CSU en SP voor DE; PL en PN voor MT).
2. Ga door de app met identieke persona-antwoorden.
3. Kies eenmaal partij A als eigen keuze, dan partij B.
4. **Eerste-orde-scores moeten verschillen met minstens 30 punten** (op de gebruikte schaal). Als de scores binnen 5 punten van elkaar liggen: cascade werkt niet, deploy stopzetten en 138.1/138.2 opnieuw doorlopen.

#### 138.5 — Herbouw wanneer element-namen wijzigen

Als de 183 element-namen worden vertaald (zoals in v3.13 voor DE/MT/CH gebeurde), **hoeft `partij_posities` NIET herzien te worden** — die is gekoppeld aan `element.id` en niet aan de tekst. Element-namen zijn UI-labels; posities zijn semantische scoring op element-ID. Deze scheiding is expliciet: **niet vertalen = niet raken**.

---

## TODO's v3.14 (open)

- CH `partij_posities` verfijnen via Optie-Y-programma-analyse (nu heuristiek uit Regel 135.5)
- DE `SectorIcons.tsx` porteren naar DE-sleutels (nu nog NL-sleutels ondanks Duitse UI)
- Cascade-rekenmotor voor DE + MT + CH (analoog aan NL `gevolgenkaart.json`)
- Fine-tuning per partij op basis van gebruiker-feedback
- Regelbestand-DOCX genereren
- Unieke kleuren per partij (nu delen VVD/PVV/CU allemaal "blauw")
- Uitmergel-drift kalibratie herbekijken (nu resulteert in netto = 0)
- Extra grafiek: absoluut BBP-index vs NEPK-index (bijkomend leerpunt)

---

*Einde regelbestand v3.13. Alles wat vanaf nu wordt gebouwd, volgt deze regels.*
