# Canonieke menuconfigurator

**Enige bron van waarheid**: `nl/_data/menu-config.yaml`

## Workflow

```
menu-config.yaml   →   menu_bouwen.py   →   { menu/{taal}.json ,  {taal}/index.html }
     ↑                                                                ↑
     |                                                                |
  handmatig                                                     nooit handmatig
  bewerken                                                      bewerken op de
                                                                voorpagina's
```

## Wat wijzigen?

### Menu-item toevoegen

Voeg een nieuw item toe onder een `groepen[].items:` in `menu-config.yaml`:

```yaml
- key: nieuwe_editie
  labels: {nl: Titel NL, en: Title EN, de: Titel DE, ru: Заголовок}
  urls:   {nl: "editie-nieuw/", en: "new-edition/", de: "ausgabe-neu/", ru: ""}
```

Laat `urls[<taal>]` leeg om terug te vallen op de NL-versie (dan wordt de
link `../nl/editie-nieuw/`). De fallback-link krijgt in het menu een
cursieve grijze stijl (`.ov-nav__fallback`).

### Groep hernoemen

Pas `labels` aan onder de betreffende `groepen[]`-entry.

### Volgorde wijzigen

Herorden `groepen[]` of `items[]` in de YAML. De volgorde in YAML is de
volgorde op de pagina.

### Sub-rubriek toevoegen

Voeg `sub_van: <parent_key>` toe. Sub-items worden ingesprongen onder
hun parent gerenderd (zoals Fundament/Europese kaarten onder Gevolgenkaarten).

### Scheidingslijn

Voeg `scheiding_boven: true` toe aan een item om er een `<hr>` boven te zetten
(zoals tussen de 7 hoofdedities en de 4 losse edities).

## Uitvoeren

```bash
# Regenereer alles (JSON + HTML)
python3 scripts/menu_bouwen.py

# Alleen tonen wat het zou doen
python3 scripts/menu_bouwen.py --dry-run

# Alleen bepaalde talen
python3 scripts/menu_bouwen.py --only nl,ru
```

## Wat het script doet

1. Leest `nl/_data/menu-config.yaml`
2. Schrijft `nl/_data/menu/{taal}.json` — machine-leesbare structuur per taal
3. Vervangt het eerste `<nav>...</nav>` blok in `{taal}/index.html`
4. Verwijdert eerdere `ov-nav v2` CSS/JS blokken
5. Injecteert verse CSS vóór `</head>` en JS vóór `</body>`

Idempotent: herhaalde runs geven identieke output.

## Nooit doen

- **Nooit** het `<nav>`-blok op de voorpagina's handmatig bewerken. De volgende
  `menu_bouwen.py`-run gooit dat overheen.
- **Nooit** de JSON's in `nl/_data/menu/` handmatig bewerken. Ze worden
  gegenereerd.

## Uitbreiden naar meer talen

Voeg een taalcode toe aan `talen:` en aan elke `labels:`/`urls:`-dict. Als
`urls[<taal>]` leeg blijft, valt de link terug op NL.

## Nawoord

Deze configurator vervangt de hardgecodeerde MENUS-dict in
`scripts/menu_definitie.py` voor de voorpagina's. De legacy nav op
artikelpagina's blijft (voorlopig) via de oude scripts lopen.
