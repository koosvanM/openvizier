# Lees eerst — voor je een script in deze map draait

De meeste scripts in deze map zijn **verouderd** en manipuleren menu's,
navigatie of pagina-inhoud buiten de canonieke matrix om. Als je zomaar iets
draait, kan je de site onherstelbaar door elkaar schoppen.

## De canonieke werkwijze

De menu-matrix wordt beheerd via **`../nl/_data/vizier.xlsx`**. Wijzigingen
daarin worden automatisch omgezet naar de vijf JSON-tabellen onder
`../nl/_data/tabellen/` door **`xlsx_naar_json.py`** — een GitHub Action draait
dit bij elke push die de xlsx wijzigt.

**Lees eerst `../tools/MATRIX-REGELS.md` voordat je iets doet.**

## Scripts die je wél mag draaien

- `xlsx_naar_json.py` — genereert de tabellen uit de xlsx (lokaal testen)
- `auto_post.py` — social-media post (aangeroepen door workflow)
- `xlsx_naar_json.py` — via workflow

## Scripts die je NIET mag draaien

Zie de verboden-scripts-lijst in `../tools/MATRIX-REGELS.md § 7`.

Kort samengevat: alles wat in de naam `menu`, `navigatie`, `nav`, of `rebuild`
heeft, is verouderd en manipuleert de site buiten de matrix om. Niet draaien.

## Bij twijfel

Doe eerst `git status` en `git diff` na een dry-run. Als een script honderden
HTML-bestanden aanpast, is het bijna zeker een verouderd batch-script dat de
xlsx-workflow doorbreekt.
