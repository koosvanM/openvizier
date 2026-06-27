# Tools voor Het Open Vizier

Hulpscripts voor onderhoud van de site.

## Link-audit & auto-fix

Twee scripts die samenwerken om gebroken interne links te detecteren en
waar mogelijk automatisch te repareren.

### `link_audit.py` — vinden

Loopt alle HTML-bestanden door en rapporteert welke `href`-attributen naar
niet-bestaande bestanden verwijzen.

```bash
# Volledig rapport in terminal
python3 tools/link_audit.py

# Alleen samenvatting
python3 tools/link_audit.py --quiet

# Ook JSON-output (voor verdere verwerking)
python3 tools/link_audit.py --json rapport.json

# Voor CI: exit-code 1 als er fouten zijn
python3 tools/link_audit.py --fail-on-errors
```

Wat wordt overgeslagen:
- `/preview/...`-paden (preview-content, niet live)
- `${...}`-template-literals (JavaScript dynamisch ingevuld)
- Externe URLs (`http://`, `https://`, `mailto:`, `tel:`)
- Anchors (`#fragment`)

### `link_fix.py` — repareren

Probeert gebroken links automatisch te repareren via de slug-cluster-mapping
in `slug_clusters.json`.

```bash
# Bestanden aanpassen
python3 tools/link_fix.py

# Eerst kijken wat er zou veranderen, zonder iets te schrijven
python3 tools/link_fix.py --dry-run

# JSON-rapport van wat is/zou worden gefixt
python3 tools/link_fix.py --json fix-rapport.json

# Voor CI: faal als er onopgeloste fouten resteren
python3 tools/link_fix.py --fail-on-unresolved
```

### `slug_clusters.json` — de datafile

Bevat de slug-vertaaltabel per taal. Drie soorten regels:

**1. `common_files`** — bestanden in taal-root (zoals `op-de-hoogte.html`)
```json
"op-de-hoogte": {
  "nl": "op-de-hoogte",
  "en": "keep-informed",
  "de": "auf-dem-laufenden"
}
```

**2. `wat_opkomt_clusters`** — losse artikelen in de "wat opkomt"-stroom
```json
{
  "_label": "Trump als spiegel",
  "nl": "trump-als-spiegel",
  "en": "trump-as-mirror",
  "de": "trump-als-spiegel"
}
```

**3. `directe_fixes`** — één-op-één padcorrecties
```json
"/en/future/verkennen.html": "/en/verkennen.html"
```

### Strategie van auto-fix

Wanneer een gebroken link wordt gevonden, probeert het script in deze volgorde:
1. Match in `directe_fixes`
2. Match op `common_files` — vertaal naar de juiste taal-slug
3. Match op `wat_opkomt_clusters` — zoek cluster waarin de slug voorkomt,
   gebruik de slug voor de doel-taal
4. Fallback-volgorde: doel-taal → EN → NL

Als alle strategieën falen blijft de link onopgelost en wordt het via
`link_audit.py` zichtbaar gemaakt. Dat is de bedoeling: liever een
duidelijke fout dan een stille verkeerde gok.

### Een nieuw cluster toevoegen

Wanneer een artikel een vertaling krijgt of een nieuw artikel in meerdere
talen verschijnt, voeg een entry toe aan `wat_opkomt_clusters` in
`slug_clusters.json`:

```json
{
  "_label": "Korte beschrijving van het artikel",
  "nl": "slug-zonder-html-extensie",
  "en": "english-slug",
  "de": "deutsche-version"
}
```

Talen die niet bestaan kun je weglaten — fallback gaat dan naar EN of NL.

### Automatische uitvoering via GitHub Actions

`.github/workflows/link-audit.yml` zorgt dat dit gebeurt:
- **Bij elke push naar main**: auto-fix draait en commit eventuele fixes terug
- **Elke maandag 06:00 UTC**: wekelijkse audit voor regressies
- **Handmatig via GitHub UI**: tab Actions → Link-audit → Run workflow

Als auto-fix niet alle fouten kan repareren, faalt de workflow met een
rapport — dan moet je `slug_clusters.json` uitbreiden of een bron-pagina
handmatig corrigeren.
