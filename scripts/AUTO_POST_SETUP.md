# Auto-post setup — Mastodon + LinkedIn

GitHub Actions workflow die nieuwe artikelen van Het Open Vizier automatisch
deelt op Mastodon en LinkedIn. Triggert bij elke push naar `main`, wacht 2
minuten op Netlify-deploy, en post dan.

## Wat wordt waar gepost

| Platform | Talen           | Per artikel | API                |
|----------|-----------------|-------------|--------------------|
| Mastodon | NL, DE, EN, RU  | 4 toots (1 per taal) | Native v1/statuses |
| LinkedIn | NL, EN          | 2 posts     | Native UGC of Buffer |

**Waarom dit verschil?** Mastodon's federatie hanteert taal-tags goed; LinkedIn
bestraft dezelfde inhoud meermaals posten. NL + EN dekt je hoofdpubliek zonder
spam-signaal.

## Wat in één run wordt gepost

- **Max 6 posts per run** (bootstrap-bescherming, instelbaar via
  GitHub Variable `MAX_POSTS_PER_RUN`)
- Eén nieuw artikel in NL+DE+EN+RU = 4 Mastodon + 2 LinkedIn = 6 posts → past
- Vier nieuwe artikelen tegelijk = de eerste tot de cap, rest volgende run

## State-tracking

`.posted.json` aan repo-root. Sleutels: `platform|lang|url`. Wordt na elke run
terug-gepusht naar `main` met `[skip ci]` zodat de workflow niet recurseert.

---

## Setup stap voor stap

### Eenmalig: Mastodon

1. Log in op je Mastodon instance in browser
2. **Preferences → Development → New application**
3. Naam: `Het Open Vizier auto-post`
4. Scopes: vink **`write:statuses`** aan, rest uit
5. Submit → open de nieuwe app → kopieer **Your access token**

Op GitHub: `Settings → Secrets and variables → Actions → New secret`:

| Naam                 | Waarde                                            |
|----------------------|---------------------------------------------------|
| `MASTODON_INSTANCE`  | `mastodon.social` (jouw instance, geen `https://`)|
| `MASTODON_TOKEN`     | access token uit stap 5                           |

### Eenmalig: LinkedIn — kies één van twee paden

#### Pad A: Native LinkedIn API (gratis, technischer)

LinkedIn vereist een eigen app met OAuth. Token verloopt na **60 dagen** en
moet handmatig vernieuwd worden.

1. Ga naar https://www.linkedin.com/developers/apps
2. **Create app**: naam `Het Open Vizier auto-post`, kies een
   "verified" company page als app-owner (of je persoonlijke pagina)
3. Tab **Products** → vraag **"Share on LinkedIn"** product aan
   (instant goedkeuring voor persoonlijke posts)
4. Optioneel: voor company-pagina-posts ook **"Marketing Developer Platform"**
   aanvragen (handmatige LinkedIn-review, kan weken duren)
5. Tab **Auth** → kopieer Client ID en Client Secret
6. Genereer access token via OAuth2 (eenmalig):
   ```
   # Open in browser:
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https%3A%2F%2Flocalhost&scope=w_member_social
   
   # Na inloggen redirect naar https://localhost?code=AUTH_CODE
   # Wissel auth code in voor token (cURL):
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -d "grant_type=authorization_code" \
     -d "code=AUTH_CODE" \
     -d "redirect_uri=https://localhost" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET"
   # Response bevat "access_token"
   ```
7. Vind je author URN:
   ```
   curl https://api.linkedin.com/v2/userinfo \
     -H "Authorization: Bearer YOUR_TOKEN"
   # "sub" veld bevat je member ID → URN = "urn:li:person:MEMBER_ID"
   ```

GitHub Secrets:

| Naam                  | Waarde                                |
|-----------------------|---------------------------------------|
| `LINKEDIN_TOKEN`      | access token uit stap 6               |
| `LINKEDIN_AUTHOR_URN` | `urn:li:person:abc123` of `urn:li:organization:456` |

**Belangrijk**: zet een herinnering op dag 55 om het token te vernieuwen.

#### Pad B: Buffer / Zapier webhook (eenvoudiger, vereist abonnement)

1. **Buffer**: `buffer.com` → nieuwe channel = LinkedIn-profiel
2. Maak een Zapier zap (gratis tier werkt voor lage volumes):
   - **Trigger**: Webhook (Catch Hook) → krijg URL
   - **Action**: Buffer → Add to Queue (LinkedIn channel)
   - Field-mapping: `text` → post body, `url` → link
3. Test de zap met sample data

GitHub Secret:

| Naam                | Waarde                                  |
|---------------------|------------------------------------------|
| `BUFFER_WEBHOOK_URL`| Zapier webhook URL                       |

Het script probeert eerst native LinkedIn als die secrets ingesteld zijn,
anders valt het terug op Buffer. Stel maar één pad in, niet beide.

### Bootstrap state (al gedaan)

Het bestand `.posted.json` is al voorgevuld met alle 342 huidige artikelen
(in 4 talen) op zowel Mastodon als LinkedIn (NL+EN). De eerste workflow-run
zal dus géén historische artikelen spammen.

Hergenerate (alleen nodig na grote site-reorganisatie):
```bash
python3 scripts/bootstrap_state.py
git add .posted.json
git commit -m "Bootstrap auto-post state"
git push
```

### Test met dry-run

Op GitHub: **Actions → Auto-post new articles → Run workflow**
→ kies `dry_run: true` → **Run workflow**.

In de run-log zie je wat *zou* worden gepost zonder dat het echt gebeurt.

---

## Hoe het script werkt

1. **Scan** alle taal-directories voor `.html` files
2. Voor elk artikel: voor Mastodon (alle talen) én LinkedIn (alleen NL+EN):
3. **Check** `.posted.json` op key `platform|lang|url`
4. **Skip** als al gepost
5. **Extract** title + lead via HTML parser
6. **Compose** toot/post:
   - Mastodon: `{title}\n\n{lead}\n\n{url}` binnen 500 char
   - LinkedIn: zelfde format binnen 3000 char + media-card naar URL
7. **POST** naar API (of webhook)
8. **Record** in state-bestand
9. **Pause** 2s tussen posts
10. **Commit** state terug naar repo

## Lokaal testen

```bash
# Mastodon only
export MASTODON_INSTANCE="mastodon.social"
export MASTODON_TOKEN="..."
export DRY_RUN=1
python3 scripts/auto_post.py

# LinkedIn native
export LINKEDIN_TOKEN="..."
export LINKEDIN_AUTHOR_URN="urn:li:person:..."
export DRY_RUN=1
python3 scripts/auto_post.py

# LinkedIn via Buffer
export BUFFER_WEBHOOK_URL="https://hooks.zapier.com/..."
export DRY_RUN=1
python3 scripts/auto_post.py
```

## Troubleshooting

**Mastodon HTTP 401**
Token vervallen of ingetrokken → regenerate in Mastodon Preferences.

**LinkedIn HTTP 401**
Token verlopen (60 dagen). Regenerate via OAuth flow.

**LinkedIn HTTP 403 "Insufficient scope"**
Je app heeft geen `w_member_social` scope. Vraag aan in
Developer Portal → Products → "Share on LinkedIn".

**Workflow runt, geen posts ondanks nieuwe artikel**
- Pad onder bekende directory? (zie YAML `paths:` lijst)
- `<title>` aanwezig in HTML?
- Niet in `IGNORE_FILES` (`index.html`, `delen.html`, etc.)?

**State revert / dubbele posts**
Workflow nooit halverwege cancelen — `concurrency` is daarom op
`cancel-in-progress: false` gezet.

## LinkedIn-token vernieuwen na 60 dagen

```bash
# Stap 1: OAuth-link opnieuw openen, AUTH_CODE krijgen
# Stap 2: Wissel voor nieuw token
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d "grant_type=authorization_code" \
  -d "code=NIEUW_AUTH_CODE" \
  -d "redirect_uri=https://localhost" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
# Stap 3: Update GitHub Secret LINKEDIN_TOKEN
```

Eventueel: voeg een herinnering toe via `schedule_cron` in Perplexity Computer
om dit elke 55 dagen aan jezelf te sturen.

## Beveiliging

- Mastodon scope: alleen `write:statuses` — kan geen DMs lezen of accounts volgen
- LinkedIn scope: alleen `w_member_social` — kan alleen op jouw naam posten
- Secrets versleuteld in GitHub, niet zichtbaar in logs
- Geen tokens in `.posted.json` of andere committed bestanden
