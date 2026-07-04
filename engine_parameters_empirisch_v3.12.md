# Empirische ankers voor de simulatie-engine "Het Open Vizier" (Vote Impact)
### Verdedigbare parameters voor NEPK → koopkracht, fiscale multipliers, policy-lags en macro-context DE/MT

**Versie:** v3.12 — **Opgesteld:** 4 juli 2026
**Reikwijdte:** Vijf onderzoeksvragen. Elke waarde is voorzien van een exacte bron-URL (markdown-link). Waar een waarde niet uit een gefetchte bron te bevestigen was, staat "n.a." of een expliciete markering "onvoldoende empirische basis — model-tuning parameter".

> **Methodische kanttekening vooraf.** De term **NEPK ("netto-belastingdruk in % BIP")** is een intern engine-begrip van Het Open Vizier; de publicatie zelf definieert de term niet op de gefetchte pagina ([Het Open Vizier — "The matrix of the exodus"](https://openvizier.org/en/what-surfaces/the-matrix-of-the-exodus)). De startwaarden 6,83% (DE) en 4,40% (MT) komen **niet** overeen met standaard tax-to-GDP-ratio's (DE ≈ 38%, MT overall tax burden ≈ 29%). Ze lijken een enger gedefinieerde "netto"-maatstaf (bijv. belasting minus transfers, of een specifieke deelheffing). Dit heeft directe gevolgen voor de interpretatie van Vraag 1 en Vraag 4/5 — zie de betreffende secties.

---

## VRAAG 1 — NEPK → koopkracht-/beschikbaar-inkomen-elasticiteit

**Scenario in de engine:** NEPK Duitsland stijgt van 6,83% BIP naar 10% BIP (relatieve stijging ~46%, absoluut +3,17 procentpunt BIP) over 5 jaar. Wat is het verwachte %-effect op reëel beschikbaar huishoudinkomen?

### Centrale bevinding

De sterkste directe, causale, land-specifieke (Duitsland) meting van "1 procentpunt-BIP belastingverschuiving → % beschikbaar inkomen" komt uit DIW Berlin. Die geeft een **mechanische, eerste-orde doorwerking van ongeveer 1,1–1,3% netto-inkomen per procentpunt-BIP belasting.**

| Anker | Bron-waarde | Impliciete elasticiteit |
|---|---|---|
| DIW: BTW-standaardtarief −1pp = −0,34% BIP belastingopbrengst → **+0,43% netto huishoudinkomen** | [DIW Economic Bulletin 31+32.2017, tabel 3](https://www.diw.de/documents/publikationen/73/diw_01.c.562950.de/diw_econ_bull_2017-31-1.pdf) | 0,43 / 0,34 ≈ **1,26% netto-inkomen per pp-BIP** |
| DIW: verlaagd tarief −2pp = −0,16% BIP → +0,23% netto-inkomen | [DIW Economic Bulletin 31+32.2017](https://www.diw.de/documents/publikationen/73/diw_01.c.562950.de/diw_econ_bull_2017-31-1.pdf) | 0,23 / 0,16 ≈ **1,44% netto-inkomen per pp-BIP** |

Dit is de **mechanische (impact) doorwerking** — vóór gedragseffecten en macro-terugkoppeling. De 5-jaars macro-doorwerking is groter, omdat een belastingverhoging óók via de tax-multiplier het BIP (en dus het inkomen) verlaagt (zie Vraag 2).

### Puntschatting voor de engine

- **1 procentpunt-BIP NEPK-stijging → circa −1,25% reëel beschikbaar inkomen (mechanisch, korte termijn).**
- Toegepast op het scenario (+3,17 pp BIP): mechanisch ≈ **−4,0% reëel beschikbaar inkomen** op korte termijn.
- **Voeg de indirecte macro-route toe** (via tax-multiplier, Vraag 2): een narratieve tax-multiplier van −2 tot −3 (Ramey) impliceert dat +3,17pp-BIP belasting het BIP over enkele jaren met ~6–9% zou drukken; het beschikbaar-inkomen-effect ligt tussen de mechanische −4% en een pessimistische macro-uitkomst. **Centrale 5-jaars schatting: −5% tot −7% reëel beschikbaar inkomen; range −4% (alleen mechanisch, low) tot −9% (high, macro + tax-multiplier).**

### Range (low / centraal / high)

| Horizon | Low | Centraal | High | Redenering / bron |
|---|---|---|---|---|
| 1 jaar (impact) | −1,0% per pp | −1,25% per pp | −1,45% per pp | [DIW 2017](https://www.diw.de/documents/publikationen/73/diw_01.c.562950.de/diw_econ_bull_2017-31-1.pdf) mechanisch |
| 5 jaar (incl. macro) | −4% (scenario, mechanisch) | −5,5% (scenario) | −9% (scenario, tax-multiplier −3) | Combinatie [DIW](https://www.diw.de/documents/publikationen/73/diw_01.c.562950.de/diw_econ_bull_2017-31-1.pdf) + [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) |

### Bron-tabel

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| DIW Berlin Economic Bulletin 31+32.2017 | https://www.diw.de/documents/publikationen/73/diw_01.c.562950.de/diw_econ_bull_2017-31-1.pdf | 2017 | "Lowering the regular rate of the value-added tax by one percentage point would relieve private households by 0.43 percent of net income, on average." (−0,34% BIP) |
| OECD Revenue Statistics 2024 — Germany | https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/global-tax-revenues/revenue-statistics-germany.pdf | 2024 | "the tax-to-GDP ratio in Germany decreased … to 38.1% in 2023" (context: totale belastingdruk, niet "NEPK") |
| Ramey (2019), JEP | https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf | 2019 | Tax rate change multipliers "vary between –2 and –3" (indirecte inkomensroute) |

### Aanbeveling engine-code

- Gebruik voor de **directe koopkracht-koppeling** een lineaire coëfficiënt van **β ≈ 1,25% beschikbaar-inkomensdaling per procentpunt-BIP NEPK-stijging** (mechanisch, jaar 1). Bron-anker: DIW 2017.
- Voor de **5-jaars/cumulatieve koopkracht-index**: hanteer een exponent/multiplier die de tax-multiplier (−2 tot −3, Ramey) meeweegt. Praktisch: `koopkracht_index_Δ ≈ −(1,25 × ΔNEPK_pp) − (tax_multiplier_effect × aandeel_belasting_in_inkomen)`.
- **Waarschuwing:** de DIW-elasticiteit is een *distributiegemiddelde voor BTW*. Voor een brede NEPK-verschuiving (incl. directe belastingen) is de spreiding groter. Markeer de koppeling als **plausibel maar geen exacte 1-op-1-elasticiteit** — kalibreer op de range −1,0 tot −1,45% per pp.

---

## VRAAG 2 — Fiscale multipliers per beleidstype

**Doel:** Empirisch geschatte fiscale multipliers per engine-categorie (belastingverlaging, groen-investeren, sociaal-transfer, EU-integratie, deregulering) voor Duitsland/eurozone.

### Centrale waarden per categorie

| Engine-categorie | Best-passende multiplier | Range (low–high) | Horizon | Primaire bron |
|---|---|---|---|---|
| **Belastingverlaging (tax cut)** | **~0,25 (impact, AE); narratief piek −2 tot −3** | 0,25 (impact) → 2–3 (narratief, cumulatief) | Impact laag, bouwt op in ~18 mnd | [IMF TNM/14/04](https://www.imf.org/external/pubs/ft/tnm/2014/tnm1404.pdf); [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) |
| **Groen-investeren (publieke investering/infra)** | **~0,4 (short-run) → 1,5–1,6 (long-run)** | 0,4–1,6 | Bouwt op over meerdere jaren | [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf); [Ilzetzki/Mendoza/Végh 2013](https://www.nber.org/system/files/working_papers/w16479/revisions/w16479.rev1.pdf) |
| **Sociaal-transfer** | **~0,5–1,0 (permanent); ~0 (tijdelijk)** | 0 (tijdelijk) – 1,0 (permanent) | Kort; verdwijnt snel | [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) |
| **Algemene overheidsbestedingen (benchmark)** | **~0,75 (jaar 1, AE); 0,6–1,0 cumulatief** | 0,6–1,0 | Cumulatief stabiel tot 5 jaar | [IMF TNM/14/04](https://www.imf.org/external/pubs/ft/tnm/2014/tnm1404.pdf); [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf) |
| **EU-integratie** | **n.a. — onvoldoende empirische basis — model-tuning parameter** | — | — | Geen directe multiplier-schatting gevonden |
| **Deregulering** | **n.a. — onvoldoende empirische basis — model-tuning parameter** | — | — | Geen fiscale-multiplier-literatuur; is geen fiscale schok |

### Detail-ankers

**Belastingverlaging.** Eerste-jaars tax-multiplier in geavanceerde economieën gemiddeld **−0,25** ([IMF TNM/14/04, Mineshima e.a.](https://www.imf.org/external/pubs/ft/tnm/2014/tnm1404.pdf): "first-year multipliers amount on average to 0.75 for government spending and 0.25 for government revenues in AEs"). Voor **Duitsland specifiek** vindt de narratieve benadering een tax-multiplier van **1 in jaar 1, oplopend tot ~2,4 na 8 kwartalen** (idem, tabel 1). Narratief-brede consensus: **−2 tot −3** ([Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf)).

**Groen-investeren / publieke investering.** "Public investment multipliers: 0.4 short-run to 1.6 long-run" ([Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf), citerend Ilzetzki/Mendoza/Végh). Hoger dan consumptieve bestedingen.

**Sociaal-transfer.** "Permanent increases in benefits led to a roughly equal rise in consumption in the short-run, but the effect dissipated quickly … Temporary increases in benefits had no significant effect on aggregate consumption" ([Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf)).

**Algemene bestedingen (benchmark).** "The bulk of the estimates … lie in a surprisingly narrow range of 0.6 to 1" ([Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf)); IMF WEO okt-2020/2022-lijn bevestigt eerste-jaars spending-multiplier ~0,75 ([IMF TNM/14/04](https://www.imf.org/external/pubs/ft/tnm/2014/tnm1404.pdf)).

**Blanchard & Leigh (2013):** feitelijke multipliers in crisisjaren waren ~1,7 i.p.v. de aangenomen 0,5 — een factor tot 3 hoger dan verwacht ([Growth Forecast Errors and Fiscal Multipliers, IMF WP 13/1](https://www.elibrary.imf.org/view/journals/001/2013/001/001.2013.issue-001-en.xml); [NBER w18779](https://www.nber.org/system/files/working_papers/w18779/w18779.pdf)). **Staat-afhankelijkheid:** multipliers zijn groter in recessies ([Auerbach & Gorodnichenko 2012](https://www.aeaweb.org/articles?id=10.1257%2Fpol.4.2.1)).

### Bron-tabel

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| IMF Technical Notes and Manuals 14/04 (Mineshima e.a.) | https://www.imf.org/external/pubs/ft/tnm/2014/tnm1404.pdf | 2014 | "first-year multipliers amount on average to 0.75 for government spending and 0.25 for government revenues in AEs"; Duitsland tax-multiplier "1 … maximum after 8 quarters (about 2.4)" |
| Ramey (2019), JEP 33(2):89-114 | https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf | 2019 | Spending 0,6–1; tax −2 tot −3; public investment 0,4→1,6; ZLB 1,5+ |
| Blanchard & Leigh (2013), IMF WP 13/1 | https://www.elibrary.imf.org/view/journals/001/2013/001/001.2013.issue-001-en.xml | 2013 | Feitelijke multipliers substantieel hoger dan aangenomen (tot factor 3; ~1,7 i.p.v. 0,5) |
| Ilzetzki, Mendoza & Végh (2013), NBER w16479 | https://www.nber.org/system/files/working_papers/w16479/revisions/w16479.rev1.pdf | 2013 | Impact-multiplier high-income 0,37 → long-run 0,80; fixed exchange rate 1,5; flexibel ~0; open/hoog-schuld ~0 |

### Aanbeveling engine-code

Gebruik de volgende centrale multipliers als default; markeer EU-integratie en deregulering expliciet als tuning-parameters:
```
tax_cut_multiplier      = -0.25   # impact; laat oplopen naar -2.0 cumulatief (narratief) via lag-profiel
green_invest_multiplier =  0.5    # impact; long-run 1.5 (Ilzetzki/Ramey)
social_transfer_mult    =  0.6    # permanent; ~0 indien tijdelijk
gov_spending_benchmark  =  0.75   # jaar 1 (IMF); cumulatief 0.6-1.0
eu_integration_mult     =  n.a.   # MODEL-TUNING (geen empirische fiscale multiplier)
deregulation_mult       =  n.a.   # MODEL-TUNING (geen fiscale schok)
```
Belangrijk: pas een **recessie-opslag** toe (DE 2026 zit dicht bij nulgroei): multipliers in downturns liggen 0,7–0,9 units hoger voor spending ([talouspolitiikan review](https://talouspolitiikanarviointineuvosto.fi/wp-content/uploads/2020/05/fiscal_multiplier_review.pdf); [Auerbach & Gorodnichenko](https://www.aeaweb.org/articles?id=10.1257%2Fpol.4.2.1)).

---

## VRAAG 3 — Snelheid politieke doorwerking (policy lag)

**Doel:** Jaar-1 vs jaar-3 vs jaar-5 doorwerking als % van het uiteindelijke effect.

### Centrale bevinding — twee profielen, afhankelijk van beleidstype

**Bestedingsschokken werken snel door; belastingschokken bouwen langzamer maar dieper op.**

| Doorwerking als % van eindeffect | Bestedingen (spending) | Belasting (tax) | Bron |
|---|---|---|---|
| **Jaar 1** | **~75–90%** | **~30–50%** | [IMF WP 12/286](https://www.imf.org/-/media/Websites/IMF/imported-full-text-pdf/external/pubs/ft/wp/2012/_wp12286.ashx): "a large part … materializes within 4 quarters" |
| **Jaar 3** | **~90–100%** | **~80–90%** | [Alesina/Favero/Giavazzi 2019](https://didattica.unibocconi.it/mypage/upload/48917_20190504_114457_JEP.33.2.141.PDF): tax-effect "lasts 3–4 years"; piek in ~18 mnd ([Ramey](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf)) |
| **Jaar 5** | **~100%** (stabiel) | **~100%** | [Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf): "cumulative multipliers usually do not vary greatly across horizons up to five years" |

### Detail-ankers

- **Bestedingen — snel:** "cumulative multipliers usually do not vary greatly across horizons up to five years" en pieken "after about a year" ([Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf)). IMF: "Second-year cumulative multipliers have similar sizes to 1-year multipliers, implying that a large part of the impact of fiscal shocks on output materializes within 4 quarters" ([IMF WP 12/286](https://www.imf.org/-/media/Websites/IMF/imported-full-text-pdf/external/pubs/ft/wp/2012/_wp12286.ashx)).
- **Belasting — trager, dieper:** "many estimates of tax multipliers start out low on impact but then build … peak output effects occur in the first 18 months" ([Ramey 2019](https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf)). Tax-based consolidaties: "the effect lasts 3–4 years" ([Alesina/Favero/Giavazzi 2019](https://didattica.unibocconi.it/mypage/upload/48917_20190504_114457_JEP.33.2.141.PDF)).
- **Ilzetzki/Mendoza/Végh timing:** cumulatieve multiplier stijgt van impact 0,37 naar long-run 0,80 voor high-income landen — ~46% van het eindeffect zit al in het impact-kwartaal ([NBER w16479](https://www.nber.org/system/files/working_papers/w16479/revisions/w16479.rev1.pdf)).
- **State-dependency / Auerbach-Gorodnichenko:** 5-jaars multipliers 2,2 in recessies vs −0,3 in expansies; het profiel is sterk regime-afhankelijk ([discussie Ramey](https://econweb.ucsd.edu/~vramey/research/Ramey-Discussion-of-Auerbach.pdf); [AG 2012](https://www.aeaweb.org/articles?id=10.1257%2Fpol.4.2.1)).
- **Friedman "long and variable lags":** conceptueel anker; de empirische fiscale literatuur bevestigt dat het grootste deel van het effect binnen 1–2 jaar valt voor bestedingen, 3–4 jaar voor belasting.

### Bron-tabel

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| Baum, Poplawski-Ribeiro & Weber, IMF WP 12/286 | https://www.imf.org/-/media/Websites/IMF/imported-full-text-pdf/external/pubs/ft/wp/2012/_wp12286.ashx | 2012 | "a large part of the impact of fiscal shocks on output materializes within 4 quarters" |
| Ramey (2019), JEP | https://econweb.ucsd.edu/~vramey/research/Ramey_Fiscal_JEP.pdf | 2019 | "cumulative multipliers usually do not vary greatly across horizons up to five years"; tax "start out low … then build … peak in first 18 months" |
| Alesina, Favero & Giavazzi (2019), JEP 33(2):141-62 | https://didattica.unibocconi.it/mypage/upload/48917_20190504_114457_JEP.33.2.141.PDF | 2019 | Tax-based plans: "losses of more than two percentage points … effect lasts 3–4 years"; spending-based "lasts less than two years" |
| Ilzetzki, Mendoza & Végh (2013), NBER w16479 | https://www.nber.org/system/files/working_papers/w16479/revisions/w16479.rev1.pdf | 2013 | Impact 0,37 → long-run 0,80 (cumulatief profiel) |

### Aanbeveling engine-code

Modelleer **twee lag-profielen** (kies op basis van beleidstype):
```
# Bestedingen / investeringen (snel):
lag_spending = {jaar1: 0.80, jaar3: 0.95, jaar5: 1.00}
# Belasting (traag, dieper):
lag_tax      = {jaar1: 0.40, jaar3: 0.85, jaar5: 1.00}
```
De gevraagde "ideaal 80–100% in jaar 5" wordt gehaald: beide profielen bereiken ~100% in jaar 5. **Pas een recessie-schakelaar toe** — in de DE-2026-context (nulgroei) liggen effecten hoger en persistenter.

---

## VRAAG 4 — Duitsland 2026 macro-context (verificatie)

| Engine-startwaarde | Verificatie | Oordeel | Bron |
|---|---|---|---|
| **NEPK 6,83% BIP** | Standaard tax-to-GDP DE = **38,1% (2023)**; OECD-gemiddelde 33,9%. 6,83% is géén standaard belastingdruk-maat. | **Niet verifieerbaar als standaardmaat — engine-specifieke definitie. Onvoldoende empirische basis om 6,83% te bevestigen; model-definitie-parameter.** | [OECD Revenue Statistics 2024 — Germany](https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/global-tax-revenues/revenue-statistics-germany.pdf) |
| **Reëel BIP-groei 2026 ~0–0,5%** | Bundesbank (dec-2025): **+0,6%** kalendergecorrigeerd (0,9% ongecorrigeerd). EU-Commissie: **+0,6%**. | **Grotendeels correct; iets aan de lage kant.** Officiële prognose 0,6%, marginaal boven de engine-range. | [Bundesbank Forecast dec-2025](https://www.bundesbank.de/en/press/press-releases/bundesbank-s-forecast-for-germany-economy-will-gradually-recover-965032); [EU-Commissie DE](https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/germany/economic-forecast-germany_en) |
| **Ontslagen industrie 2024–2026: 500.000+** | EY/dpa: **124.000 in 2025** (industriewerkgelegenheid −2,3%); cumulatief **266.000 sinds 2019** (dpa feb-2026) of **341.500 sinds 2019** (EY Q1-2026, incl. bredere afbakening). | **Overschat. Bevestigd 266.000–341.500 sinds 2019; 500.000+ niet gestaafd. Markeer als te hoog.** | [dpa/Yahoo feb-2026](https://finance.yahoo.com/news/analysis-german-industry-cut-124-105835807.html); [Reuters/EY mei-2026](https://www.reuters.com/business/german-industry-keeps-cutting-jobs-despite-first-sales-rise-three-years-ey-says-2026-05-25/) |
| **Miljonair-uitstroom DE → CH/AT/ES** | Bevestigd: wereldwijd **165.000 miljonairs** verhuizen in 2025 (+14% vs 2024, was 142.000). Duitsland klom naar rang **13** onder bronlanden; **~400 vertrekkende DE-miljonairs** namen **€1,87 mrd** mee. | **Kwalitatief correct; trend en bestemmingen (o.a. Italië flat-tax €300k) bevestigd.** | [Het Open Vizier — matrix of the exodus](https://openvizier.org/en/what-surfaces/the-matrix-of-the-exodus); [Henley/Euronews](https://www.euronews.com/business/2026/06/21/which-european-countries-are-attracting-millionaires-and-which-are-losing-them) |

### Aanvullende context

- Bundesbank: HICP-inflatie DE **2,2% in 2026**, herstel "gradually … strengthen markedly" vanaf Q2-2026, gedreven door defensie- en infrastructuuruitgaven ([Bundesbank dec-2025](https://www.bundesbank.de/en/press/press-releases/bundesbank-s-forecast-for-germany-economy-will-gradually-recover-965032)).
- EU-Commissie: overheidstekort DE **3,7% BIP in 2026**, oplopend naar 4,1% in 2027 ([EU-Commissie](https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/germany/economic-forecast-germany_en)).
- Automotive sector: **111.000 banen verloren sinds 2019** (−13%) ([dpa/Yahoo](https://finance.yahoo.com/news/analysis-german-industry-cut-124-105835807.html)).

### Aanbeveling engine-code

- **BIP-groei 2026:** stel in op **0,6%** (officiële consensus), niet 0–0,5%.
- **Industrie-ontslagen:** corrigeer naar **~266.000–342.000 cumulatief sinds 2019** (niet 500.000+). Als de engine een breder "totale banenverlies inclusief toeleveranciers/aankondigingen" bedoelt, markeer expliciet en documenteer de afbakening.
- **NEPK 6,83%:** documenteer de exacte definitie in de code-comments; kan niet aan OECD/Destatis-standaardmaat worden gekoppeld → **definitie-parameter, geen externe verificatie mogelijk.**

---

## VRAAG 5 — Malta 2026 macro-context (verificatie)

| Engine-startwaarde | Verificatie | Oordeel | Bron |
|---|---|---|---|
| **NEPK 4,40% BIP** | IMF: overall tax burden (belasting + netto sociale premies) MT = **~29% BIP (2024)**, 4e-laagste in EU. Totale overheidsinkomsten **33,8% BIP (2025)**. 4,40% is géén standaardmaat. | **Niet verifieerbaar als standaardmaat — engine-specifieke "netto"-definitie. Onvoldoende basis om 4,40% te bevestigen; definitie-parameter.** | [IMF Malta 2025 Article IV](https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf) |
| **BEPS Pillar 2 (15% min. effective tax) impact** | IMF: QDMTT-implementatie **uitgesteld tot eind-2029**; zou "an additional 2 percent of GDP" kunnen opleveren. Malta koos elective 15%-regime (Legal Notice 188/2025). | **Correct als toekomstige impact; feitelijke invoering uitgesteld tot 2029.** | [IMF Malta 2025 AIV](https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf); [KPMG Malta 15% minimum tax](https://kpmg.com/mt/en/home/insights/2025/01/malta-in-the-15-percent-global-minimum-tax-world.html); [EY Malta mrt-2026](https://www.ey.com/en_mt/newsroom/ey-newsletters/tax/malta-direct-tax-newsletter-march-2026) |
| **CBI (Citizenship by Investment) einde 2025 na EU-arrest** | ECJ-arrest **29 april 2025**: golden-passport-scheme in strijd met EU-recht; Malta beëindigde het programma (nu "merit-based naturalisation"). Programma genereerde ~€1,4 mrd. | **Correct. Beëindigd na ECJ-arrest april 2025 (dus effectief 2025).** | [Reuters ECJ-arrest](https://www.reuters.com/world/europe/eu-top-court-rules-against-maltas-golden-passport-scheme-2025-04-29/); [DW](https://www.dw.com/en/eu-citizenship-no-longer-for-sale/a-72416965); [Verfassungsblog](https://verfassungsblog.de/the-eu-free-market-does-not-extend-to-citizenship/) |
| **AMLA impact iGaming-sector** | AMLA (Frankfurt) operationeel **jan-2026**; eerste directe-supervisie-selecties Q3-2026, iGaming expliciet in risicokader. Regulation (EU) 2024/1624 volledig afdwingbaar mei-2026; boetes tot 10% jaaromzet; compliance-uplift 8–15% opex; 3 mid-tier operators verlieten EU-markt. | **Correct qua tijdlijn en impactrichting (kostenstijging, marktexits).** | [Growl Games — AMLA iGaming](https://growl.games/blog/eu-amla-enforcement-hits-igaming-what-operators-must-do-now-1782543279163); [MGA/AMLA consultaties](https://sccgmanagement.com/sccg-news/2026/3/3/mga-calls-on-licensees-to-engage-in-eu-aml-consultations/) |
| **Sicily-Malta interconnector energiekosten** | Tweede interconnector: €300 mln-contract (apr-2025), Italiaans permit jan-2025, EIB-financiering €100 mln (apr-2026); verdubbelt netconnectiviteit; €712 mln netto economisch voordeel over 25 jaar. Energiesubsidies daalden naar 0,8% BIP (2025). | **Correct; project in aanbouw, verlaagt energiekosten/risico's op termijn.** | [Malta Independent](https://www.independent.com.mt/articles/2025-01-10/local/Italy-approves-permit-for-the-development-of-Malta-Sicily-second-interconnector-6736267033); [EIB apr-2026](https://www.eib.org/en/press/all/2026-151-eib-backs-with-eur100-million-malta-s-energy-transition-through-second-electricity-interconnector-with-italy); [IMF Malta AIV](https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf) |

### Aanvullende context

- IMF: MT BIP-groei **3,9% (2025)**, verwacht **~4% (2026)** — ver boven EU-gemiddelde; lopende rekening-overschot **6,3% BIP (2025)** ([IMF Malta 2025 AIV](https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf)).
- MT VAT-compliance-gap **25,9% (2022)** — een van de hoogste in de EU ([IMF Malta 2025 AIV](https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf)).
- Overheidsschuld steeg van 46,2% (2024) naar ~47% BIP (2025); tekort 3,2% BIP (2025) ([IMF Malta 2025 AIV](https://www.imf.org/-/media/files/publications/cr/2026/english/1mltea2026001-source-pdf.pdf)).

### Aanbeveling engine-code

- **NEPK 4,40%:** documenteer definitie; niet koppelbaar aan IMF/EU-standaard (29% overall burden) → definitie-parameter.
- **Pillar 2:** modelleer als **latente schok vanaf 2029** (+~2% BIP potentiële opbrengst), niet als 2026-effect.
- **CBI-einde & AMLA:** modelleer als negatieve hub-schokken vanaf 2025/2026 (inkomstenverlies CBI ~€1,4 mrd cumulatief; iGaming opex +8–15%).
- **Interconnector:** modelleer als geleidelijke energiekosten-/subsidiedaling (0,9%→0,7% BIP subsidie, 2024→2026).

---

## SAMENVATTENDE PARAMETER-AANBEVELINGEN

| Parameter | Aanbevolen engine-waarde | Empirische status |
|---|---|---|
| NEPK→koopkracht β (jaar 1) | −1,25% inkomen per pp-BIP | **Onderbouwd** (DIW, 2 sub-metingen) |
| NEPK→koopkracht (5-jr scenario +3,17pp) | −5,5% centraal (range −4 tot −9%) | Onderbouwd (DIW + Ramey) |
| Tax-cut multiplier | −0,25 impact → −2,0 cumulatief | **Onderbouwd** (IMF, Ramey, B&L) |
| Groen-investeren multiplier | 0,5 impact → 1,5 long-run | **Onderbouwd** (Ramey, IMV) |
| Sociaal-transfer multiplier | 0,6 permanent / ~0 tijdelijk | **Onderbouwd** (Ramey) |
| EU-integratie multiplier | n.a. | **Model-tuning parameter** |
| Deregulering multiplier | n.a. | **Model-tuning parameter** |
| Lag-profiel bestedingen | j1 0,80 / j3 0,95 / j5 1,00 | **Onderbouwd** (IMF, Ramey) |
| Lag-profiel belasting | j1 0,40 / j3 0,85 / j5 1,00 | **Onderbouwd** (Ramey, AFG) |
| DE BIP-groei 2026 | 0,6% | **Onderbouwd** (Bundesbank, EU) |
| DE industrie-ontslagen | 266.000–342.000 sinds 2019 (niet 500k+) | **Onderbouwd; engine-waarde te hoog** |
| DE NEPK 6,83% | definitie-parameter | Niet extern verifieerbaar |
| MT NEPK 4,40% | definitie-parameter | Niet extern verifieerbaar |
| MT Pillar 2 impact | +2% BIP, latent vanaf 2029 | **Onderbouwd** (IMF) |
| MT CBI-einde | 2025 (ECJ apr-2025) | **Onderbouwd** |
| MT AMLA iGaming | opex +8–15% vanaf 2026 | **Onderbouwd** |

**Twee parameters missen minstens 2 onafhankelijke bronnen en zijn expliciet gemarkeerd als "onvoldoende empirische basis — model-tuning parameter": EU-integratie-multiplier en deregulering-multiplier.** De NEPK-startwaarden (6,83% DE, 4,40% MT) zijn interne definitie-parameters die niet aan standaard-belastingdrukmaten koppelen.
