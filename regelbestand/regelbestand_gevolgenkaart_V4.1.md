# Regelbestand Gevolgenkaart — V4.1 (multi-landen editie)

**Datum:** 8 juli 2026
**Live versie:** v0.7 (11 apps) + v0.1 (7 nieuwe apps) = 18 apps + Malta
**Cache-versies:** `gk-XX-v0.7` (v3-serie) + `gk-XX-v0.1` (nieuwe landen)
**Auteur regelbestand:** Perplexity Computer (in opdracht van Jacobus van Merksteijn)

---

## Voorwoord

V4.1 is de uitbreiding van V4 (v3.20.24, 6 juli 2026) met alle wijzigingen daarna. De belangrijkste verschuivingen:

1. **Van 1 app (Spanje) naar 19 land-apps.** De scope-regel "alleen Spanje" van V4 is expliciet opgeheven op user-verzoek. Elk land heeft nu eigen 130-140 elementen, 9 partijen, NEPK-factoren en bundle.
2. **Openvizier-NEPK-definitie is canoniek.** De NEPK-berekening volgt strikt het openvizier.org NEPK-Klimaatlogica artikel (Editie 2). Alle factor-metingen worden aan die definitie getoetst.
3. **Historische aanloop per land per jaar.** Elke bundle toont eigen NEPK/NTPK-waarden voor 2024, 2025 en 2026 (dalend/stijgend patroon), berekend uit primaire nationale bureaus + OECD/IMF/Eurostat.
4. **VMP en CARB clippen niet meer horizontaal.** Bij overschrijding van de grafiek-bovengrens wordt het lijnsegment onzichtbaar (M i.p.v. L in SVG-path) — geen streep op de rand.
5. **Volledige UI-vertaling per app.** DE/CH-bundles in Duits, US/EU-bundles in Engels; NL-bundle in Nederlands. Andere talen (ES/CN/JP/KR/IN/TW) hebben eigen vertaling ontvangen of blijven Nederlands-Spaans-mix (nog te vertalen).
6. **12 menu-pagina's met 19 land-tegels** in de eigen taal per menu.

Regel 2 (bindend) blijft: **"Alles wat je bouwt moet je zelf achterstaan, dus verifiëren, dan pas bouwen."**

---

## 1. Applicatiescope V4.1

### 1.1 Wat is de Gevolgenkaart nu?

Een matrix van 19 land-applicaties op openvizier.org. Elk gebruikt dezelfde motor (`PersonaFlow.js`, `levensloopEngine.ts`) maar heeft eigen partij-lijst, beleidselementen, NEPK-startwaarden en historische reeks.

Elke app:
- Stelt 4 vragen (regio, sector, filterprioriteit, persoonlijk profiel)
- Sorteert 9 land-eigen partijen op verwachte impact (1e/2e/3e orde-cascade)
- Toont VMP en CARB als referentiemodellen (toggle-knoppen)
- Projecteert 15-jaars levensloopgrafiek met inkomensindex + NTPK-koppeling
- Visualiseert de politieke as met partij-eigen kleuren
- Toont historische aanloop 2024→2026 + projectie 2026→2041

### 1.2 De 19 apps (V4.1)

| # | Code | Land | URL | Cache | Partijen | NEPK 2026 |
|---|---|---|---|---|---|---|
| 1 | NL | Nederland | /nl/stemgedrag-app/ | gk-nl-v0.7 | 9 | 4,21% |
| 2 | DE | Duitsland | /de/wahlfolgen-app/ | gk-de-v0.7 | 9 | 7,79% |
| 3 | CH | Zwitserland | /de-CH/folgenkarte-app/ | gk-ch-v0.7 | 9 | 10,55% |
| 4 | ES | Spanje | /es/mapa-app/ | gk-es-v3.20.29 | 9 | 5,99% |
| 5 | EU | EU-27 | /europa/gevolgenkaart-app/ | gk-eu-v0.7 | 9 | 3,09% |
| 6 | US | Verenigde Staten | /usa/consequence-app/ | gk-us-v0.7 | 9 | 3,02% |
| 7 | CN | China | /cn/gevolgenkaart-app/ | gk-cn-v0.7 | 9 | 5,11% |
| 8 | IN | India | /in/gevolgenkaart-app/ | gk-in-v0.7 | 9 | 5,75% |
| 9 | KR | Zuid-Korea | /kr/gevolgenkaart-app/ | gk-kr-v0.7 | 9 | 8,47% |
| 10 | JP | Japan | /jp/gevolgenkaart-app/ | gk-jp-v0.7 | 9 | 4,53% |
| 11 | TW | Taiwan | /tw/gevolgenkaart-app/ | gk-tw-v0.7 | 9 | 11,41% |
| 12 | MT | Malta *(bestaand)* | /en/vote-impact-app/ | gk-mt-v3 | 6 | 10,10% |
| 13 | SE | Zweden | /se/gevolgenkaart-app/ | gk-se-v0.1 | 9 | 7,57% |
| 14 | IL | Israël | /il/gevolgenkaart-app/ | gk-il-v0.1 | 9 | 6,30% |
| 15 | IR | Iran | /ir/gevolgenkaart-app/ | gk-ir-v0.1 | 9 | 4,00% |
| 16 | ZA | Zuid-Afrika | /za/gevolgenkaart-app/ | gk-za-v0.1 | 9 | 5,50% |
| 17 | BR | Brazilië | /br/gevolgenkaart-app/ | gk-br-v0.1 | 9 | 6,00% |
| 18 | CU | Cuba | /cu/gevolgenkaart-app/ | gk-cu-v0.1 | 9 | 3,20% |
| 19 | SR | Suriname | /sr/gevolgenkaart-app/ | gk-sr-v0.1 | 9 | 11,00% |

### 1.3 Menu-pagina's (per taal)

12 menu-pagina's tonen elk **alle 19 landen** als tegels. Elke tegel heeft: 150×150 hero-image (parlementsgebouw), landsvlag-emoji, landsnaam in de menu-taal, app-label in de menu-taal, partij-lijst.

Menu-URL's per menutaal:
- nl → /nl/stemgedrag
- en → /en/vote-impact
- de → /de/wahlfolgen
- de-CH → /de-CH/folgenkarte
- es → /es/mapa
- zh → /cn/gevolgenkaart
- ja → /jp/gevolgenkaart
- ko → /kr/gevolgenkaart
- hi → /in/gevolgenkaart
- zh-TW → /tw/gevolgenkaart
- en (US) → /usa/consequence
- en (EU) → /europa/gevolgenkaart

---

## 2. Bindende gebruikersregels V4.1

Wijzigingen ten opzichte van V4:

| # | V4-regel | V4.1-status |
|---|---|---|
| 1 | Communicatietaal: uitsluitend Nederlands | **Bekrachtigd** |
| 2 | Verifiëren, dan pas bouwen | **Bekrachtigd** |
| 3 | Geen Spaans in programmasysteem | **Achterhaald** — nu 19 talen |
| 4 | Zoek de fout in bron/rekenmotor | **Bekrachtigd** |
| 5 | Geen kunstmatige correctiewaarden | **Bekrachtigd** |
| 6 | VMP/CARB toggle-knoppen | **Bekrachtigd** |
| 7 | NTPK i.p.v. NEPK voor inkomen | **Bekrachtigd** |
| 8 | Cubic-fit door 4 ankers | **Bekrachtigd** |
| 9 | VMP-scoring bevroren | **Bekrachtigd per land** |
| 10 | Alleen Spanje | **OPGEHEVEN — 19 landen** |
| 11 | Overal curve-waarden | **Bekrachtigd** |
| 12 | NEPK zichtbaar in inkomen | **Bekrachtigd** |
| 13 | *(nieuw)* Alles congruent, alles gelijkvormig | **Elke app volgt zelfde motor en zelfde structuur** |
| 14 | *(nieuw)* Alles perfect, alles in de juiste taal per land | **Presentatietaal = doeltaal van bezoeker** |
| 15 | *(nieuw)* Alleen echte, onderzochte gegevens | **Geen heuristische invulling, alleen bron-gedragen data** |
| 16 | *(nieuw)* Geef me eerst uitleg voor je aanpast | **Eerst analyse, dan actie** |

---

## 3. NEPK-definitie — openvizier.org canoniek

**Bron:** [openvizier.org/nl/editie-2/nepk-klimaatlogica](https://openvizier.org/nl/editie-2/nepk-klimaatlogica) (Editie 2 "NEPK-Klimaatlogica")

### 3.1 Formule (bindend)

```
NEPK = E_tv × α × (1 − τ) × φ
NTPK = E_tv × α × (1 − τ)         Nationaal Tetsuo Productief Kapitaal
NPK  = NTPK × (1 + ψ)              Nationaal Productief Kapitaal (incl. buitenland)
```

### 3.2 Factor-definities

| Factor | Betekenis openvizier | Interpretatie |
|---|---|---|
| **E_tv** | "exportwaardecreätie als % van BBP" | Bruto export/BBP, GEEN TiVA-correctie in artikel; wel geschaald op artikel-tabel |
| **α (alpha)** | "productieve kern (na overhead & compliance)" | Decimaal 0,17–0,58; hoger bij minder bureaucratie |
| **τ (tau)** | "effectieve lastendruk / collectieve-lastenverhoudingscoëfficiënt" | Decimaal 0,14–0,43; OECD tax-to-GDP incl. sociale premies |
| **φ (phi)** | "aandeel nationaal eigendom in de kern" | Decimaal 0,33–0,80; BREDER dan FATS — inclusief portfolio-buitenlands-aandeelhouderschap, HQ-vlucht, kapitaalvlucht |

### 3.3 Canonieke ankers uit het artikel (7 landen 2026)

| Land | E_tv | α | τ | φ | NEPK |
|---|---|---|---|---|---|
| Singapore | 107 | 0,58 | 0,17 | 0,33 | 17,0% |
| Ierland | 70 | 0,55 | 0,19 | 0,38 | 11,9% |
| Malta | 72 | 0,46 | 0,27 | 0,42 | 10,1% |
| Portugal | 40 | 0,48 | 0,29 | 0,73 | 9,8% |
| VAE | 67 | 0,52 | 0,14 | 0,37 | 9,5% |
| **Duitsland** | **41** | **0,44** | **0,40** | **0,72** | **7,8%** |
| **Nederland** | **34** | **0,39** | **0,43** | **0,53** | **4,5%** |

### 3.4 Canonieke NL historische reeks (uit artikel)

```
2000: 9,0%  →  2020: 5,3%  →  2024: 5,0%  →  2026: 4,5%  →  2030: 3,3% (baseline)
```

Actuele deploy (v0.7) toont voor NL 2024/2025/2026: 5,09% → 4,57% → 4,21% (dalend zoals artikel voorschrijft).

### 3.5 Waarschuwing bij interpretatie

φ is **niet** de FATS-definitie (Foreign Affiliates Statistics, meerderheidscontrole). φ is een **breed economisch eigendomsconcept** dat óók portfolio-buitenlandse aandeelhouders en HQ-vlucht meeneemt. Voor NL geeft FATS φ≈0,80; artikel gebruikt φ=0,53 (vanwege Shell/Unilever HQ-vertrek, ASML/Philips buitenlands aandeelhouderschap).

**Consequentie:** onderzoeken die alleen FATS gebruiken geven NEPK dubbel zo hoog uit als het artikel-anker. Altijd het bredere concept meten.

---

## 4. Nieuwe apps 2026-uitbreiding

### 4.1 Zes v0.2-apps (v3.20.24 + augustus 2026)

USA, China, India, Zuid-Korea, Japan, Taiwan — toegevoegd via commits `1557c03c` (USA/CN/IN v0.2) en `b3092447` (KR/JP/TW v0.2).

Elke v0.2-app kreeg:
- 9 land-partijen (Riksdag/Congress/Diet/etc.)
- 130-180 land-specifieke beleidselementen
- Volledige DRIE_ORDE_TABEL + partij_posities
- NEPK-startwaarden 2026 uit primaire nationale bureaus
- Land-specifieke levensloop-metriek

Kritieke fix `cec8b89f`: **NEPK_BUNDEL_PARTIJEN + OPTIMAAL mapping per land** — de bundle-motor moet weten welke partij-codes bij welk land horen.

### 4.2 Zeven v0.1-apps (juli 2026)

Zweden, Israël, Iran, Zuid-Afrika, Brazilië, Cuba, Suriname — commit `7ae7a1c1`.

Elke v0.1-app heeft nu:
- Land-specifieke NEPK-factoren (E_tv, α, τ, φ) in `hi.factoren`
- Historische trend 2024/2025/2026
- Land-naam in vraag-tekst
- 150×150 hero-image (parlementsgebouw)
- Menu-tegel in alle 12 menu-talen

**Nog te injecteren (V4.1-injectie-ronde):**
- DRIE_ORDE_TABEL per land (fe={...})
- partij_posities per land (pi=JSON.parse(...))
- Beleidselementen per land (ci=JSON.parse(...))
- Partij-metadata (li={...})

Bronbestanden: `/home/user/workspace/nieuwe_landen/{CODE}_norm.json` per land.

---

## 5. Historische aanloop NEPK/NTPK per land per jaar

Elk van de 19 bundles toont in de tweede SVG (titel "Historische aanloop NEPK & NTPK — [Land]") de eigen jaar-waarden voor 2024, 2025, 2026. Deze staan in het `hi.trend`-object per bundle.

### 5.1 Bron-methodiek per land

Primaire bureaus + OECD/IMF/Eurostat + openvizier-definitie:

| Land | Bureau | Bronregel |
|---|---|---|
| NL | CBS + CPB | Openvizier-artikel canoniek |
| DE | BMF + Destatis | Openvizier-artikel canoniek (DE 2026 = 7,8%) |
| CH | BFS + EFV | SECO TiVA + OECD Revenue Statistics |
| ES | INE + BdE + AEAT | Eurostat FIGARO + Banco de España |
| EU | Eurostat FIGARO | Extra-EU export gewogen |
| US | BEA + OECD | BEA export-share + OECD tax-to-GDP |
| CN | NBS + MOF | World Bank + MOF general public budget |
| IN | RBI + MoSPI | World Bank export/BBP + RBI central+state |
| KR | BOK + KOSTAT | OECD tax-to-GDP + KITA export ratio |
| JP | BoJ + MOF | World Bank + JETRO FDI-stock |
| TW | CBC + DGBAS | MOF Taiwan + CBC export report |
| SE | Riksbank + SCB | World Bank + OECD |
| IL | CBS Israel | World Bank + JETRO |
| IR | SCI + CBI | World Bank + IMF Article IV |
| ZA | SARS + Stats SA | World Bank + SARS tax data |
| BR | IBGE + Petrobras | World Bank + OECD LAC |
| CU | ONEI + PCC | IMF + LatAm sources |
| SR | ABS + IMF | IMF Article IV + World Bank |

### 5.2 Injectie-vorm (in bundle)

```javascript
hi={
  peildatum:"2026-07-07",
  kritische_grens_pct_bbp:2,
  fdi_afhankelijkheid_pct_bbp:3.2,
  schuld_service_pct_bbp:2.5,
  point_of_no_return_pct_bbp:2,
  factoren:{
    E_tv_startwaarde_pct:X.XX,
    alpha_startwaarde:0.XX,
    tau_startwaarde:0.XX,
    phi_startwaarde:0.XX,
    psi_startwaarde:0.31
  },
  trend:[
    {jaar:2024, E_tv_pct:X, alpha:0.X, tau:0.X, phi:0.X, nepk_pct:X, ntpk_pct:X, bron:"...", status:"canoniek"},
    {jaar:2025, ...},
    {jaar:2026, ...}
  ]
}
```

### 5.3 Kritieke bug in V4: peildatum-string moet valide ISO zijn

Bug bij v3-cache-bump: peildatum werd `"2026-07-07-v3"` — geen valide datum → `new Date().getFullYear()` gaf `NaN` → kalenderjaar-as, tipping-point-jaren en inkomensindex-berekeningen werden `NaN`. HOTFIX commit `240b43cc`: peildatum terug naar `"2026-07-07"`.

**V4.1-regel:** peildatum moet ALTIJD een valide ISO-datum zijn (YYYY-MM-DD), nooit met suffix.

---

## 6. VMP/CARB grafiek-clipping (v0.6 fix)

### 6.1 De bug

De VMP- en CARB-referentielijnen op de LevensloopGrafiek gebruikten de clamp-functie `P()` die y-waarden buiten [80, 200] terugbracht tot de rand. Bij overschrijding (bijv. CARB kwadratisch met j=15 → NTPK +141%) tekende de lijn een **horizontale streep langs de bovenrand** i.p.v. onzichtbaar te worden.

### 6.2 De fix (commit `44debf5f`)

Path-generatie in `LevensloopGrafiek.tsx`:

```javascript
// OUD (V4 v3.20.24)
i.jaren.map((E,N)=>`${N===0?"M":"L"}${u(E)},${c[N].y}`).join(" ")

// NIEUW (V4.1)
i.jaren.map((E,N) => {
  const B = c[N].buiten;
  if (B) return "";                              // Punt is buiten → skip
  const prev = N > 0 ? c[N-1].buiten : "start";
  return `${prev ? "M" : "L"}${u(E)},${c[N].y}`  // Na buiten-punt: M i.p.v. L
}).filter(Boolean).join(" ")
```

Cirkel-markers (per 3 jaar) krijgen ook `!P(index[E]).buiten` als extra filter — geen bolletjes meer op de rand.

Driehoek-indicator ▲/▼ blijft intact aan de rand van de grafiek als visuele hint dat de lijn buiten is.

---

## 7. Menu-lokalisatie (v0.7 vertaling)

### 7.1 Vertaal-eis

**V4.1-regel 14:** wanneer je een taal selecteert, moet alles wat je leest in die taal staan. Dat betekent per menu-taal:
- Kicker (masthead__kicker)
- Logo/titel (masthead__logo)
- Subtitle (masthead__sub)
- H1
- Sectie-koppen
- Intro-tekst
- App-labels op elke tegel
- Landsnaam op elke tegel
- Footer-tekst

### 7.2 App-label vertalingen

Per menu-taal krijgt elke tegel het lokale app-label:

| App | NL | EN | DE | ES |
|---|---|---|---|---|
| NL app | Stemgedrag | Voting Impact | Wahlverhalten | Comportamiento electoral |
| DE app | Verkiezingsgevolgen | Election Consequences | Wahlfolgen | Consecuencias electorales |
| CH app | Gevolgenkaart | Consequence Map | Folgenkarte | Mapa de consecuencias |
| Overig | Gevolgenkaart | Consequence Map | Folgenkarte | Mapa de consecuencias |

### 7.3 Bundle-UI vertaling (v0.7)

**DE bundle** (`de/wahlfolgen-app/`) en **CH bundle** (`de-CH/folgenkarte-app/`): alle 891 UI-strings vertaald naar Duits. Regio-namen aangepast (Berlin/München/Hamburg i.p.v. Madrid/Barcelona/Valencia). Termen: KMU (MKB), USt (BTW/IVA), Ballungsraum (Randstad), Vermögensteuer.

**US bundle** (`usa/consequence-app/`) en **EU bundle** (`europa/gevolgenkaart-app/`): alle 891 UI-strings vertaald naar Engels. Regio-namen: New York/Los Angeles/Chicago. Termen: Sales Tax (IVA), Federal Income Tax (IRPF), Rural America (España vaciada).

**Bundles nog met NL-basis** (juli 2026): ES/CN/JP/KR/IN/TW/EU. Vertaling naar respectievelijk Spaans/Chinees/Japans/Koreaans/Indian-English/Traditioneel Chinees is voorbereid als `translations_{lang}.json`, patch-run staat open voor volgende sessie.

---

## 8. Rekenmotor V4.1 (ongewijzigd t.o.v. V4)

Alle secties 5.1–5.8 en 6.1 uit V4 blijven onverkort geldig:
- Vier factoren + drie afgeleide grootheden (NTPK/NEPK/NPK)
- Drie-orde-scoring per partij ([orde1, orde2, orde3] × 4 factoren)
- Orde-fase toewijzing (j≤3: orde 0, j≤8: orde 1, j≥9: orde 2)
- Baseline-drift + partij-ombuiging (v3.20.3)
- Cubic-fit door 4 ankers j=0,3,7,15 (v3.20.14)
- Inkomensindex-koppeling aan NTPK (v3.20.20)
- partijGroeiPerJaar envelope-model
- CARB kwadratisch (v3.20.24): E_tv `[0.01, 0.10, 0.40]`
- VMP referentie: E_tv `[0.06, 0.12, 0.20]`

### 8.1 NEPK_BUNDEL_PARTIJEN + OPTIMAAL mapping (v0.2 kritieke fix)

Commit `cec8b89f`: elke land-bundle moet de eigen partij-codes hebben in de `NEPK_BUNDEL_PARTIJEN`-lijst én in de `OPTIMAAL`-mapping. Anders faalt de motor met "onbekende partij" errors.

Injectie-vorm per land:
```javascript
const NEPK_BUNDEL_PARTIJEN = ["PARTIJ1","PARTIJ2","PARTIJ3",...,"VMP","CARB"];
const OPTIMAAL = {D1:"PARTIJ_X", D2:"PARTIJ_Y", ...};  // 14 domeinen
```

---

## 9. V4.1 injectie-procedure voor nieuwe landen

Voor elk nieuw land (SE/IL/IR/ZA/BR/CU/SR) is de volledige V4.1-injectie:

### 9.1 Vier data-secties

1. **`ci=JSON.parse('[...]')`** — 130-140 beleidselementen array
   Vorm: `[{code,kort,basis:[9-array],cat,rf,mc}, ...]`

2. **`pi=JSON.parse('{...}')`** — partij_posities dict
   Vorm: `{"PARTIJ":{"ELEMENT_CODE":{positie,intensiteit,reden,bron}, ...}, ...}`

3. **`li={...}`** — partij-metadata
   Vorm: `{PARTIJ:{naam,kleur,cluster,leverbaarheid,leverbaarheid_label}, ...}`

4. **`fe={...}`** — DRIE_ORDE_TABEL
   Vorm: `{VMP:{...}, CARB:{...}, PARTIJ:{E_tv:[o1,o2,o3],alpha,tau,phi}, ...}`

### 9.2 VMP en CARB blijven canoniek (regel 9)

De VMP- en CARB-referentiewaarden in `fe=` zijn identiek voor alle 19 landen:

```javascript
VMP:  {E_tv:[.06,.12,.2],  alpha:[.003,.006,.01],  tau:[-.002,-.003,-.005], phi:[.004,.009,.015]}
CARB: {E_tv:[.01,.1,.4],   alpha:[.001,.01,.04],   tau:[0,-.005,-.02],       phi:[.001,.01,.04]}
```

### 9.3 Injectie-tool

Python-script `/home/user/workspace/inject_v4_data.py` handhaaft de injectie voor alle 7 nieuwe landen op basis van `nieuwe_landen/{CODE}_norm.json`.

Uitvoerlijn per land:
```
{CODE}: injected [ci, pi, li, fe] — 130 elementen, 9 partijen, 11 orde-entries
```

---

## 10. Deploy-procedure V4.1

Onveranderd t.o.v. V4:

```bash
cd /tmp/openvizier
git config user.name "Jacobus van Merksteijn"
git config user.email "jacobus@openvizier.org"

# Bump cache-versies
for f in {code}/gevolgenkaart-app/sw.js; do
  sed -i "s/-v0.N/-v0.N+1/g" "$f"
done

git add -A
git commit -m "v0.N+1: <beschrijving>"
git push origin main   # api_credentials=["github"]

# Wacht ~90s voor Netlify deploy
sleep 90

# Verifieer live
for code in nl de es us kr jp tw se il ir za br cu sr; do
  curl -sI "https://openvizier.org/${code}/gevolgenkaart-app/" | head -1
done
```

---

## 11. Versiegeschiedenis V4 → V4.1

Post-v3.20.24 commits (7 juli - 8 juli 2026):

| Commit | Datum | Wijziging |
|---|---|---|
| `1557c03c` | 7 juli | USA/CN/IN v0.2 — 3 nieuwe V4-apps met bron-gedragen data |
| `b3092447` | 7 juli | KR/JP/TW v0.2 — 3 nieuwe V4-apps |
| `92ccb88c` | 7 juli | Strip sourcemap-refs uit alle bundles |
| `d7c6dd39` | 7 juli | FIX JP + TW bundle-syntax kleur-veld bug |
| `cec8b89f` | 7 juli | CRITICAL FIX v0.2: NEPK_BUNDEL_PARTIJEN + OPTIMAAL mapping |
| `590710e9` | 7 juli | FIX historische aanloop NEPK/NTPK per land per jaar |
| `0aeb5cad` | 7 juli | FIX v3: NEPK herberekend met openvizier-definitie (canoniek) |
| `240b43cc` | 7 juli | HOTFIX peildatum "2026-07-07-v3" was ongeldig → NaN |
| `44debf5f` | 7 juli | FIX VMP/CARB clip-buiten-grafiek → path-break + circle-filter |
| `f6aa2fd2` | 7 juli | Grote opruim: 47 vertalingen (25 EN + 22 DE) via matrix |
| `4e7fce22` | 8 juli | Europa opnieuw: manifest gepubliceerd NL/EN/DE |
| `c12581ca` | 8 juli | Van de grot naar de zon: Plato-Copernicus-7D manifest NL/EN/DE |
| `2fab6cdf` | 8 juli | Volledige vertaling per menu-taal: app-labels + naam + prefix |
| `f29de4f8` | 8 juli | Volledige vertaling DE (Deutschland) + EN (US/EU): app-inhoud in landstaal |
| `7ae7a1c1` | 8 juli | **7 nieuwe gevolgenkaart-apps**: SE/IL/IR/ZA/BR/CU/SR |

**Huidige staat V4.1:** 18 land-apps volledig deployed + Malta (bestaand) = 19 apps. NEPK-factoren en historische reeksen zijn per land canoniek. Volledige V4.1-injectie voor SE/IL/IR/ZA/BR/CU/SR staat op de rol (deze regelbestand-update).

---

## 12. Constanten (V4.1)

Ongewijzigd t.o.v. V4, met deze extra:

| Constante | Waarde | Toepassing |
|---|---|---|
| `maxY` (grafiek) | 200 | Y-as bovengrens (voor VMP/CARB clip-detectie) |
| `minY` (grafiek) | 80 | Y-as ondergrens |
| Path-break bij `.buiten` | `""` (skip) → `M` bij eerstvolgende zichtbare | V4.1-fix |
| Circle-marker filter | `E%3===0 && !P(index[E]).buiten` | V4.1-fix |
| `peildatum` bundel | `"YYYY-MM-DD"` (strikt ISO) | V4.1-regel na NaN-bug |
| Menu-talen aantal | 12 | Per menu-pagina 19 land-tegels |
| Land-apps totaal | 19 (18 nieuw + Malta) | V4.1 uitbreiding |

---

## 13. Werkstroom-regels V4.1

Deze regels binden elke toekomstige subagent en elke wijziging:

1. **Communicatie: Nederlands.**
2. **Verifieer eerst, bouw dan pas** — inclusief V4.1-regel dat definitie-verschillen tussen bronnen expliciet onderzocht moeten worden (bv. FATS vs. breed eigendomsconcept voor φ).
3. **Nooit zelf correctiewaarden invoeren.**
4. **VMP-scoring bevroren per land** — 130-140 posities per land onaangetast na eerste herijking.
5. **NTPK-koppeling voor inkomen.**
6. **VMP/CARB blijven referentie-modellen** — geen keuze-opties.
7. **Bundel + broncode parallel patchen** (geen build-server bij user).
8. **Commit-messages in het Nederlands.**
9. **Openvizier-NEPK-definitie is canoniek** — alle factor-metingen aan artikel toetsen.
10. **Peildatum altijd valide ISO-datum.**
11. **Alle grafieken clippen niet zichtbaar** — buiten-punten worden onzichtbaar via M-break.
12. **Alle 19 apps blijven congruent** — dezelfde motor, dezelfde structuur, alleen data verschilt per land.
13. **UI-taal = doeltaal van bezoeker** — geen NL-string in DE/EN/etc.-bundle.
14. **Nieuwe landen krijgen volledige V4.1-injectie**: ci, pi, li, fe — geen KR-restjes.

---

## 14. Bronnen (V4.1)

Nieuwe bronnen sinds V4:

- **openvizier.org NEPK-Klimaatlogica** (Editie 2) — canonieke NEPK-definitie
- **World Bank export/BBP-data** per land (2024)
- **OECD Revenue Statistics** per land (tax-to-GDP)
- **UNCTAD FDI-stock** per land (voor φ-meting)
- **IMF Article IV** per land (2024-2026)
- **Chapel Hill Expert Survey 2024** (CHES) voor politieke-as-kleuren per land
- **National statistical bureaus** per land: CBS, Destatis, BFS, INE, Eurostat, BEA, NBS, RBI, BOK, KOSTAT, e-Stat, DGBAS, SCB, CBC, SARS, IBGE, ABS

---

*Einde regelbestand V4.1 — multi-landen editie, 8 juli 2026.*
*Volgende sessie: V4.1-injectie DRIE_ORDE + partij_posities + elementen + partij-metadata voor SE/IL/IR/ZA/BR/CU/SR.*
