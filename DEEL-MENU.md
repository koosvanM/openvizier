# Deel-menu — hoe het werkt

Elke pagina op openvizier.org toont in de hoofdnavigatie een **Delen**-item met vier acties:

| Actie | Wie mag dit | Werkt hoe |
|---|---|---|
| 🔒 **PDF downloaden** | Alleen met een geldige toegangscode | Vraagt om code → checkt hash-lijst in de repo → rendert gestileerde PDF |
| **Op Facebook delen** | Iedereen | Opent Facebook-sharer met de canonical URL |
| **Link kopiëren** | Iedereen | Kopieert URL naar het klembord |
| **Per e-mail versturen** | Iedereen | Opent standaard mailapp met titel + link ingevuld |

## Werking op hoofdlijnen

De site is puur statisch: geen server, geen database, geen API-key.
Toegangscodes worden als **SHA-256 hashes** opgeslagen in `assets/deel-codes.json`.
Alleen jij (met de master-key) kunt via `/admin/deel-beheer.html` nieuwe codes genereren.
Klanten die je een code geeft kunnen ermee inloggen voor de periode die jij hebt ingesteld (standaard 7 dagen).

## Codes beheren

1. Open **`https://openvizier.org/admin/deel-beheer.html`**
2. Log in met de master-key (bewaar deze veilig — hij staat niet in de repo, alleen de hash)
3. **Genereer een nieuwe code:**
   - Kies aantal geldigheidsdagen (1–90, standaard 7)
   - Vul optioneel een label in (bv. "Klant A · juli-editie") — helpt je het overzicht bij te houden
   - Klik "Genereer code"
4. De pagina toont:
   - De code zelf in groot formaat (bv. `7XK2-M9PQ`)
   - Klaar-om-te-versturen berichten in **Nederlands, Engels en Duits** — één klik om te kopiëren
5. Stuur de code + het bericht via WhatsApp, e-mail of geef 'm telefonisch door
6. **Belangrijk:** klik "Bestand downloaden" (of "JSON kopiëren"), vervang `assets/deel-codes.json` in je repo, commit en push. Netlify deployt vanzelf en de code werkt binnen ~1 minuut.

De admin-pagina toont ook een tabel met **alle bestaande codes** (actief en verlopen). Je kunt individuele codes verwijderen of alle verlopen codes in één klik opruimen.

## Wat de klant doet

1. Opent een artikel op openvizier.org
2. Klikt in het menu op **Delen → 🔒 PDF downloaden**
3. Popup vraagt om de toegangscode
4. Correct → PDF wordt gedownload; browser onthoudt de code tot de vervaldatum
5. Fout of verlopen → "Onjuiste of verlopen code" — probeer opnieuw of neem contact op

De klant hoeft geen account, geen e-mailadres en geen abonnement — alleen de code die jij hebt uitgegeven.

## Bestandsstructuur

| Bestand | Verantwoordelijkheid |
|---|---|
| `admin/deel-beheer.html` | Admin-interface: login, generator, code-overzicht |
| `assets/deel-codes.json` | Lijst van SHA-256 hashes + vervaldatums + master-key hash |
| `assets/deel-menu.js` | Client-side logica: code-popup, PDF-generatie, klembord |
| `assets/deel-menu.css` | Styling voor dropdown, popup, toast, PDF-layout |
| `nl/_data/menu-config.yaml` | Vertalingen + `is_deel_menu: true` op het `delen`-item |
| `scripts/menu_bouwen.py` | Rendert de dropdown op alle 802 pagina's |

## Menu bijwerken

Wijzigingen aan het menu of de deelvertalingen gaan via de canonieke workflow:

```bash
# 1. Bewerk nl/_data/menu-config.yaml
# 2. Regenereer alle 802 pagina's:
python3 scripts/menu_bouwen.py

# 3. Commit + push
git add -A && git commit -m "chore: menu bijwerken" && git push
```

## Beveiliging — belangrijke opmerkingen

- **Codes zijn SHA-256 gehasht** in de repo. De originele codes staan er niet in.
- **De master-key staat ook alleen als hash** in `assets/deel-codes.json`. Verlies je 'm, dan kan een nieuwe worden gegenereerd (maar bestaande sessies verlopen dan bij hun natuurlijke einddatum).
- **Client-side gate — realistische bescherming:** dit systeem stopt casual bezoekers en gedeelde downloadlinks. Een technisch onderlegd persoon met tijd zou de repo kunnen inspecteren en met genoeg rekencapaciteit een code kunnen brute-forcen (het alfabet is 32 tekens × 8 posities = ~10¹² combinaties). Voor een opiniekrant tegen scrapers en gratis-verspreiders is dat prima; voor echt gevoelig materiaal zou je een echte backend willen.
- **Codes zijn hoofdletterongevoelig** bij invoer — het systeem normaliseert automatisch.

## Kosten

Volledig gratis: geen serverkosten, geen API-quota. Alles draait in de browser van de bezoeker.
