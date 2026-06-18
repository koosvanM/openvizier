# Het Open Vizier — Installatiehandleiding

Stap-voor-stap instructies om de krant online te brengen.
Totaal benodigde tijd: ongeveer **90 minuten verspreid over één avond**.
Totale kosten eerste jaar: ongeveer **$ 30** (domein + e-mail + nieuwsbrief).

---

## Wat je krijgt

- **Website** op `https://openvizier.org` in drie talen (NL/DE/EN)
- **E-mail** op `@openvizier.org` (5 mailboxen via Namecheap)
- **Reactiesysteem** onder elk artikel, met AI-moderatie (gratis via Giscus + GitHub)
- **Nieuwsbrief** met double opt-in (gratis tot 100 lezers via Buttondown)

---

## Stap 1 — Domein registreren (10 min, ~$13/jaar)

1. Ga naar [namecheap.com](https://www.namecheap.com).
2. Maak een account aan als je die nog niet hebt.
3. Zoek op **openvizier.org** en voeg toe aan winkelwagen.
4. **WhoisGuard / Domain Privacy:** AAN (gratis).
5. **Auto-renew:** AAN.
6. Reken af. Eerste jaar ongeveer $7,50, renewal $13/jaar.

---

## Stap 2 — Namecheap Private Email (10 min, ~$10/jaar)

1. In je Namecheap-dashboard ga je naar **Domain List → openvizier.org → Manage**.
2. Klik op het tabblad **Email**.
3. Kies **Private Email** → het *Starter*-pakket (5 mailboxen, ~$9,88/jaar promo, daarna ~$15/jaar).
4. Tijdens het bestelproces kun je direct de DNS-records laten configureren — kies **"Yes, configure automatically"**.
5. Maak de volgende mailboxen aan (Dashboard → Private Email → Manage):
   - `redactie@openvizier.org` — algemeen redactioneel
   - `jacobus@openvizier.org` — jouw persoonlijke adres
   - `moderatie@openvizier.org` — moderatie-notificaties
   - `nieuwsbrief@openvizier.org` — afzender van de nieuwsbrief
   - `info@openvizier.org` — reserve / contactformulier
6. Voor elke mailbox: stel een sterk wachtwoord in en zet **forwarding** naar je eigen Apple-relay-adres of een ander bestaand adres dat je al gebruikt. Zo komen alle e-mails meteen op één plek binnen.
7. **Mobiele app:** Namecheap Private Email werkt met elke IMAP/SMTP-client. Instructies vind je in het dashboard onder **Settings → Mail Client Setup**.

---

## Stap 3 — GitHub-repo + Netlify (20 min, gratis)

### 3a. GitHub-account

1. Ga naar [github.com](https://github.com) en maak een account, of log in.
2. Maak een nieuwe **public** repository genaamd `openvizier`.
3. Maak een **tweede** public repo genaamd `openvizier-discussies` — deze is voor het discussiesysteem (zie stap 4).

### 3b. Upload de site

1. Op je computer: pak de zip `openvizier.zip` uit.
2. In de map, open een terminal en typ:
   ```
   git init
   git add .
   git commit -m "Eerste editie Het Open Vizier"
   git branch -M main
   git remote add origin https://github.com/JOUW_GEBRUIKERSNAAM/openvizier.git
   git push -u origin main
   ```
   (Vervang `JOUW_GEBRUIKERSNAAM` door je echte GitHub-gebruikersnaam.)

### 3c. Netlify koppelen

1. Ga naar [netlify.com](https://www.netlify.com) en log in (je hebt al een account).
2. Klik **Add new site → Import from Git → GitHub**.
3. Geef Netlify toegang tot je `openvizier`-repo.
4. **Build settings:**
   - Build command: *(leeg laten)*
   - Publish directory: `.` (de hoofdmap)
5. Klik **Deploy**.
6. Na ongeveer 30 seconden is je site live op een tijdelijke `*.netlify.app`-URL — test hem.

### 3d. Eigen domein koppelen aan Netlify

1. In Netlify ga je naar **Site settings → Domain management → Add custom domain**.
2. Typ `openvizier.org` en klik **Verify**.
3. Netlify geeft je twee DNS-records (of vraagt je name servers te wijzigen).
4. **Eenvoudigste route — DNS-records aanpassen in Namecheap:**
   - Ga naar Namecheap → openvizier.org → Manage → **Advanced DNS**.
   - Verwijder bestaande A-records voor `@` en `www`.
   - Voeg toe:
     - **A-record** met host `@` en value `75.2.60.5` (Netlify's load balancer)
     - **CNAME** met host `www` en value `[je-site-naam].netlify.app`
   - Sla op. DNS propagatie duurt 15 min - 24 uur, meestal binnen het uur.
5. In Netlify: klik **Verify DNS configuration** zodra het werkt.
6. Activeer **HTTPS** (Netlify regelt het SSL-certificaat automatisch via Let's Encrypt).

---

## Stap 4 — Reactiesysteem (Giscus) inrichten (15 min, gratis)

Giscus gebruikt GitHub Discussions als backend. Gratis, geen tracking, AI-moderatie via GitHub Actions mogelijk.

1. Ga naar je `openvizier-discussies`-repo op GitHub.
2. **Settings → General → Features:** zet **Discussions** AAN.
3. **Settings → General → Default branch:** maak een nieuwe branch indien nodig.
4. Open de **Discussions**-tab en maak een nieuwe categorie genaamd **"Editie 1"** (Type: Announcement).
5. Ga naar [giscus.app](https://giscus.app/nl).
6. Vul in:
   - Repository: `JOUW_GEBRUIKERSNAAM/openvizier-discussies`
   - Pagina ↔ Discussions Mapping: **pathname**
   - Discussion Category: **Editie 1**
   - Reactie-positie: **Boven de reacties**
   - Thema: **Light**
7. Giscus genereert een `<script>`-blok. Kopieer de waarden van:
   - `data-repo`
   - `data-repo-id`
   - `data-category`
   - `data-category-id`
8. Open elk artikel in `nl/editie-1/*.html` en vervang de placeholders:
   - `GEBRUIKER/openvizier-discussies` → jouw waarde
   - `GIT_REPO_ID_HIER` → jouw repo-id
   - `CATEGORY_ID_HIER` → jouw category-id
9. Commit en push naar GitHub — Netlify deployt automatisch.

**Tip:** je hoeft niet voor elk artikel apart te bewerken. Open `build_articles.py`, zoek de placeholders, vervang ze daar, en run `python3 build_articles.py` opnieuw.

### AI-moderatie aanzetten (optioneel, geavanceerd)

1. Maak in `openvizier-discussies` een nieuwe file aan: `.github/workflows/moderate.yml`.
2. Voeg een GitHub Action toe die elke nieuwe Discussion-comment doorstuurt naar de OpenAI/Claude API en bij een match (spam/belediging) automatisch verbergt.
3. Een werkend voorbeeld vind je bij [github.com/giscus/giscus/discussions](https://github.com/giscus/giscus/discussions).

Optie zonder code: laat alle reacties handmatig modereren via **Settings → Discussions → Require moderation**. Met 5-30 reacties per editie is dat goed te doen.

---

## Stap 5 — Nieuwsbrief (Buttondown) (15 min, gratis tot 100 lezers)

1. Maak een account op [buttondown.email](https://buttondown.email).
2. Verifieer je e-mailadres.
3. Stel afzender in op `nieuwsbrief@openvizier.org`.
4. Onder **Settings → Domains** voeg je openvizier.org toe; Buttondown geeft je een TXT-, MX- en DKIM-record om aan je DNS toe te voegen (Namecheap → Advanced DNS).
5. Buttondown geeft je een **embed-formulier**. Open `nl/index.html`, zoek het regel met `formspree.io/f/REPLACE_ME` en vervang het hele `<form>`-blok door de Buttondown-embed-code.
6. Test door je eigen e-mailadres in te schrijven; je moet een bevestigingsmail krijgen (double opt-in).

**Eerste nieuwsbrief versturen:** kopieer een korte tekst die naar de zes meest interessante artikelen linkt, plus de tagline en datum.

---

## Stap 6 — Vertalingen (lopend, optioneel voor lancering)

De DE- en EN-pagina's bevatten nu een "binnenkort"-melding. Voor echte vertalingen:

1. Open elk NL-artikel en vertaal het in DeepL (de gratis versie volstaat tot 500.000 tekens/maand).
2. Sla de Duitse versie op als `de/ausgabe-1/[slug].html` en de Engelse als `en/edition-1/[slug].html`.
3. Pas de top-navigatie van die bestanden aan zodat de juiste taal-link actief is.
4. **Tip voor consistentie:** vraag een AI-model om de vertaling te reviewen op idioom — "vertaal deze tekst van Nederlands naar formeel Duits, geschikt voor een redactionele krant".

---

## Stap 7 — LinkedIn-integratie voor de auto-post bot

De auto-post bot (`scripts/auto_post.py`) kan automatisch NL- en EN-berichten plaatsen op LinkedIn zodra je twee omgevingsvariabelen instelt: `LINKEDIN_TOKEN` en `LINKEDIN_AUTHOR_URN`. Berichten in andere talen worden overgeslagen om spam te vermijden.

### 7a. LinkedIn Developer App aanmaken

1. Ga naar [linkedin.com/developers](https://www.linkedin.com/developers/) en log in met je LinkedIn-account.
2. Klik op **Create app**.
3. Vul in:
   - **App name:** bijv. `Open Vizier Auto-post`
   - **LinkedIn Page:** selecteer je persoonlijke profiel of organisatiepagina
   - **App logo:** upload een afbeelding (vereist)
4. Accepteer de gebruiksvoorwaarden en klik **Create app**.
5. Ga naar het tabblad **Auth**. Noteer de **Client ID** en **Client Secret** — je hebt ze nodig voor de OAuth2-flow.
6. Voeg onder **OAuth 2.0 settings → Authorized redirect URLs** een tijdelijke callback-URL toe, bijv.:
   ```
   https://localhost:8080/callback
   ```

### 7b. Benodigde OAuth2-scopes aanvragen

Ga naar het tabblad **Products** in je app en vraag de volgende producten aan:

- **Share on LinkedIn** — geeft de scope `w_member_social` (vereist om posts te maken)
- **Sign In with LinkedIn using OpenID Connect** — geeft de scopes `openid` en `profile` (vereist om je URN op te halen)

Na goedkeuring (meestal direct of binnen 24 uur) zie je de scopes verschijnen onder **Auth → OAuth 2.0 scopes**.

> **Let op:** voor posten naar een *organisatiepagina* (in plaats van een persoonlijk profiel) heb je het product **Marketing Developer Platform** nodig — dat vereist een aparte aanvraag bij LinkedIn en heeft een langere doorlooptijd.

### 7c. Access token verkrijgen (OAuth2-flow)

LinkedIn gebruikt de **Authorization Code Flow**. Voer de stappen hieronder uit in een terminal.

**Stap 1 — Autorisatie-URL samenstellen**

Vervang `JOUW_CLIENT_ID` en open de volgende URL in je browser:

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=JOUW_CLIENT_ID&redirect_uri=https%3A%2F%2Flocalhost%3A8080%2Fcallback&scope=openid%20profile%20w_member_social
```

Log in en klik op **Allow**. Je browser wordt doorgestuurd naar iets als:
```
https://localhost:8080/callback?code=AQT...&state=
```
Kopieer de waarde van de `code`-parameter.

**Stap 2 — Code inwisselen voor een access token**

```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=JOUW_CODE_HIER" \
  -d "redirect_uri=https%3A%2F%2Flocalhost%3A8080%2Fcallback" \
  -d "client_id=JOUW_CLIENT_ID" \
  -d "client_secret=JOUW_CLIENT_SECRET"
```

Het antwoord ziet er zo uit:

```json
{
  "access_token": "AQV...",
  "expires_in": 5183999,
  "scope": "openid,profile,w_member_social"
}
```

Sla de waarde van `access_token` op — dit is je `LINKEDIN_TOKEN`. Het token is **60 dagen geldig**.

### 7d. Je `LINKEDIN_AUTHOR_URN` opzoeken

De `LINKEDIN_AUTHOR_URN` identificeert wie de post publiceert. Voor een persoonlijk profiel is dit `urn:li:person:XXXX`, voor een organisatie `urn:li:organization:XXXX`.

**Persoonlijk profiel** — haal de `sub`-waarde op via het OpenID Connect userinfo-endpoint:

```bash
curl -H "Authorization: Bearer JOUW_ACCESS_TOKEN" \
  https://api.linkedin.com/v2/userinfo
```

Voorbeeldantwoord:

```json
{
  "sub": "abc123XYZ",
  "name": "Jacobus De Vries",
  "email": "jacobus@openvizier.org"
}
```

Je `LINKEDIN_AUTHOR_URN` wordt dan:
```
urn:li:person:abc123XYZ
```

**Organisatiepagina** — de numerieke ID staat in de URL van je LinkedIn-pagina:
```
https://www.linkedin.com/company/12345/
                                 ^^^^^
```
Je `LINKEDIN_AUTHOR_URN` wordt dan:
```
urn:li:organization:12345
```

### 7e. GitHub Secrets instellen

1. Ga naar je GitHub-repo → **Settings → Secrets and variables → Actions**.
2. Klik op **New repository secret** en voeg de volgende twee secrets toe:

   | Naam | Waarde |
   |---|---|
   | `LINKEDIN_TOKEN` | Het access token uit stap 7c |
   | `LINKEDIN_AUTHOR_URN` | Bijv. `urn:li:person:abc123XYZ` |

3. Controleer dat de andere vereiste secrets ook aanwezig zijn:

   | Naam | Beschrijving |
   |---|---|
   | `MASTODON_INSTANCE` | URL van je Mastodon-instantie, bijv. `https://mastodon.social` |
   | `MASTODON_TOKEN` | Mastodon API access token |
   | `BUTTONDOWN_API_KEY` | Buttondown API-sleutel |

### 7f. Token verloopt na 60 dagen — handmatig vernieuwen

LinkedIn-tokens verlopen na 60 dagen. Er is geen automatische vernieuwing via refresh tokens in de standaard Member Authorization flow. Zet een herinnering in je agenda voor over ∼55 dagen.

Om te vernieuwen:
1. Herhaal stap 7c (autorisatie-URL openen → nieuwe code ophalen → inwisselen voor nieuw token).
2. Ga naar GitHub → **Settings → Secrets** en overschrijf `LINKEDIN_TOKEN` met het nieuwe token.

> **Tip:** LinkedIn geeft ook een `refresh_token` terug met een geldigheidsduur van 365 dagen als je app toegang heeft tot het **Marketing Developer Platform**-product. Vraag dit aan als je de vernieuwing wilt automatiseren.

## Stap 8 — Lanceren

1. **Aankondiging op LinkedIn:** post een korte introductie met link naar `https://openvizier.org/nl/editie-1/voorwoord.html`. Vraag mensen om zich in te schrijven voor de nieuwsbrief.
2. **Mail naar 20-50 mensen** die je vertrouwt — vrienden, oud-collega's, vakgenoten. Vraag eerlijke feedback en of ze willen reageren onder een artikel.
3. **Eerste discussievragen aanjagen:** plaats zelf een eerste reactie onder elk artikel — een aanvullende gedachte of vraag — om de drempel te verlagen.

---

## Onderhoud per editie (vanaf editie 2)

Per editie kost ongeveer **6-10 uur** verdeeld over twee weken:
- 3-4 uur schrijven
- 1 uur vertalen (DeepL + nalezen)
- 1 uur opmaak en publiceren
- 30-60 minuten moderatie en lezersreacties per week

Voor een nieuwe editie:
1. Kopieer `nl/editie-1/` naar `nl/editie-2/`, vervang inhoud.
2. Maak nieuwe Discussion-categorie in GitHub: "Editie 2".
3. Update `data-category` waarde in `build_articles.py` en run het script.
4. Update voorpagina en archief.
5. Push naar GitHub — Netlify deployt automatisch.
6. Verstuur nieuwsbrief.

---

## Hulp nodig?

Voor elke stap waarvan je vastloopt: stuur me een bericht. Ik kan stappen uitvoeren of meekijken.

Veel succes met editie één.
