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

## Stap 7 — Lanceren

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
