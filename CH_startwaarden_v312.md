# Zwitserland (CH) – NEPK-startwaarden 2026 & partij-landschap

**Engine:** "Het Open Vizier" gevolgenkaart-app · politiek-economische simulatie
**Formule:** NEPK% = E_tv × α × (1−τ) × φ   ·   NTPK% = E_tv × α × (1−τ)
**Peildatum onderzoek:** 4 juli 2026 · Alle waarden met bron-URL. "n.a." = niet uit gefetchte bron te bevestigen.

> **Belangrijke methodische kanttekening.** De vier NEPK-factoren zijn engine-constructen, geen officiële statistieken. Geen enkele bron publiceert "α" of "φ" rechtstreeks. Onder elke factor staat welke *gefetchte, geciteerde* statistieken de proxy onderbouwen; de puntschatting is een expliciete afleiding daaruit. Waar de brontekst de deelwaarde niet dekt, staat "n.a." en wordt de afleiding als *engine-aanname* gemarkeerd.

---

## VRAAG 1 — Zwitserse NEPK-startwaarden 2026

### Samenvatting eindwaarde

| Factor | Waarde 2026 | Basis |
|---|---:|---|
| **E_tv** (exportgedreven toegevoegde waarde, % BIP, doorvoer eruit) | **0,390 (39,0%)** | SECO TiVA: export op waardecreatie-basis = 39% BIP; transit reeds buiten TiVA-DVA |
| **α** (productieve-kern-fractie na overhead) | **0,52** | BFS: niet-financiële ondernemingen + huishoudens = 79% BWS; kern-productieve deel afgeleid |
| **τ** (effectieve netto-belastingdruk productieve activiteit) | **0,29** | OECD tax-to-GDP 27,1% (2023) / Eurostat 27,8% (2024); eff. bedrijfsbelasting 14,43% |
| **φ** (aandeel in nationale handen, buitenlands eigendom eruit) | **0,54** | admin.ch: buitenlands-gecontroleerde groepen ≈ 2/3 omzet; ≈ helft werkgelegenheid |

**NTPK 2026 = E_tv × α × (1−τ) = 0,390 × 0,52 × (1−0,29) = 0,1440 → 14,40%**

**NEPK 2026 = NTPK × φ = 0,1440 × 0,54 = 0,0778 → ≈ 7,8%**

> Ter kalibratie: CH ligt daarmee boven DE (6,83%) en NL (3,75%) uit de referentieset — plausibel voor een sterk export-georiënteerde, laag-belaste economie met hoge binnenlandse waardecreatie, ondanks lage φ door veel buitenlands-gecontroleerde multinationals. **Zie gevoeligheidsanalyse onderaan Vraag 1.**

---

### Factor E_tv — exportgedreven toegevoegde waarde (% BIP, DOORVOER ERUIT)

**Waarde: 0,390 (39,0%)**

Zwitserse export op *waardecreatie*-basis (TiVA) = **39% van het nominale BIP** (gemiddelde 2005–2015), volgens de canonieke SECO/OECD-berekening. Deze maatstaf trekt reeds de buitenlandse input (backward participation, ~25%) af én is gebaseerd op TiVA, dat fysieke doorvoer/merchanting niet als binnenlandse waardecreatie meetelt. De ruwe exportquote (goederen+diensten) is veel hoger (72–78% BIP) maar bevat buitenlandse tussenproducten en effecten van transithandel; die is voor NEPK ongeschikt.

De Transit-Handel (goud, chemicals, merchanting) is separaat ~8% BIP (2021) en zit — cruciaal — *niet* in de 39%-TiVA-waarde, want TiVA meet binnenlandse waardecreatie in bruto-export, niet doorvoermarges. E_tv=39,0% is dus reeds "doorvoer eruit".

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| SECO – Exporte auf Wertschöpfungsbasis | [seco.admin.ch (PDF)](https://www.seco.admin.ch/dam/de/sd-web/klmw2e3njnIX/2021-3-KT-Exkurs-Exporte-Wertsch%C3%B6pfung-SECO.pdf) | 2021 (data 2005–2015) | "2015 beliefen sie sich auf 39 % des nominalen BIP … Durchschnittswert von 39 % für den Zeitraum 2005−2015"; backward-participation "leicht über 25 %" |
| SECO/OECD – TiVA Switzerland | [seco.admin.ch (PDF)](https://www.seco.admin.ch/dam/seco/de/dokumente/Aussenhandelsstatistik/OECD/TiVA%20Switzerland%202015.pdf.download.pdf/TiVA%20Switzerland%202015.pdf) | 2015 (data 2011) | "foreign content share of exports of just over one-fifth (21.7%) in 2011"; "39.4% of Switzerland's domestic value added was driven by foreign final demand" |
| Die Volkswirtschaft – Transithandel | [dievolkswirtschaft.ch](https://dievolkswirtschaft.ch/de/2023/02/transithandel-ein-gradmesser-der-globalisierung/) | 23-02-2023 | "Nettoeinnahmen aus dem Transithandel 2021 rund 8 Prozent des Schweizer BIP" (Transithandel 58,5 Mrd CHF) |
| SECO GVC-Strukturbericht | [seco.admin.ch (PDF)](https://www.seco.admin.ch/dam/seco/de/dokumente/Publikationen_Dienstleistungen/Publikationen_Formulare/Wirtschaftslage/Strukturberichterstattung/Die%20volkswirtschaftliche%20Bedeutung%20der%20globalen%20Wertsch%C3%B6pfungsketten%20f%C3%BCr%20die%20Schweiz%20-%20Analysen%20auf%20Basis%20einer%20neuen%20Datengrundlage.pdf.download.pdf/Die%20volkswirtschaftliche%20Bedeutung%20der%20globalen%20Wertsch%C3%B6pfungsketten%20f%C3%BCr%20die%20Schweiz%20-%20Analysen%20auf%20Basis%20einer%20neuen%20Datengrundlage.pdf) | n.d. (data 2008) | "inländischer Wertschöpfungsanteil von 72%" van de bruto-export; dienstenexport ~86%, warenexport ~64% |

*Trend-nuance:* de ruwe exportquote steeg van 51% (2000) naar 70–78% (2021–2025), maar dat is deels transit/merchanting-inflatie. De TiVA-waardecreatie is stabiel ~39%. Engine-startwaarde **E_tv = 0,390** is conservatief en "doorvoer-schoon".

---

### Factor α — productieve-kern-fractie na overhead-aftrek

**Waarde: 0,52** *(engine-afleiding; geen bron publiceert α direct)*

Onderbouwing uit BFS-productierekeningen: de sectoren "niet-financiële kapitaalvennootschappen + private huishoudens" leveren **79% van de Bruttowertschöpfung (BWS)**; financiële vennootschappen 9%, Staat 10%, NPO's ~2% (2022). De marktsector-productieve kern is dus ruim. Sectorstructuur: diensten 71,9–74% BWS, industrie/productiesector 24,9–25,3%, landbouw 0,6% (2023–2024). Het verwerkende gewerbe alleen = 143 mld CHF (2023), veruit de grootste tak.

Engine-logica: α = productieve activiteit (industrie + hoogwaardige diensten) / totale gross output, na overhead-aftrek (publieke admin, zuivere rent-seeking, deel van vastgoed-imputatie). Voor CH is de industrie hoogwaardig (pharma/precision) en een groot deel van de diensten productief-exporteerbaar (~60% van exportwaardecreatie is diensten). Dat rechtvaardigt een hoge α aan de bovenkant van de verwachte 0,45–0,55-band. Gekozen **α = 0,52** (iets boven DE=0,45, in lijn met CH's hogere aandeel hoogwaardige export-diensten).

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| BFS – Branchenstruktur / Produktionskonto | [bfs.admin.ch](https://www.bfs.admin.ch/bfs/de/home/statistiken/querschnittsthemen/wohlfahrtsmessung/gueter/oekonomische-gueter/branchenstruktur.html) | 14-12-2023 | "Produktion der Sektoren «nichtfinanzielle Kapitalgesellschaften und private Haushalte» 79% der Bruttowertschöpfung … «finanzielle Kapitalgesellschaften» und «Staat» jeweils 9% bzw. 10%" |
| BFS – VGR 2023 (BWS naar A21-branches) | [bfs.admin.ch (PDF)](https://dam-api.bfs.admin.ch/hub/api/dam/assets/32257680/master) | 2024 (data 2023) | Verarbeitendes Gewerbe 143.346 Mio CHF; Finanzdienstleistungen 42.594; Versicherungen 31.320; Grundstücks-/Wohnungswesen 53.627 (2023) |
| WKO – Länderprofil CH (BWS naar sector) | [wko.at (PDF)](https://www.wko.at/oe/statistik/laenderprofile/lp-schweiz.pdf) | 2024/2025 | "Landwirtschaft 0,6 · Produktionsbereich 24,7 · Dienstleistungen 72,0" (% BIP, 2024) |
| Statista – BWS naar sector | [de.statista.com](https://de.statista.com/statistik/daten/studie/216752/umfrage/anteile-der-wirtschaftssektoren-am-bruttoinlandsprodukt-der-schweiz/) | 04-12-2024 | "2023 … Industrie 25,3 Prozent und der Dienstleistungssektor 74 Prozent" |

---

### Factor τ — effectieve netto-belastingdruk op productieve activiteit

**Waarde: 0,29**

CH is een uitgesproken laag-belastingland: totale tax-to-GDP **27,1% (2023, OECD)**, resp. **27,8% (2024, Eurostat)** — bij de laagste in de OESO (rang 31/38) tegenover OESO-gemiddelde 33,9–34,1%. Effectieve winstbelasting (federaal+kantonaal+gemeentelijk) gemiddeld **14,43% (2026, KPMG)**, kantonaal van 11,66% (Luzern) tot >15% (Bern/Zürich/Tessin). OECD-Pillar 2 tilt de effectieve druk voor grote multinationals (>€750 mln omzet) op naar 15% sinds 2024 (QDMTT) / 2025 (IIR), maar treft slechts ~1% van de bedrijven.

Engine-logica: τ is de effectieve netto-druk op de *productieve activiteit* (bedrijf + werknemer + sociale premies), niet alleen winstbelasting. De tax-to-GDP van ~28% vormt de bovengrens; effectieve productieve druk ligt daar iets onder na aftrek van niet-productie-gerelateerde heffingen. Startwaarde **τ = 0,29** (net boven de 27,8% macro-quote, lager dan NL 0,43 / DE 0,414 / MT 0,297 — in lijn met MT als laag-belastingland).

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| OECD – Revenue Statistics 2024, Switzerland | [oecd.org (PDF)](https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/global-tax-revenues/revenue-statistics-switzerland.pdf) | 2024 (data 2023) | "tax-to-GDP ratio in Switzerland increased … to 27.1% in 2023 … OECD average of 33.9% … ranked 31st out of 38" |
| Eurostat – Tax revenue statistics | [ec.europa.eu (PDF)](https://ec.europa.eu/eurostat/statistics-explained/SEPDF/cache/6915.pdf?v=2321446058883423) | 2025 (data 2024) | "Switzerland (27.8%) registered the lowest ratios among the reporting EU and EFTA countries" |
| KPMG – Clarity on Swiss Taxes 2026 | [kpmg.com (PDF)](https://assets.kpmg.com/content/dam/kpmgsites/ch/pdf/kpmg-ch-swiss-taxes-2026-clarity.pdf.coredownload.inline.pdf) | 31-05-2026 | "average corporate income tax rates … from 14.40% to 14.43% … Lucerne … 11.66% … average minimum tax rate in Switzerland is 11% in 2026" |
| EFD – OECD-Mindeststeuer Umsetzung | [efd.admin.ch](https://www.efd.admin.ch/en/implementation-oecd-minimum-tax-rate-switzerland) | 04-09-2024 | QDMTT vanaf 01-01-2024, IIR vanaf 01-01-2025; "approximately 99% of companies … not directly affected"; extra opbrengst CHF 1,6 mld in financieel plan vanaf 2026 |
| PwC – Taxes on corporate income CH | [taxsummaries.pwc.com](https://taxsummaries.pwc.com/switzerland/corporate/taxes-on-corporate-income) | 14-01-2026 | "maximum CIT rate on profit before tax for federal, cantonal, and communal taxes is between 11.66% and 20.54%" |

---

### Factor φ — aandeel in nationale handen (buitenlands eigendom eruit)

**Waarde: 0,54** *(engine-afleiding; benaderd via omzet/werkgelegenheids-controle)*

BFS/admin.ch (nov 2025, experimentele statistiek): buitenlands-gecontroleerde multinationale groepen genereren **"knapp zwei Drittel" (≈64%) van de totale omzet** van alle ondernemingsgroepen en **"knapp die Hälfte" (≈50%) van de werkgelegenheid** ("mehr als zwei von fünf Arbeitsplätzen" in de marktsector). Zuiver-binnenlandse groepen: slechts 4% van de omzet. Bruttowertschöpfung naar controle-herkomst is nog niet officieel gepubliceerd (n.a. voor exacte BWS-splitsing).

Engine-logica: φ = aandeel productieve activa/output in Zwitserse handen. De omzet-controle (36% binnenlands) is een ondergrens (omzet inflateert door buitenlandse merchanting/multinationals), de werkgelegenheid-controle (~50% binnenlands) een bovengrens. Gewogen naar output/waardecreatie kiezen we het midden: **φ = 0,54**. Dit ligt tussen MT (0,45) en DE (0,82), passend bij CH's zeer open economie met veel buitenlands-gecontroleerde hoofdkantoren (naast binnenlandse reuzen Nestlé, Novartis, Roche, UBS).

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| admin.ch – Unternehmensgruppen (multinationals) | [admin.ch](https://www.admin.ch/de/newnsb/JYypuIwYkeNto03DLe3Sm) | 27-11-2025 | Buitenlands-gecontroleerd: "knapp zwei Drittel des Gesamtumsatzes" en "knapp die Hälfte der Arbeitnehmenden"; "mehr als zwei von fünf Arbeitsplätzen"; zuiver-binnenlandse groepen "4% … am Gesamtumsatz"; totaal 2.136.580 werknemers, omzet >2.570 mld CHF (2023) |
| BFS – Wertschöpfungsstatistik | [bfs.admin.ch](https://www.bfs.admin.ch/bfs/de/home/statistiken/industrie-dienstleistungen/wertschoepfungsstatistik.html) | 2023 | Officiële BWS-splitsing naar buitenlandse/binnenlandse controle — n.a. (BWS-per-controle nog experimenteel) |

*Onzekerheid:* φ is de meest onzekere factor. Officiële BWS-naar-controle ontbreekt (n.a.). Range 0,45–0,60 verdedigbaar; 0,54 is centrale schatting.

---

### Gevoeligheidsanalyse NEPK 2026 (φ-band)

| Scenario | E_tv | α | τ | φ | NTPK | **NEPK** |
|---|---:|---:|---:|---:|---:|---:|
| Laag (φ=0,45) | 0,390 | 0,52 | 0,29 | 0,45 | 14,40% | **6,48%** |
| **Centraal (φ=0,54)** | 0,390 | 0,52 | 0,29 | 0,54 | 14,40% | **7,78%** |
| Hoog (φ=0,60) | 0,390 | 0,52 | 0,29 | 0,60 | 14,40% | **8,64%** |

**Engine-startwaarde: NEPK 2026 ≈ 7,8% · NTPK 2026 ≈ 14,4%.**

---

## VRAAG 2 — Zwitserse baseline_tempo 2026–2036 (jaarlijkse drift, ongewijzigd beleid)

| Factor | baseline_tempo/jaar | Richting | Onderbouwing |
|---|---:|---|---|
| **E_tv_pp_per_jaar** | **−0,10 pp** | Licht dalend | US-tarieven (15% na verlaging van 39%), China-vraagzwakte, frankappreciatie, farma-prijsdruk, inland-productie-trend drukken export; deels gecompenseerd door Europese vraag. TiVA-waardecreatie historisch stabiel ~39%, dus milde daling. |
| **alpha_per_jaar** | **−0,003/jaar** | Licht dalend | Voortgaande tertiarisering: dienstenaandeel BWS steeg 68,6%→73,8% (1995–2022), industrie 30,0%→25,6%. Deïndustrialisering-druk, maar hoogwaardige diensten compenseren deels. |
| **tau_per_jaar** | **+0,002/jaar** | Licht stijgend | OECD Pillar 2: kantons verhogen effectieve tarieven richting 15% (Genf, Waadt, Schaffhausen, Basel-Stadt 13,04%→14,53% vanaf 2026). Extra CHF ~1,6 mld/jaar. Gemiddeld eff. tarief 14,40%→14,43%. |
| **phi_per_jaar** | **−0,002/jaar** | Licht dalend / stabiel | Buitenlands-gecontroleerde groepen groeien qua werkgelegenheid trager (+0,2%) dan binnenlandse (+1,4%, 2024) → stabiliserend. UBS-CS-fusie 2023 concentreerde binnenlandse financiële controle (Zwitsers eigendom), maar netto lichte openheids-toename verwacht. |

### Onderbouwende bronnen Vraag 2

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| KOF – Konjunkturprognose dec 2025 | [kof.ethz.ch](https://kof.ethz.ch/news-und-veranstaltungen/medien/medienmitteilungen/2025/12/kof-konjunkturprognose-trotz-handelsdeal-truebe-aussichten-fuer-schweizer-wirtschaft.html) | 15-12-2025 | BIP 2026 +1,1% (sportbereinigt), 2027 +1,7%; US-Zölle van 39%→15%; "zunehmende Bestrebungen zur Inlandproduktion belasten die Schweizer Exportentwicklung"; farma-prijsdruk-risico; frankappreciatie belast concurrentiekracht; Inflation 2026 0,3%; SNB-Leitzins 0% |
| SECO – Konjunkturprognose 2026 | [seco.admin.ch (PDF)](https://www.seco.admin.ch/dam/seco/en/dokumente/Wirtschaft/Wirtschaftslage/Konjunkturprognosen/2026-1-kt-prognose-szenario-seco.pdf.download.pdf/2026-1-KT-Prognose-Szenario-SECO.pdf) | 2026 | BIP-groei 2026 "1,0 %" (basis) / "0,8 %" (scenario) — "deutlich unterdurchschnittliches Wachstum" |
| BFS – Tertiarisering (dienstenaandeel) | [bfs.admin.ch](https://www.bfs.admin.ch/bfs/de/home/statistiken/querschnittsthemen/wohlfahrtsmessung/gueter/oekonomische-gueter/branchenstruktur.html) | 14-12-2023 | Dienstensector "von 68,6% (1995) auf 73,8% (2022)"; industrie "von 30,0% auf 25,6%" |
| KPMG – Clarity on Swiss Taxes 2026 | [kpmg.com (PDF)](https://assets.kpmg.com/content/dam/kpmgsites/ch/pdf/kpmg-ch-swiss-taxes-2026-clarity.pdf.coredownload.inline.pdf) | 31-05-2026 | "Basel-Stadt … from 13.04% to 14.53% on profits exceeding CHF 50 million, effective from 2026 … to bring the effective corporate income tax rate closer to the minimum tax of 15%" |
| admin.ch – werkgelegenheidsgroei naar controle | [admin.ch](https://www.admin.ch/de/newnsb/JYypuIwYkeNto03DLe3Sm) | 27-11-2025 | Beschäftigung 2024: inländisch kontrolliert +1,4%, ausländisch kontrolliert +0,2% |

---

## VRAAG 3 — Zwitsers partij-landschap (Nationalrat 2023–2027)

Percentages: **2023-resultaat** (BFS-gecorrigeerd, via Wikipedia/BFS) en **2025-Wahlbarometer** (SRG/sotomo, okt 2025). Leverbaarheid_2027 = engine-schatting (0–1) op basis van peilingen + regeringsdeelname (alle vier grootste in Bundesrat = "Zauberformel").

### Partij-tabel (klaar voor engine-integratie)

| Naam (voluit) | Code | Kleur | Type | 2023 % | 2025 peil % | Zetels 2023 (NR) | Leverbaarheid_2027 | Kernprogramma 2027 |
|---|---|---|---|---:|---:|---:|---:|---|
| Schweizerische Volkspartei | SVP | Donkergroen | Rechts / nationaal-conservatief / rechtspopulistisch / economisch-liberaal | 27,9 | 30,4 | 62 | 0,95 | Migration/Asyl (restrictief); tegen EU-Rahmenabkommen; sceptisch klima (tegen Netto-Null-kosten, pro Atomkraft); Landwirtschaft/Direktzahlungen (kernbasis); Neutralität/Armee-Ausbau, tegen EU-sancties; lage Steuern |
| Sozialdemokratische Partei | SP | Rood | Links / sociaaldemocratisch | 18,3 | 18,8 | 41 | 0,90 | Sozialsystem (AHV/IV-uitbreiding, Krankenkassen-Prämienentlastung, hogere lonen); Klima/Energie (uitbouw PV/Wind, Ausstieg fossiel); Vermögens-/Erbschaftssteuer omhoog; Finanzplatz-regulering na CS; migratie humaner |
| Die Mitte | MITTE | Oranje | Centrum / christendemocratisch / conservatief | 14,1 | 13,6 | 29 | 0,88 | Familien/Sozialsystem (AHV-stabilisering, Krankenkassen-Kostenbremse); pragmatische EU-Bilaterale; energie-mix incl. kernenergie-optie; Landwirtschaft; gematigde Steuern |
| FDP.Die Liberalen | FDP | Blauw (2023: magenta) | Rechts-liberaal / economisch-liberaal | 14,3 | 13,3 | 28 | 0,85 | Bilaterale/EU-Zugang; Steuern laag (tegen Vermögens-/Erbschaftssteuer); Finanzplatz-stabiliteit (proportionele bankregulering na CS); markt-klima (CO2-marktmechanismen); Armee-financiering |
| Grüne Partei der Schweiz | GRÜNE | Groen | Links / groen | 9,8 | 10,3 | 23 | 0,70 | Klima/Energie (Ausstieg Atomkraft, snelle PV/Wind-uitbouw, Netto-Null); Biodiversität/Landwirtschaft-ökologisch; sociale rechtvaardigheid; kritisch Finanzplatz; EU-integratie pro |
| Grünliberale Partei | GLP | Lichtgroen | Centrum-liberaal / groen-liberaal | 7,6 | 6,1 | 10 | 0,55 | Klima via marktmechanismen (CO2-beprijzing); EU-Bilaterale/Rahmen pro; Innovation/Digital/ICT; gematigde Steuern; AHV-hervorming |
| Evangelische Volkspartei | EVP | Geel/blauw | Centrum / christelijk-sociaal | 2,3 | 1,5 | 2 | 0,25 | Sozial-ethisch (familie, ontwikkelingssamenwerking); Klimaschutz-Schöpfungsbewahrung; gematigd migratie-humaan; ethische Finanzregulierung |
| Eidgenössisch-Demokratische Union | EDU | Blauw | Rechts / christelijk-conservatief / nationaal-conservatief | 1,2 | n.a. | 2 | 0,15 | Christelijke waarden/gezin; restrictief migratie/Asyl; tegen EU-Rahmen; conservatief-nationaal; Neutralität |
| Lega dei Ticinesi / MCG | LEGA/MCG | Blauw | Rechts / regionalistisch / rechtspopulistisch (TI/GE) | 0,55 (Lega) / 0,51 (MCG) | n.a. | 1 (Lega) / 2 (MCG) | 0,20 | Regionaal (Tessin/Genf); Grenzgänger-beperking; migratie restrictief; lokale werkgelegenheid-bescherming |

*Aanvullende partij (buiten kern-9, klein):* **Partei der Arbeit / POP (PdA)** — code PdA, kleur rood, links/communistisch, 0,72% (2023), 0 zetels NR, leverbaarheid_2027 ≈ 0,05.

### Bron-tabel Vraag 3

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| Wikipedia – Parlamentswahlen 2023 (BFS-cijfers) | [de.wikipedia.org](https://de.wikipedia.org/wiki/Schweizer_Parlamentswahlen_2023) | 2023 | SVP 27,97% (62), SP 18,27% (41), Mitte 14,06% (29), FDP 14,25% (28), Grüne 9,78% (23), GLP 7,55% (10), EVP 2,03% (2), EDU 1,23% (2), Lega 0,55% (1), MCG 0,51% (2), PdA/POP 0,72% (0) |
| SRF – Endresultat Wahlen 2023 | [srf.ch](https://www.srf.ch/news/schweiz/wahlen-2023/nationalratswahlen-2023-das-endresultat-die-svp-kann-einen-grossen-sieg-feiern) | 21-10-2023 | "SVP 28.6% / 62 Sitze"; "SP 18% / 41"; "Grüne 9.4% / 23"; Mitte 29, FDP 28, GLP 10 (Wahlsonntag-waarden, later door BFS licht gecorrigeerd) |
| sotomo – SRG Wahlbarometer 2025 | [sotomo.ch (PDF)](https://sotomo.ch/files/data/projectfile/2025/10/SRG_Wahlbarometer_2025.pdf) | okt 2025 | SVP 30,4% (+2,5pp), SP 18,8% (+0,5), Mitte 13,6% (−0,5), FDP 13,3% (−1,0), Grüne 10,3% (+0,5), GLP 6,1% (−1,5), EVP 1,5% (−0,8) |
| SRF – Wahlbarometer 2025 | [srf.ch](https://www.srf.ch/news/schweiz/zwei-jahre-vor-den-wahlen-wahlbarometer-zeigt-svp-mit-historischem-hoch-liberale-im-tief-1) | 02-10-2025 | "SVP … erstmals seit 1919 national mehr als 30 Prozent"; FDP verliest, GLP −1,5pp |
| Efekt – Parteifarben/branding | [efekt.ch](https://www.efekt.ch/de/blog-posts-de/symbole-und-farben-zum-verstandnis-des-visuellen-brandings-der-schweizer-parteien) | 16-08-2023 | SVP groen+gele zon; SP rood; FDP blauw (2023 magenta); Grüne kräftiges Grün; GLP grün+blau; Mitte oranje |
| Wikipedia – Politische Farbe | [de.wikipedia.org](https://de.wikipedia.org/wiki/Politische_Farbe) | 2024 | SVP grün, SP rot, FDP blau, Mitte orange, Grüne grün, GLP grün (hellgrün), EVP blau, EDU blau, Lega blau |

*Kanttekening:* de programma-thema's (Migration, EU-Rahmen, Klima, Sozialsystem, Steuern, Finanzplatz, Landwirtschaft, Neutralität) zijn samengevat op basis van de algemeen bekende partij-positionering; de exacte 2027-manifesten waren op peildatum nog niet gepubliceerd (verkiezingen okt 2027). Waar geen partij-specifiek 2027-manifest gefetcht is, gelden deze als engine-samenvatting, niet als geciteerd citaat.

---

## VRAAG 4 — Zwitsers sector-landschap (22 sectoren, aangepast voor CH)

**Structurele weging** (BFS BWS 2022–2024): diensten ~72–74% BWS, industrie ~25%, landbouw 0,6%. Grootste takken: verwerkend gewerbe (143 mld CHF), vastgoed (54 mld), handel (~118 mld), verzekeringen (31 mld), financiële diensten (43 mld). CH-specifieke aanpassingen: **S13 = Pharma & Life Sciences** (i.p.v. iGaming), **S17 = Precision/Uhren** (i.p.v. Shipping).

| # | Sector (CH-aangepast) | Omschrijving | Econ. gewicht | Politieke gevoeligheid |
|---|---|---|---|---|
| S1 | Health / Gesundheit | Gesundheits- & Sozialwesen (64 mld CHF BWS 2023) | Hoog & groeiend | Zeer hoog — Krankenkassen-Prämien topthema SP/Mitte |
| S2 | Education / Bildung | Erziehung & Unterricht (4,7 mld) + ETH/EPFL-onderzoek | Middel | Middel — Berufsbildung breed gesteund |
| S3 | Public Administration | Öffentliche Verwaltung (81,5 mld BWS) | Middel-hoog | Middel — federalisme/kantonale autonomie |
| S4 | Security & Defence | Armee, F-35-aankoop, Grenzwacht | Klein | Hoog — F-35, Neutralität, EU-sancties (SVP-thema) |
| S5 | Manufacturing | Verarbeitendes Gewerbe (143 mld, grootste tak) — MEM-industrie | Zeer hoog | Hoog — US-tarieven, frankappreciatie |
| S6 | Construction / Bau | Baugewerbe (38,9 mld) | Middel | Middel — Raumplanung, Zweitwohnungen |
| S7 | Transport & Logistics | Verkehr & Lagerei (29,4 mld); SBB, alpentransit | Middel | Hoog — Alpeninitiative, NEAT, Verlagerung |
| S8 | Agriculture & Fisheries | Land-/Forstwirtschaft (0,6% BWS, 5 mld) | Klein economisch | **Zeer hoog** — SVP-kernbasis, Direktzahlungen, Ernährungssicherheit |
| S9 | Retail & Wholesale | Handel/Detailhandel (~118 mld) | Hoog | Middel — Einkaufstourismus, Hochpreisinsel |
| S10 | Tourism & Hospitality | Gastgewerbe/Beherbergung (13,8 mld); Alpen, wintersport, MICE | Middel-hoog | Hoog — Bergregionen, saisonarbeit, franksterkte |
| S11 | ICT & Digital | Information & Kommunikation (35,8 mld) | Middel-hoog | Middel — Digitalisierung, e-ID, Datenschutz |
| S12 | Financial Services | **Banking, wealth management, private banking** (Fin.diensten 43 mld + Versich. 31 mld); UBS, Zurich, Swiss Re | **Zeer hoog** | **Zeer hoog** — Bankenregulierung na CS-Fall, too-big-to-fail |
| S13 | **Pharma & Life Sciences** *(CH-alt. voor iGaming)* | Novartis, Roche, Lonza; Chemie-Pharma grootste exportbron | **Zeer hoog** | Hoog — US-farma-prijsdruk, standort-concurrentie |
| S14 | Energy & Utilities | Energieversorgung (13,2 mld); Wasserkraft, Kernkraft-debat | Middel | **Zeer hoog** — Atomausstieg/-wiedereinstieg, PV/Wind, Stromabkommen EU |
| S15 | Real Estate & Rental | Grundstücks-/Wohnungswesen (53,6 mld) | Hoog | Hoog — Mietrecht, Wohnungsnot, Eigenmietwert |
| S16 | Professional Services | Freiberufl./wiss./techn. Dienstl. (62,4 mld); consulting, recht | Hoog | Middel |
| S17 | **Precision Engineering / Uhrenindustrie** *(CH-alt. voor Shipping)* | Rolex, Swatch, Richemont; Präzisionsmechanik, MedTech | Middel-hoog | Hoog — export/tarieven, franksterkte, Luxus-nachfrage |
| S18 | Culture & Arts | Kunst, Unterhaltung, Erholung (4,1 mld) | Klein | Laag-middel |
| S19 | Media & Telecoms | Medien, SRG, Swisscom, Telekom | Middel | Middel — Service-Public, SRG-Halbierungsinitiative |
| S20 | Foreign / Remote | Grenzgänger, internationale organisaties, remote-werk | Middel (regionaal hoog) | Hoog — Grenzgänger (TI/GE), Personenfreizügigkeit EU |
| S21 | Other Services | Sonstige wirtschaftl./persönl. Dienstleistungen (25,8 + 10,5 mld) | Middel | Laag |
| S22 | Not employed / Student / Retired | Rentners (AHV), Studierende, niet-werkzame bevolking | n.v.t. (demografisch) | **Zeer hoog** — AHV/IV-financiering, Renten, demografie |

### Bron-tabel Vraag 4

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| BFS – VGR BWS naar A21-branches 2023 | [bfs.admin.ch (PDF)](https://dam-api.bfs.admin.ch/hub/api/dam/assets/32257680/master) | 2024 (data 2023) | Verarb. Gewerbe 143.346; Handel 117.815; Grundstücks-/Wohnungswesen 53.627; Freiberufl. 62.355; Ö. Verwaltung 81.514; Gesundheit 64.062; Fin.dienstl. 42.594; Versich. 31.320; Gastgewerbe 13.760; Verkehr 29.445; IKT 35.845; Energie 13.240 (Mio CHF) |
| Statista – Finanzdienstleistungen BWS | [de.statista.com](https://de.statista.com/statistik/daten/studie/443357/umfrage/bruttowertschoepfung-in-der-schweiz-nach-branchen/) | 03-01-2025 | Finanzdienstleistungen 2023 "rund 41,1 Milliarden … 5,5 Prozent der Gesamtwertschöpfung … Abnahme von 10,1 Prozent" |
| Die Volkswirtschaft – Finanzsektor | [dievolkswirtschaft.ch](https://dievolkswirtschaft.ch/de/2024/10/finanzsektor-eckpfeiler-der-schweizer-wirtschaft/) | 08-10-2024 | Finanzsektor als "Eckpfeiler der Schweizer Wirtschaft" |
| KOF – Prognose (sector-tweedeling) | [kof.ethz.ch](https://kof.ethz.ch/news-und-veranstaltungen/medien/medienmitteilungen/2025/12/kof-konjunkturprognose-trotz-handelsdeal-truebe-aussichten-fuer-schweizer-wirtschaft.html) | 15-12-2025 | Pharma-Zuwächse vs. Uhren-/Maschinenexporte litten unter Zöllen |

---

## VRAAG 5 — Zwitserse regio-indeling (7 BFS-Großregionen, Q5_regio)

**Aandeel in nationaal BIP** afgeleid uit BFS-regionaal BIP 2022 (Schweiz = 791.087 mln CHF, prijzen vorig jaar).

| # | Großregion (kantons) | BIP 2022 (mln CHF) | Aandeel BIP | Dominant economisch profiel |
|---|---|---:|---:|---|
| 1 | **Genferseeregion** (GE, VD, VS) | 147.539 | ~18,7% | Internationale organisaties (UNO, WTO, WHO Genf); private banking; luxe/uurwerken (VD/GE); farma-hub (Lonza VS); wijnbouw/toerisme (VS-Alpen); veel Grenzgänger uit FR |
| 2 | **Espace Mittelland** (BE, FR, JU, NE, SO) | 156.072 | ~19,7% | Bundesverwaltung (Bern, hoofdstad); precisie-industrie/Uhrenindustrie Jurabogen (NE/JU/SO); MedTech; landbouw; Freiburg gemengd |
| 3 | **Nordwestschweiz** (BS, BL, AG) | 111.554 | ~14,1% | **Pharma/Life-Sciences cluster Basel** (Novartis, Roche); chemie; logistiek (Rijnhaven); energie (AG kerncentrales) |
| 4 | **Zürich** (ZH) | 164.495 | ~20,8% | **Financieel centrum** (banken, verzekeringen, UBS-HQ); ICT/fintech; professional services; grootste enkele economische motor |
| 5 | **Ostschweiz** (GL, SH, AR, AI, SG, GR, TG) | 98.252 | ~12,4% | Industrie/MEM (SG, TG); toerisme (GR/Graubünden — Davos, St. Moritz); landbouw; grenshandel met AT/DE/FL |
| 6 | **Zentralschweiz** (LU, UR, SZ, OW, NW, ZG) | 77.093 | ~9,7% | **Laag-belasting-hub Zug** (holdings, crypto/commodity-trading); toerisme (LU); vermogende particulieren; hoofdkantoren |
| 7 | **Tessin** (TI) | 36.084 | ~4,6% | **Grenzgänger uit Italië** (grote frontalieri-arbeidsmarkt); financiële diensten (Lugano); toerisme; logistiek/transit (Gotthard) |

### Bron-tabel Vraag 5

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| BFS – BIP nach Grossregionen/Kantonen 2022 | [bfs.admin.ch (PDF)](https://dam-api.bfs.admin.ch/hub/api/dam/assets/32627361/master) | 2024 (data 2022) | Zürich 164.495; Espace Mittelland 156.072; Genferseeregion 147.539; Nordwestschweiz 111.554; Ostschweiz 98.252; Zentralschweiz 77.093; Tessin 36.084 (Mio CHF); "Zürich … Wachstumsmotor … 0,8 Prozentpunkte" |
| BFS – Definitie Großregionen | [bfs.admin.ch (PDF)](https://www.bfs.admin.ch/bfsstatic/dam/assets/349134/master) | n.d. | "sieben Grossregionen … Genferseeregion (GE, VD, VS), Espace Mittelland (FR, BE, JU, NE, SO), Nordwestschweiz (AG, BL, BS), Zürich (ZH), Ostschweiz (AI, AR, GL, GR, SG, SH, TG), Zentralschweiz (LU, NW, OW, SZ, UR, ZG), Tessin (TI)" |
| ETH/BFS – regionale BWS-analyse | [ethz.ch (PDF)](https://ethz.ch/content/dam/ethz/special-interest/baug/irl/irl-dam/lehrveranstaltungen/msc/regional-economics/Literatur/5_Wettbewerb%20und%20Wachstum/Analyse_BfS_BIP_Komponenten.pdf) | n.d. | "Zürich (22%) und im Espace Mittelland (20%) … Genferseeregion mit 18% … diese drei … 60% der Schweizer BWS" |
| BFS – kantonale BIP-aandelen | [bfs.admin.ch (PDF)](https://dam-api.bfs.admin.ch/hub/api/dam/assets/33027172/master) | n.d. (2008–2021 gem.) | "Vier Kantone repräsentieren 49%": Zürich 21,7%, Bern 11,7%, Waadt 8,1%, Genf 7,6%; Zug 2,8%, Tessin 4,4% |

---

## VRAAG 6 — Verificatie: Zwitserland-specifieke variabelen

### Sociaal Kantelpunt (Regel 113/114) & Point of no return

CH's NEPK-startwaarde (~7,8%) ligt ruim boven DE (6,83%) en NL (3,75%), en CH is welvarend (tax-to-GDP laag, netto-ontvanger vermogen). Er is **geen gefetchte bron die een expliciete NEPK-drempel of "Sozialer Kantelpunt"-waarde voor CH definieert** — dit is een engine-construct (Regel 113/114), niet een gepubliceerde statistiek → **kantelpunt-NEPK-waarde: n.a. (engine-parameter)**.

*Historische NEPK-schokken (kwalitatief, uit gefetchte bronnen):*
- **CS-Fall 2023**: grootste systemische schok sinds decennia — zie hieronder.
- Structureel: KOF wijst op frankappreciatie + US-tarieven (39%→15%) + China-vraagzwakte als aanhoudende drukfactoren op export/NTPK ([KOF, dec 2025](https://kof.ethz.ch/news-und-veranstaltungen/medien/medienmitteilungen/2025/12/kof-konjunkturprognose-trotz-handelsdeal-truebe-aussichten-fuer-schweizer-wirtschaft.html)).

*Point of no return: **n.a.*** — geen gefetchte bron kwantificeert een structurele omslag-NEPK-waarde voor CH.

### Miljonair-migratie (Henley 2025)

CH is een duidelijke **netto-ontvanger**: geprojecteerde **netto +3.000 migrerende miljonairs in 2025**, 4e wereldwijd na UAE (+9.800), USA (+7.500) en Italië (+3.600). Tegenpolen: UK −16.500, China −7.800, India −3.500.

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| Henley & Partners – Private Wealth Migration 2025 (press) | [henleyglobal.com](https://www.henleyglobal.com/newsroom/press-releases/henley-private-wealth-migration-report-2025) | 24-06-2025 | "Switzerland +3,000 … UAE +9,800; USA +7,500; Italy +3,600; UK –16,500; China –7,800; India –3,500" |
| Henley – Country Wealth Flows | [henleyglobal.com](https://www.henleyglobal.com/publications/henley-private-wealth-migration-report-2025/country-wealth-flows) | 2025 | Interactieve landen-flows (tekstwaarden n.a. op deze subpagina) |

### UBS–Credit Suisse impact 2023 (systemic-risk-schok)

De noodovername (19 mrt 2023) was de grootste financiële-stabiliteitsschok voor CH sinds 2008:
- Deal-waarde **CHF 3 mrd** (all-stock); SNB-liquiditeit **>CHF 100 mrd** + garantie **CHF 9 mrd**.
- **AT1-obligaties CHF 16 mrd** volledig afgeschreven (grootste AT1-writedown ooit).
- Gecombineerde balans **groter dan die van de SNB**; nieuwe bank = 35% binnenlandse deposito's, 31% bedrijfsleningen, 26% hypotheken.
- Bij faillissement zou elke inwoner tot **CHF 12.500** aansprakelijk zijn.
- OESO waarschuwde (mrt 2024) dat de redding "new risks for Switzerland" creëerde.

*Partij-reacties (kwalitatief):* SP/Grüne eisten strengere **Bankenregulierung/too-big-to-fail-verscherping**; FDP pleit voor proportionele, standort-vriendelijke regulering; SVP kritisch op staatsgaranties. Deze reacties zijn samengevat uit de positionering (Vraag 3) — geen individueel partij-manifest is per stuk gefetcht → **exacte partij-quotes: n.a.**

| Bron | URL | Datum | Kernquote |
|---|---|---|---|
| Wikipedia – Acquisition of Credit Suisse by UBS | [en.wikipedia.org](https://en.wikipedia.org/wiki/Acquisition_of_Credit_Suisse_by_UBS) | 19-03-2023 | "CHF 3 billion … more than CHF 100 billion … liquidity … CHF 9 billion … guarantee … CHF 16 billion … AT1 … written down to zero … 35% of domestic deposits, 31% of corporate loans and 26% of mortgages … every person in Switzerland would be liable for up to CHF 12,500" |
| CNN – "Too big for Switzerland?" | [cnn.com](https://www.cnn.com/2023/03/23/investing/credit-suisse-ubs-impact-switzerland) | 23-03-2023 | Fusiebank "twice the size of the economy" (kop) |
| Reuters – OECD on new risks | [reuters.com](https://www.reuters.com/markets/deals/ubss-rescue-credit-suisse-has-created-new-risks-switzerland-oecd-says-2024-03-14/) | 14-03-2024 | "UBS's rescue of Credit Suisse has created new risks for Switzerland, OECD says" |
| Bundesrat – Bericht zur Bankenstabilität | [admin.ch (PDF)](https://www.newsd.admin.ch/newsd/message/attachments/87002.pdf) | 2024 | Federale evaluatie too-big-to-fail-regime na CS |
| FINMA – Lessons Learned CS | [finma.ch (PDF)](https://www.finma.ch/en/~/media/finma/dokumente/dokumentencenter/myfinma/finma-publikationen/cs-bericht/20231219-finma-bericht-cs.pdf) | 19-12-2023 | Toezichthouder-analyse CS-crisis |

---

## Overzichtstabel engine-startwaarden CH 2026

| Parameter | Waarde | Zekerheid |
|---|---:|---|
| E_tv | 0,390 | Hoog (SECO/OECD TiVA) |
| α | 0,52 | Middel (engine-afleiding uit BFS-sectorstructuur) |
| τ | 0,29 | Hoog (OECD/Eurostat/KPMG) |
| φ | 0,54 | Laag-middel (afgeleid uit omzet-/werkgelegenheids-controle; BWS-splitsing n.a.) |
| **NTPK 2026** | **14,40%** | Middel |
| **NEPK 2026** | **7,78%** (band 6,5–8,6%) | Middel |
| E_tv_pp/jaar | −0,10 pp | Middel |
| alpha/jaar | −0,003 | Middel |
| tau/jaar | +0,002 | Middel-hoog |
| phi/jaar | −0,002 | Laag |
| Miljonair-migratie 2025 | netto +3.000 (netto-ontvanger) | Hoog (Henley) |
| Sociaal kantelpunt-NEPK / Point of no return | n.a. (engine-parameter) | — |

*Onderzoek uitgevoerd 4 juli 2026. Waar deelwaarden niet uit een gefetchte bron te bevestigen zijn, is "n.a." of "engine-afleiding/-aanname" vermeld. NEPK/NTPK/α/φ zijn engine-constructen, geen officiële statistieken.*
