# Vertaalopdracht — 11 NL-artikelen naar 1 doeltaal

## Mappenstructuur

- Bron: `/tmp/gh-repo/nl/wat-opkomt/`
- Doel DE: `/tmp/gh-repo/de/was-aufkommt/`
- Doel EN: `/tmp/gh-repo/en/what-surfaces/`
- Doel RU: `/tmp/gh-repo/ru/chto-vsplyvaet/`

## Slug-conventie

Lees `/tmp/gh-repo/scripts/slugmap.json` voor de exacte doelbestandsnamen per taal.

## Stijl & toon (van de auteur Jacobus van Merksteijn)

1. **Hard, scherp, snijdend**. Elke zin moet snijden. Geen omslachtigheid.
2. **Veel woorden vetgedrukt** (`<strong>`) — concrete cijfers, kerntermen, technische termen.
3. **Geen lange zinsneden** — die worden niet gelezen.
4. **Klemtoonregels**:
   - "anti-immuunziekte" boven "auto-immuunziekte" in titels en kernzinnen
   - Structuur in betogen: **analyse → medische parallel → oplossing**
   - Geen "7d-denkraam" terminologie
5. **Cijfers exact behouden**:
   - CBAM: €75,36/ton CO₂, €2,1 mld/kwartaal
   - ETS: €60-€75/ton, gratis allocatie 97,5%→0% in 2034
   - Pillar Two: 15% minimum-tax, GIR-deadline 30 juni 2026
   - Lbv-uitkoop: €212.795/kg stikstof
   - Carbon-Alert BiCRS: €40/ton (productiekosten €22-€28), 400 ton biomassa/ha → 200 ton CO₂/ha/jaar
   - Congo 2,8 Mha = €22,4 mld/jr; Indonesië 2,1 Mha = €16,8 mld/jr

## Vertaalglossaire (verplicht gebruiken)

| NL | DE | EN | RU |
|---|---|---|---|
| anti-immuunziekte | Anti-Immunkrankheit | anti-immune disease | анти-иммунная болезнь |
| auto-immuunziekte | Autoimmunkrankheit | autoimmune disease | аутоиммунная болезнь |
| levensader(s) | Lebensader(n) | lifeline(s) | жизненная артерия |
| MKB | KMU | SME | МСП |
| DGA | GGF | owner-director | директор-собственник |
| Treg-cel | Treg-Zelle | Treg cell | T-reg клетка |
| voedingslijn | Versorgungslinie | feeding line | линия снабжения |
| de leiding | die Führung | the leadership | руководство |
| boer/boeren | Bauer/Bauern | farmer/farmers | фермер/фермеры |
| stallen-emigratie | Stall-Emigration | stable-emigration | эмиграция животноводства |
| Den Haag | Den Haag | The Hague | Гаага |
| Brussel | Brüssel | Brussels | Брюссель |
| gevolgenkaart | Folgenkarte | consequence map | карта последствий |
| plundering | Plünderung | plunder | разграбление |

## Diagnose-kader (verplicht aanwezig in elk artikel)

Elk vertaald artikel **moet** een diagnose-kader hebben — boven (na de auteurregel) en onder (vóór de alarm-strook of vóór het "verder lezen"-blok). Gebruik EXACT deze formuleringen:

### DE
- **Top**: "Dieser Text ist als <strong>Diagnose</strong> eines kranken Verwaltungs- und Wirtschaftssystems geschrieben. Er ist kein persönlicher Angriff, sondern ein Versuch, den tatsächlichen Zustand so klar wie möglich zu beschreiben, damit eine gezielte Behandlung möglich wird."
- **Bottom**: "Alles, was oben beschrieben wurde, ist als <strong>Diagnose</strong> gemeint, nicht als Angriff. Nur wenn wir das Krankheitsbild klar ins Auge fassen, können wir verhindern, dass es weiter wuchert, und an der Genesung arbeiten."

### EN
- **Top**: "This piece is written as a <strong>diagnosis</strong> of a sick administrative and economic system. It is not a personal attack, but an attempt to describe the actual condition as clearly as possible so that targeted treatment becomes possible."
- **Bottom**: "Everything described above is meant as a <strong>diagnosis</strong>, not as an attack. Only by looking the disease squarely in the eye can we prevent it from spreading further and begin working towards recovery."

### RU
- **Top**: "Этот текст написан как <strong>диагноз</strong> больной административной и экономической системы. Это не личное нападение, а попытка как можно яснее описать фактическое положение дел, чтобы стало возможным целенаправленное лечение."
- **Bottom**: "Всё, что описано выше, задумано как <strong>диагноз</strong>, а не как нападение. Только глядя клинической картине прямо в лицо, мы можем не дать ей расползтись дальше и начать работать на выздоровление."

Het kader-blok HTML-template (vervang `LANG_TOP_BODY` en `LANG_BOTTOM_BODY`):

```html
<!-- diagnose-kader v3 -->
<aside class="diagnose-kader diagnose-kader--top" style="max-width:920px;margin:1.5rem auto 2rem auto;padding:1.4rem 1.75rem;background:#f4ece0;border:1px solid #c9b896;border-left:5px solid #1c5760;font-family:Georgia,serif;color:#1a1a1a;line-height:1.6;">
  <p style="margin:0;font-size:1rem;">LANG_TOP_BODY</p>
</aside>
```

```html
<!-- diagnose-kader v3 -->
<aside class="diagnose-kader diagnose-kader--bottom" style="max-width:920px;margin:2.5rem auto 1.5rem auto;padding:1.4rem 1.75rem;background:#f4ece0;border:1px solid #c9b896;border-left:5px solid #1c5760;font-family:Georgia,serif;color:#1a1a1a;line-height:1.6;">
  <p style="margin:0;font-size:1rem;">LANG_BOTTOM_BODY</p>
</aside>
```

## Interne links omleiden

**Belangrijk**: Alle `href="..."` naar andere NL-artikelen moeten worden omgezet naar het taalspecifieke pad. Voorbeeld voor DE:

- `href="de-actor-is-de-regel.html"` → `href="der-akteur-ist-die-regel.html"`
- `href="../editie-1/index.html"` → `href="../ausgabe-1/index.html"`
- `href="../editie-0/index.html"` → `href="../ausgabe-0/index.html"`

Mapnamen per taal:
| NL | DE | EN | RU |
|---|---|---|---|
| editie-0..6 | ausgabe-0..6 | edition-0..6 | vypusk-0..6 |
| wat-opkomt | was-aufkommt | what-surfaces | chto-vsplyvaet |
| dossiers | dossiers | dossiers | dossiers |
| onderzoek | forschung | research | issledovanie |

Voor links naar artikelen die NOG NIET vertaald zijn in de doeltaal: laat ze wijzen naar het NL-bestand met `href="../../nl/wat-opkomt/SLUG.html"`.

## Lang-attribuut

`<html lang="...">` zetten naar `de`, `en` of `ru`.

## Werkwijze

1. Lees `/tmp/gh-repo/scripts/slugmap.json` voor doelbestandsnamen
2. Voor elk van de 11 bron-bestanden:
   - Lees NL-bron
   - Vertaal alle inhoud, behoud alle HTML-structuur (klassen, asides, divs)
   - Plaats het diagnose-kader boven (na `<p class="wo-artikel__auteur">`) en onder (vóór `alarm-strook` of vóór het verder-lezen-blok). Lees de bron eerst — het kan zijn dat een NL-artikel al een diagnose-kader heeft; vertaal die dan gewoon mee.
   - Schrijf naar het juiste pad in de doelmap
3. Geef aan het eind een lijst van geschreven bestanden terug

## Belangrijke aandachtspunten

- **Behoud alle inline `style="..."` attributen woordelijk** (kleuren, padding, max-width). Niet aanpassen.
- **Behoud SVG-blokken woordelijk** (geen vertaling van interne SVG-coderingen)
- **`<title>` en `<meta description>` ook vertalen**
- **Geen losse data verzinnen** — als een specifieke datum/cijfer onduidelijk is, behoud het NL-getal letterlijk

## Bronlijst

11 bestanden in `/tmp/gh-repo/nl/wat-opkomt/`:

1. de-actor-is-de-regel.html
2. de-auto-immuunziekte-slaat-toe.html
3. de-grote-plundering.html
4. de-singaporese-gevolgenkaart.html
5. de-zwitserse-gevolgenkaart.html
6. plundering-0-eerst-plukken-dan-oordelen.html
7. plundering-1-diagnose.html
8. plundering-2-mechaniek.html
9. plundering-3-afloop.html
10. plundering-4-politieke-landschap.html
11. zij-doden-hun-levensader.html
