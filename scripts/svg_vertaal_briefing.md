# Vertaal SVG-tekstinhoud per taal

## Wat je gaat doen

Er zijn **16 SVG-bestanden** met Nederlandstalige tekst-elementen in `/tmp/gh-repo/assets/`. Voor jouw doeltaal zijn er al **16 kopieën** aangemaakt met suffix `.<lang>.svg` (bv. `hero-actor-vervanging.de.svg`).

Jouw taak: **vervang alle Nederlandse tekst in die 16 kopieën door de vertaling**.

## Bestanden voor jouw doeltaal

Vervang `<LANG>` door je doeltaal (`de`, `en`, of `ru`):

1. `/tmp/gh-repo/assets/wat-opkomt/actor-vervanging/hero-actor-vervanging.<LANG>.svg`
2. `/tmp/gh-repo/assets/wat-opkomt/actor-vervanging/medisch-politiek-tableau.<LANG>.svg`
3. `/tmp/gh-repo/assets/wat-opkomt/actor-vervanging/revolutie-routekaart.<LANG>.svg`
4. `/tmp/gh-repo/assets/wat-opkomt/stikstof-slaat-toe/twee-scenarios.<LANG>.svg`
5. `/tmp/gh-repo/assets/wat-opkomt/stikstof-slaat-toe/hero-stikstof-slaat-toe.<LANG>.svg`
6. `/tmp/gh-repo/assets/wat-opkomt/immuunsysteem/hero-immuunsysteem.<LANG>.svg`
7. `/tmp/gh-repo/assets/wat-opkomt/brussel-arm/hero-brussel-arm.<LANG>.svg`
8. `/tmp/gh-repo/assets/wat-opkomt/brussel-aders/hero-brussel-aders.<LANG>.svg`
9. `/tmp/gh-repo/assets/wat-opkomt/voedingslijn/hero-voedingslijn.<LANG>.svg`
10. `/tmp/gh-repo/assets/wat-opkomt/levensader/hero-levensader.<LANG>.svg`
11. `/tmp/gh-repo/assets/wat-opkomt/voedingslijn/illustratie-kompas-verouderd.<LANG>.svg`
12. `/tmp/gh-repo/assets/wat-opkomt/voedingslijn/illustratie-tempo-verschil.<LANG>.svg`
13. `/tmp/gh-repo/assets/diagrams/7d-dimensions.<LANG>.svg`
14. `/tmp/gh-repo/assets/diagrams/samenhang-stromingen.<LANG>.svg`
15. `/tmp/gh-repo/assets/wat-opkomt/voedingslijn/illustratie-wachtkamer-bestuurders.<LANG>.svg`
16. `/tmp/gh-repo/assets/diagrams/seaskin-grenslaag.<LANG>.svg`

## Werkwijze per bestand

Voor elk van de 16 bestanden:
1. Lees het SVG-bestand
2. Vind alle `<text>...</text>` en `<tspan>...</tspan>` elementen met Nederlandse tekst
3. Vervang **alleen de tekstinhoud** door de vertaling — laat alle XML-attributen, kleuren, coordinaten, `<rect>`, `<circle>`, `<path>`, `<g>` etc. **ongewijzigd**
4. Schrijf het bestand terug op dezelfde plek

## Verboden — NIET doen

- ❌ Geen XML-attributen wijzigen (x, y, font-size, fill, transform, class, id)
- ❌ Geen elementen toevoegen of weghalen
- ❌ Geen viewBox of width/height aanpassen
- ❌ Geen `<style>`-blok wijzigen (kleuren behouden)
- ❌ Geen geometrie wijzigen (paden, rechthoeken, cirkels)

## Wat WEL doen

- ✅ Vertaal de tekstinhoud tussen `<text>...</text>` en `<tspan>...</tspan>`
- ✅ Houd zelfde lengte zoveel mogelijk — extreem lange vertalingen lopen uit het kader
- ✅ Behoud unicode-tekens (€, °, ², etc.)
- ✅ Behoud regel-afbrekingen via `<tspan x="..." dy="...">` — vertaal binnen die structuur

## Stijl & glossarium

Gebruik dezelfde toon als de artikelen: hard, snijdend, geen overbodige woorden.

### Glossarium

| NL | DE | EN | RU |
|---|---|---|---|
| anti-immuunziekte | Anti-Immunkrankheit | anti-immune disease | анти-иммунная болезнь |
| auto-immuunziekte | Autoimmunkrankheit | autoimmune disease | аутоиммунная болезнь |
| levensader | Lebensader | lifeline | жизненная артерия |
| MKB | KMU | SME | МСП |
| DGA | GGF | owner-director | директор-собственник |
| Treg-cel | Treg-Zelle | Treg cell | T-reg клетка |
| voedingslijn | Versorgungslinie | feeding line | линия снабжения |
| de leiding | die Führung | the leadership | руководство |
| boer/boeren | Bauer/Bauern | farmer/farmers | фермер/фермеры |
| Den Haag | Den Haag | The Hague | Гаага |
| Brussel | Brüssel | Brussels | Брюссель |
| LAAG 1/2/3/4 | EBENE 1/2/3/4 | LAYER 1/2/3/4 | СЛОЙ 1/2/3/4 |
| KIND | KIND | CHILD | РЕБЁНОК |
| SCHOLING | SCHULBILDUNG | SCHOOLING | ОБРАЗОВАНИЕ |
| VOLWASSENE | ERWACHSENE/R | ADULT | ВЗРОСЛЫЙ |
| ACTOR | AKTEUR | ACTOR | АКТОР |
| DIAGNOSE | DIAGNOSE | DIAGNOSIS | ДИАГНОЗ |
| RECEPT | REZEPT | RECIPE | РЕЦЕПТ |
| OPLOSSING | LÖSUNG | SOLUTION | РЕШЕНИЕ |
| oergevoel | Urgefühl | primal sense | первобытное чувство |
| hervorming | Reform | reform | реформа |
| vervanging | Ersetzung | replacement | замена |

## CIJFERS

Behoud exact:
- CBAM €75,36/ton (DE/RU) of €75.36/ton (EN met punt-decimaal voor EN, of houd komma — kies één)
- ETS €60-€75/ton
- Lbv-uitkoop €212.795/kg (DE/RU komma-duizend, EN: €212,795/kg)
- BiCRS €40/ton
- 400 ton biomassa/ha → 200 ton CO₂/ha/jaar
- Pillar Two 15%
- 30 juni 2026 → 30. Juni 2026 (DE), 30 June 2026 (EN), 30 июня 2026 (RU)

## Klaar

Aan het eind: rapporteer welke 16 bestanden je hebt vertaald (lijst met absoluut pad). Geen Git-actie.
