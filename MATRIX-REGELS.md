# Regelbestand — menu-matrix van openvizier.org

Hoe de menu-navigatie van Het Open Vizier werkelijk werkt, en hoe je een
artikel op de juiste plek in de matrix inschrijft — zodat het **daadwerkelijk
zichtbaar wordt** op de site.

Laatst bijgewerkt: 3 juli 2026.

---

## 0. Gouden regel — één bron, geen zijingangen

**De ene canonieke bron is `nl/_data/vizier.xlsx`.**

Alles wat de bezoeker in het bovenmenu, in `verkennen/`, in de cirkelnavigatie
en in de artikellijsten ziet, wordt uiteindelijk gerenderd uit die xlsx via
`scripts/xlsx_naar_json.py`, dat de vijf JSON-tabellen onder
`nl/_data/tabellen/` opnieuw wegschrijft.

Er is een GitHub Action die dit script **automatisch draait bij elke push die
`vizier.xlsx` wijzigt**. Dat betekent:

- **Wijzig je alleen de JSON-tabellen**, dan overleeft je wijziging tot iemand
  de xlsx bewerkt en pusht — daarna wordt alles overschreven en weggegooid.
- **Wijzig je alleen de xlsx**, dan draait de Action en worden de tabellen
  automatisch bijgewerkt.
- **Wijzig je beide**, dan wint de xlsx bij de eerstvolgende push.

**Werkregel:** wijzig altijd in de xlsx en laat de Action de tabellen
regenereren. Als je in nood direct de tabellen bewerkt, moet je **in dezelfde
commit ook de xlsx bijwerken**, anders is de fix van korte duur.

**Verboden zijingangen:**

- ~~`nl/_data/structuur.json`~~ — verwijderd op 3 juli 2026. Was een oude
  losstaande variant die nergens werd gelezen.
- ~~`nl/_data/layouts.json`~~ — verwijderd op 3 juli 2026. Idem.
- Losse HTML-hard-coded menu-items op `<taal>/index.html` — **mag alleen als
  voorpagina-highlight**, niet als de canonieke menustructuur. De matrix
  bepaalt het menu, niet omgekeerd.
- Scripts in `scripts/` die menu's genereren zonder via de xlsx te gaan
  (`menu_definitie.py`, `installeer_navigatie_universeel.py`,
  `rebuild_alle_menus.py`, enz.). Zie §7 voor het verboden-scripts-register.

---

## 1. Anatomie van de matrix

### 1.1 De 5 tabellen (auto-gegenereerd uit vizier.xlsx)

```
nl/_data/tabellen/1_knopen.json          # Skelet, alle talen samen
nl/_data/tabellen/2_routes_<taal>.json   # URL-routes per taal
nl/_data/tabellen/3_beelden.json         # Hero-afbeelding per code
nl/_data/tabellen/4_teksten_<taal>.json  # Naam, ondertitel, beschrijving per taal
nl/_data/tabellen/5_layouts.json         # Render-opties
```

**Wie leest de tabellen:**

- `<taal>/verkennen.html` en `<taal>/verkennen-embed.html` — de publieke matrix
- `nl/structuur.html` — beheer-pagina (noindex/nofollow)

### 1.2 Codering

Elke knoop heeft een code `N.N.N.N...` (onbeperkte diepte).

**Eerste cijfer = taal-ID:**

| Cijfer | Taal | URL-map |
|--------|------|---------|
| 1 | Nederlands | `nl/` |
| 2 | English | `en/` |
| 3 | Deutsch | `de/` |
| 4 | Русский | `ru/` |
| 5 | Français | `fr/` |
| 6 | Español | `es/` |
| 7 | Italiano | `it/` |
| 8 | Português | `pt/` |

Onder elke taal zit standaard dezelfde substructuur op niveau 2:

| Code | Type | Naam (NL-voorbeeld) |
|------|------|---------------------|
| `<T>.1` | `ingang` | Bladeren |
| `<T>.2` | `ingang` | Verdiepen |
| `<T>.3` | `ingang` | Onderzoeken |

Onder `<T>.1` Bladeren:

| Code | Naam |
|------|------|
| `<T>.1.1` | Laatste artikelen (chronologisch) |
| `<T>.1.2` | De voorpagina |
| `<T>.1.3` | Edities |

Onder `<T>.1.3` Edities zitten alle themadelen. Voor NL bijvoorbeeld:

| Code | Editie |
|------|--------|
| `1.1.3.1` | Editie 0 — Europa |
| `1.1.3.2` | Editie 1 |
| `1.1.3.3` | Editie 2 — Thermostaat/Belastingbeleid |
| `1.1.3.4` | Editie 3 — Oergevoel |
| … | … |

**Historische data-inconsistentie:** de editie-nummers zijn niet 1-op-1 gelijk
over talen. NL Editie 2 = `1.1.3.3`, maar bij EN staat Edition 2 op
`3.1.3.3` en bij DE Ausgabe 2 op `2.1.3.3` (EN gebruikt DE's slot, DE gebruikt
EN's slot — historisch gegroeid). **Zoek altijd op URL of naam** voordat je
aanneemt welke code een editie heeft in een andere taal.

### 1.3 Types

| Type | Betekenis | Voorbeeld |
|------|-----------|-----------|
| `talenring` | Wortel (bestaat 1x, code `0`) | Het Open Vizier |
| `taal` | Talige rootknoop | code `1` = NL |
| `ingang` | Hoofdrubriek | Bladeren / Verdiepen / Onderzoeken |
| `onderwerp` | Sub-rubriek onder ingang | Laatste artikelen |
| `richting` | Themadraad onder onderwerp | Gevolgenkaarten NL |
| `serie` | Reeks artikelen met kop | De Grote Plundering |
| `sub-rubriek` | Extra tussenniveau | zelden gebruikt |
| `artikel` | Eindpunt met URL | De matrix van de uittocht |

### 1.4 Statusvelden

| Veld | Waarden | Betekenis |
|------|---------|-----------|
| `status` | `live` / `concept` | Concept wordt niet getoond aan lezers |
| `actief` | `true` / `false` | `false` = verborgen zonder verwijderen |

---

## 2. Kolommen per tabel (JSON-schema)

### 2.1 `1_knopen.json`

```json
{
  "code":     "1.1.1.17",
  "ouder":    "1.1.1",
  "type":     "artikel",
  "status":   "live",
  "volgorde": "17",
  "actief":   true
}
```

### 2.2 `2_routes_<taal>.json`

```json
{
  "code":              "1.1.1.17",
  "url":               "wat-opkomt/moet-nederland-ook-volgen.html",
  "doel_open":         "self",
  "terug_naar":        "",
  "klik_actie":        "auto",
  "versie_uitgebreid": "",
  "versie_kort":       "",
  "audio_nl":          "",
  "audio_de":          "",
  "audio_en":          "",
  "audio_ru":          "",
  "video_url":         "",
  "transcript":        "",
  "pdf_download":      "",
  "delen_url":         ""
}
```

**URL-conventie:** relatief vanaf `<taal>/`. Voor een artikel onder
`nl/wat-opkomt/…` schrijf je alleen `wat-opkomt/….html` — niet met leading
slash, niet met `../`.

### 2.3 `3_beelden.json`

```json
{
  "code":         "1.1.1.17",
  "hero":         "../assets/wat-opkomt/H_matrix_uittocht.jpg",
  "hero_positie": "center",
  "hero_filter":  "standaard",
  "hero_alt":     ""
}
```

**Filter-opties** (uit `_meta.filter_definities`):

| Filter | CSS-effect |
|--------|-----------|
| `geen` | geen filter |
| `standaard` | `sepia(.35) brightness(.85) contrast(1.05)` |
| `licht` | `sepia(.20) brightness(1.00) contrast(1.05)` |
| `donker` | `sepia(.55) brightness(.55) contrast(1.10)` |
| `helder` | `sepia(.10) brightness(1.05) contrast(1.05)` |
| `sepia-zwaar` | `sepia(.85) brightness(.75) contrast(1.20)` |

**Hero-conventie:** bestandsnaam `H_<slug>.jpg`, formaat **896×1200 (portret,
3:4)**, JPEG quality 85, ±300–800 kB.

### 2.4 `4_teksten_<taal>.json`

```json
{
  "code":             "1.1.1.17",
  "naam":             "Moet Nederland ook volgen?",
  "ondertitel":       "Laten wij onze industrie zakken?",
  "beschrijving":     "Duitsland ontlast €10 mrd/jaar …",
  "tekst_positie":    "auto",
  "tekst_kleur":      "licht",
  "notitie":          "",
  "tags":             "stemgedrag, belastingbeleid, matrix",
  "auteur":           "Jacobus van Merksteijn",
  "datum_publicatie": "2026-07-03",
  "gerelateerd":      ""
}
```

### 2.5 `5_layouts.json`

Blijf hiervan af. De layouts (`1`…`5` / `9`) beschrijven de tegel-arrangementen
die de matrix rendert. Alleen wijzigen wanneer je bewust een nieuw layouttype
toevoegt.

---

## 3. Werkwijze — nieuw artikel publiceren

Voor een drietalige publicatie (NL/EN/DE) doorloop je onderstaande zes stappen.

### 3.1 Bestanden aanmaken

```
nl/wat-opkomt/<slug-nl>.html
en/what-surfaces/<slug-en>.html
de/was-aufkommt/<slug-de>.html
assets/wat-opkomt/H_<gemeenschappelijke-slug>.jpg     # 896×1200 JPEG
```

### 3.2 Xlsx bewerken

Open **`nl/_data/vizier.xlsx`**, ga naar tabblad **Knopen**. Voeg voor elke taal
en elk artikel-plaatsing één regel toe. Voor een tweetalige publicatie met
kruisverwijzing onder Editie 2 = **12 rijen** (2 artikelen × 3 talen × 2
plekken):

Kolommen die je invult (niet-lege waarden):

| Kolom | Waarde |
|-------|--------|
| Code | bijv. `1.1.1.17` |
| Ouder | bijv. `1.1.1` |
| Taal | `nl` / `en` / `de` |
| Type | `artikel` |
| Naam | titel |
| Ondertitel | subtitel |
| Beschrijving | leadtekst |
| URL | `wat-opkomt/….html` |
| Hero | `../assets/wat-opkomt/H_….jpg` |
| Hero-positie | `center` |
| Hero-filter | `standaard` |
| Tekst-positie | `auto` |
| Tekst-kleur | `licht` |
| Terug naar | (voor kruisverwijzing: code van de editie) |
| Status | `live` |
| Volgorde | volgnummer onder de ouder |
| Actief | `TRUE` |
| Auteur | `Jacobus van Merksteijn` |
| Datum publicatie | `YYYY-MM-DD` |
| Tags | comma-gescheiden |

### 3.3 Volgende volgnummer bepalen

Voor elke ouder-code: kijk in de xlsx welke `Volgorde`-nummers al bestaan onder
die ouder, neem het volgende. Voor de code doe je hetzelfde: laatste segment
+1.

### 3.4 Kruisverwijzingen

Als een artikel logisch onder meerdere plekken hoort (bijv. onder Laatste
artikelen én onder Editie 2), maak dan **twee aparte rijen** met dezelfde URL
maar verschillende codes. Zet in de tweede rij `Terug naar` op de code van de
editie zodat de "terug"-knop de lezer weer daar aflevert.

### 3.5 Regeneratie & audit

Push naar `main`. De GitHub Action detecteert de xlsx-wijziging en draait
`xlsx_naar_json.py` automatisch. Om zelf lokaal te verifiëren voor de push:

```bash
python3 scripts/xlsx_naar_json.py
python3 tools/link_audit.py
```

De link-audit moet 0 gebroken links tonen. Als er iets breekt, staat er
waarschijnlijk een URL in de xlsx die naar een niet-bestaand bestand wijst.

### 3.6 Voorpagina bijwerken (verplicht bij elke publicatie)

Dit is de dagkrant-regel (zie § 4.1). Voeg voor elk nieuw artikel één
`<a class="home-wo__rij-breed">` toe direct ná `<div class="home-wo__kop">...</div>`
in `<section class="home-wo">`, voor NL/EN/DE. Gebruik `style="margin-top:1rem;margin-bottom:2rem;"`.
Oudere lead-blokken en de `home-wo__rijen`-container schuiven een positie omlaag.

**Geen zij-ingangen** — gebruik nooit ad-hoc top-banners zoals `.pl-top`,
`.klm-pl`, `.disc-top`, `.gem-top`, `.dgk-top` of eigen `<style>`-blokken
boven `.home-wo`. Één patroon: `home-wo__rij-breed` binnen `.home-wo`.

### 3.7 Live-verificatie

Na Netlify-deploy (±90 s):

- `https://openvizier.org/<taal>/` — controleer of het artikel als **eerste**
  item op de voorpagina verschijnt (dagkrant-regel)
- `https://openvizier.org/<taal>/wat-opkomt/` — controleer of het **bovenaan**
  de chronologische lijst staat
- `https://openvizier.org/<taal>/verkennen.html` — controleer of het artikel
  als tegel in de matrix verschijnt
- De directe artikel-URL zelf → HTTP 200
- De editie-landingspagina waar je een kruisverwijzing plaatste

---

## 4. Voorpagina en Nieuw — volgorderegel

De voorpagina en het "Nieuw"-overzicht zijn de **dagkrant** van Het Open Vizier.
De volgorderegel is simpel en absoluut:

> **Het laatste artikel staat altijd bovenaan. Chronologisch nieuws-eerst.**

Deze regel geldt op twee plekken:

### 4.1 Voorpagina (`<taal>/index.html`)

Het `★ Wat opkomt` / `★ What surfaces` / `★ Was aufkommt`-blok bovenaan de
voorpagina is **handmatig** onderhouden — het wordt niet automatisch uit de
matrix opgehaald. Voor elke nieuwe publicatie voeg je een `<a class="home-wo__rij-breed">`
blok toe op de **absolute top** van `<section class="home-wo">`, direct na
`<div class="home-wo__kop">...</div>` en bóven alle bestaande rijen — inclusief
boven eventuele redactionele lead-blokken (zoals "Editie Klimaat", "Wie zijn
opbouwers wegjaagt", "Soevereiniteit als cyclus") en bóven de
`home-wo__kaart_kop "Aanbevolen om opnieuw te lezen"` / `home-wo__rijen`-container.

**Er mag geen "lead-artikel" of "discussiestuk" boven het nieuwste artikel
blijven staan.** De voorpagina is een krant, geen vitrine. Oudere redactionele
lead-blokken schuiven een positie omlaag zodra er iets nieuws verschijnt.

**DOM-structuur van `<section class="home-wo">`, in volgorde:**

```
<section class="home-wo">
  <div class="home-wo__kop"> … </div>          <!-- ★ label + intro -->

  <!-- 1. NIEUWSTE ARTIKEL — dagkrant-rij (verplicht bij elke publicatie) -->
  <a class="home-wo__rij-breed" style="margin-top:1rem;margin-bottom:2rem;"> … </a>

  <!-- 2. Vaste editorial-leads (★ edities / discussiestukken), ná de dagkrant-rij -->
  <a class="home-wo__rij-breed" style="margin-bottom:2rem;..."> … </a>
  <a class="home-wo__rij-breed" style="margin-bottom:2rem;..."> … </a>

  <!-- 3. "Aanbevolen om opnieuw te lezen" — chronologische rijen-container -->
  <p class="home-wo__kaart_kop">Aanbevolen om opnieuw te lezen</p>
  <div class="home-wo__rijen">
    <a class="home-wo__rij-breed"> … </a>
    …
  </div>
</section>
```

**Losse zij-ingangen (`.pl-top`, `.klm-pl`, `.disc-top`, `.gem-top`, `.dgk-top`,
en alle andere ad-hoc top-banner-klassen) zijn verboden voor nieuwe publicaties.**
Bestaande zij-ingangen in `<taal>/index.html` worden bij de volgende publicatie
omgezet naar `home-wo__rij-breed` of verwijderd. Één consistent HTML-patroon:
`home-wo__rij-breed` binnen `<section class="home-wo">`.

### 4.2 Nieuw (`<taal>/wat-opkomt/`)

De index-pagina van Nieuw moet artikelen tonen in **omgekeerde chronologische
volgorde**: het meest recente artikel bovenaan, dan aflopend.

Dit werkt automatisch als je in de xlsx per artikel het `Volgorde`-veld invult
én de sortering van `wat-opkomt/index.html` op datum staat. Bij twijfel:
controleer de eerste drie items van de live-pagina na deploy — als jouw nieuwe
artikel niet op positie 1 staat, moet je de `wo-item`-blokken in
`nl/wat-opkomt/index.html` handmatig herordenen (en de EN/DE-equivalenten).

### 4.3 Waar dit niet geldt

Editie-landingspagina's (`editie-2/`, `editie-klimaat/`, enz.) volgen **niet**
de chronologische regel — die zijn thematisch geordend en respecteren de
volgorde die in de xlsx is opgegeven onder de betreffende editie-code.

---

## 5. Veelvoorkomende valkuilen

1. **Alleen JSON-tabellen bewerken zonder xlsx.** Volgende xlsx-push wist het.
   → Altijd via de xlsx.

2. **Alleen HTML plaatsen zonder matrix-inschrijving.** De pagina bestaat op de
   URL, maar verschijnt niet in `verkennen/`, niet in de cirkelnavigatie, niet
   in artikellijsten. HTML alleen is niet genoeg.

3. **`Volgorde` niet gezet of dubbel.** Zonder unieke volgorde per ouder komt
   het artikel op onvoorspelbare plek te staan.

4. **URL relatief-fout.** Vanuit de routes-tabel is de URL relatief aan
   `<taal>/`. Dus alleen `wat-opkomt/foo.html`, niet `/nl/wat-opkomt/foo.html`
   en niet `../nl/wat-opkomt/foo.html`.

5. **Hero relatief-fout.** In beelden-tabel is de hero-URL relatief aan
   `<taal>/`. Dus `../assets/wat-opkomt/H_foo.jpg` (twee puntjes).

6. **Editie-code aannemen.** De code van een editie is niet in elke taal
   hetzelfde nummer. Zoek altijd op URL (`edition-2/` / `ausgabe-2/`) of naam
   voordat je een kruisverwijzing inschrijft.

7. **Status = `concept` vergeten om te zetten.** Concepten worden niet
   getoond. Zet op `live` voor publicatie.

8. **`Actief` per ongeluk op `FALSE`.** Alles wat live moet, moet `TRUE`.

9. **Verouderde scripts draaien.** Zie §7.

10. **Dagkrant-regel op de voorpagina vergeten.** Nieuw artikel dat wel in
    `wat-opkomt/` staat maar niet als eerste op de voorpagina prijkt, doet de
    site aan als een archief in plaats van een krant. Zie §4.1 — elk nieuw
    artikel is de eerste `home-wo__rij-breed`, oudere leads schuiven omlaag.

11. **Volgorde op `wat-opkomt/`-index niet omgekeerd chronologisch.** Als je
    nieuwe artikelen achteraan hebt geplakt in plaats van bovenaan, staat het
    laatste artikel onderaan de lijst. Nieuwste bovenaan, altijd. Zie §4.2.

---

## 6. Checklist per publicatie

- [ ] HTML-artikel bestaat op de juiste `<taal>/<map>/<slug>.html`
- [ ] Hero-afbeelding staat als 896×1200 JPEG in `assets/wat-opkomt/`
- [ ] `nl/_data/vizier.xlsx` heeft nieuwe rij(en) op tabblad **Knopen**
- [ ] Per rij ingevuld: Code, Ouder, Taal, Type=artikel, Naam, Ondertitel,
      Beschrijving, URL, Hero, Hero-positie, Hero-filter, Tekst-positie,
      Tekst-kleur, Status=live, Volgorde, Actief=TRUE, Auteur, Datum
- [ ] Voor kruisverwijzingen: extra rij met dezelfde URL, andere Ouder-code,
      `Terug naar` ingevuld
- [ ] **Dagkrant-regel voorpagina**: nieuw artikel als **eerste**
      `<a class="home-wo__rij-breed">` binnen `<section class="home-wo">`,
      direct ná `<div class="home-wo__kop">...</div>`, in NL/EN/DE.
      Oudere lead-items (Editie Klimaat, Opbouwers, enz.) staan erónder.
- [ ] **Geen zij-ingangen** — geen `.pl-top`, `.klm-pl`, `.disc-top`, `.gem-top`,
      `.dgk-top` of andere ad-hoc top-banners toegevoegd of achtergelaten
- [ ] **Dagkrant-regel Nieuw**: nieuw artikel als **eerste** `wo-item` in
      `<taal>/wat-opkomt/index.html` (en EN/DE-equivalenten); oudere items zijn
      een positie omlaag geschoven
- [ ] `python3 scripts/xlsx_naar_json.py` lokaal gedraaid → geen fouten
- [ ] `python3 tools/link_audit.py` → 0 gebroken links
- [ ] Commit + push naar `main`
- [ ] Live-check: nieuw artikel staat als éérste op de voorpagina van elke taal
- [ ] Live-check: nieuw artikel staat bovenaan `wat-opkomt/` van elke taal
- [ ] Live-check: HTTP 200 op de nieuwe URLs, zichtbaar in `verkennen/`

---

## 7. Verboden-scripts-register

Onderstaande scripts in `scripts/` genereren of manipuleren menu's/navigatie
**buiten de xlsx om** en mogen niet meer worden gedraaid. Ze zijn historisch
in de repo maar hun output is achterhaald door de xlsx-workflow.

- `menu_definitie.py` — hard-coded menu-definitie, onvolledig
- `installeer_navigatie_universeel.py` — schrijft menu's over
- `rebuild_alle_menus.py` — overschrijft nav-blokken sitebreed
- `remove_menu_talenring.py` — inconsistent met huidige structuur
- `ruim_dubbel_menu.py` — verwarde artefacten
- `uniform_menu.py` — negeert xlsx
- `vertaal_navigatie.py` — outdated
- `vertaal_navigatie_4_talen.py` — outdated
- `voeg_navmobile_script_toe.py` — legitiem alleen voor mobile-nav-JS
- `voeg_stemgedrag_menu_toe.py` — ad-hoc script, taak volbracht
- `audit_menus.py` — leesalleen, mag gedraaid worden
- `menu_fixes.py` — verwarrend, wordt niet meer gebruikt

De enige scripts die je hoort te draaien voor matrix-werk zijn:

- `scripts/xlsx_naar_json.py` (bij lokale test; GitHub Action doet het anders
  automatisch)
- `tools/link_audit.py` (verificatie)
- `tools/link_fix.py` (alleen bij bewuste hernoemingen)

---

## 8. Notities voor toekomstige agents

- Nooit `nl/_data/structuur.json` of `nl/_data/layouts.json` opnieuw aanmaken.
  Ze zijn met opzet verwijderd op 3 juli 2026 als vluchtroute.
- Nooit de matrix-JSON-tabellen bewerken zonder gelijktijdig de xlsx bij te
  werken. De xlsx wint bij de eerstvolgende push.
- Bij twijfel: lees dit bestand opnieuw voordat je iets aanraakt in
  `nl/_data/` of in `scripts/`.
