# Vertaal de proloog "Een staat met een auto-immuunziekte"

## Bron en doel

- **Bron**: `/tmp/gh-repo/nl/wat-opkomt/de-metafoor-auto-immuunziekte.html`
- **Doel DE**: `/tmp/gh-repo/de/was-aufkommt/die-metapher-autoimmunkrankheit.html`
- **Doel EN**: `/tmp/gh-repo/en/what-surfaces/the-metaphor-autoimmune-disease.html`
- **Doel RU**: `/tmp/gh-repo/ru/chto-vsplyvaet/metafora-autoimmunnoy-bolezni.html`

## Toon en stijl

**ZACHT, BESCHOUWEND, REËEL.** Niet de harde diagnose-stijl van de Brussel-artikelen.
- Lange flowende zinnen mogen
- Minder vet, geen schreeuw-stijl
- Toon: bezonnen, uitleggend, uitnodigend tot meedenken
- Geen vet op cijfers, want er staan geen cijfers in
- Wel `<em>` (italic) op zachte sleuteltermen zoals "auto-immuunziekte" zelf in de eerste alinea

## Werkwijze

1. Lees `/tmp/gh-repo/nl/wat-opkomt/de-metafoor-auto-immuunziekte.html` volledig
2. Vertaal alle Nederlandse tekst — behoud ALLE HTML/CSS-structuur woordelijk
3. Aanpassingen:
   - `<html lang="...">` naar je doeltaal
   - `<title>` en `<meta name="description">` vertalen
   - Kop-banner "Gratis maandelijkse krant zonder reclame — Schrijf u in zonder verplichting" vertalen
   - Masthead kicker "Wat opkomt · 20 juni 2026" vertalen
   - Kruimels: "Voorpagina › Wat opkomt › De metafoor — auto-immuunziekte" vertalen
   - Article label "Brussel-campagne · proloog" vertalen
   - Auteursregel "Jacobus van Merksteijn · Malta, juni 2026" — behoud de naam, vertaal "Malta, juni 2026" naar je doeltaal datumconventie
4. Vervang interne links:
   - `href="../"` blijft zo (verwijst naar taal-root, dat klopt al)
   - `href="./"` blijft zo
   - `href="../delen.html"` → DE: `../teilen.html`, EN: `../share.html`, RU: `../podelitsya.html`
   - `href="de-anti-immuunziekte-van-brussel.html"` → DE: `die-anti-immunkrankheit-bruessels.html`, EN: `the-anti-immune-disease-of-brussels.html`, RU: `anti-immunnaya-bolezn-bryusselya.html`
   - `href="zij-doden-hun-levensaders-brussel.html"` → DE: `sie-toeten-ihre-lebensadern-bruessel.html`, EN: `they-kill-their-lifelines-brussels.html`, RU: `oni-ubivayut-svoi-zhiznennye-arterii-bryussel.html`
   - `href="de-auto-immuunziekte-slaat-toe.html"` → DE: `die-autoimmunkrankheit-schlaegt-zu.html`, EN: `the-autoimmune-disease-strikes.html`, RU: `autoimmunnaya-bolezn-nanosit-udar.html`
   - `href="zij-doden-hun-levensader.html"` → DE: `sie-toeten-ihre-lebensader.html`, EN: `they-kill-their-lifeline.html`, RU: `oni-ubivayut-svoyu-zhiznennuyu-arteriyu.html`
5. Diagnose-kader-tekst gebruiken (vaste formuleringen):

### DE
- TOP: "Dieser Text ist als <strong>Diagnose</strong> eines kranken Verwaltungs- und Wirtschaftssystems geschrieben. Er ist kein persönlicher Angriff, sondern ein Versuch, den tatsächlichen Zustand so klar wie möglich zu beschreiben, damit eine gezielte Behandlung möglich wird."
- BOTTOM: "Alles, was oben beschrieben wurde, ist als <strong>Diagnose</strong> gemeint, nicht als Angriff. Nur wenn wir das Krankheitsbild klar ins Auge fassen, können wir verhindern, dass es weiter wuchert, und an der Genesung arbeiten."

### EN
- TOP: "This piece is written as a <strong>diagnosis</strong> of a sick administrative and economic system. It is not a personal attack, but an attempt to describe the actual condition as clearly as possible so that targeted treatment becomes possible."
- BOTTOM: "Everything described above is meant as a <strong>diagnosis</strong>, not as an attack. Only by looking the disease squarely in the eye can we prevent it from spreading further and begin working towards recovery."

### RU
- TOP: "Этот текст написан как <strong>диагноз</strong> больной административной и экономической системы. Это не личное нападение, а попытка как можно яснее описать фактическое положение дел, чтобы стало возможным целенаправленное лечение."
- BOTTOM: "Всё, что описано выше, задумано как <strong>диагноз</strong>, а не как нападение. Только глядя клинической картине прямо в лицо, мы можем не дать ей расползтись дальше и начать работать на выздоровление."

## Glossarium voor de proloog

| NL | DE | EN | RU |
|---|---|---|---|
| auto-immuunziekte | Autoimmunkrankheit | autoimmune disease | аутоиммунная болезнь |
| anti-immuunziekte | Anti-Immunkrankheit | anti-immune disease | анти-иммунная болезнь |
| T-cellen | T-Zellen | T cells | T-клетки |
| regulerende T-cellen | regulierende T-Zellen | regulatory T cells | регуляторные T-клетки |
| de leiding | die Führung | the leadership | руководство |
| boer | Bauer | farmer | фермер |
| MKB / familiebedrijf | KMU / Familienunternehmen | SME / family business | МСП / семейный бизнес |
| commandostructuur | Befehlskette / Führungsstruktur | command structure | командная структура |
| corrigerende tegenmacht | korrigierende Gegenmacht | corrective counter-power | корректирующая контр-власть |
| persoonlijke aansprakelijkheid | persönliche Haftung | personal liability | личная ответственность |
| Brussel | Brüssel | Brussels | Брюссель |
| Den Haag | Den Haag | The Hague | Гаага |
| CBAM, ETS, Pillar Two | CBAM, ETS, Pillar Two | CBAM, ETS, Pillar Two | CBAM, ETS, Pillar Two (behoud) |

## Verboden

- ❌ Geen rode/alarm-blokken introduceren
- ❌ Geen hardere stijl-elementen toevoegen die niet in NL stonden
- ❌ Geen extra cijfers of feiten introduceren
- ❌ Geen wijzigingen aan kleuren/CSS

## Bij oplevering

Bevestig dat je het bestand hebt geschreven met `write` naar het juiste pad.
Geen git-commit.
