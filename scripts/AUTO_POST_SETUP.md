# Auto-post setup — Mastodon

This workflow automatically posts new NL articles to Mastodon whenever you push
to `main`. It runs in GitHub Actions, waits ~2 minutes for Netlify to deploy,
then posts a toot with the article's title, lead and URL.

## What gets posted

- **What**: any new `.html` file under `nl/wat-opkomt/` or `nl/editie-*/`
  (except `index.html`, `delen.html`, `over.html`)
- **Where**: your Mastodon instance, as a public toot
- **When**: ~2 minutes after a push to `main` that adds new article files
- **How often**: max 3 posts per workflow run (bootstrap protection)

The state file `.posted.json` tracks which articles have been posted and is
committed back to the repo after each successful run, so each article posts
exactly once.

## One-time setup

### 1. Create a Mastodon application

1. Log into your Mastodon instance in a browser
2. Go to **Preferences → Development → New application**
3. Name: `Het Open Vizier auto-post`
4. Scopes: tick **`write:statuses`** (uncheck everything else)
5. Click **Submit**
6. Open the new application and copy the **access token** (the long string,
   not the client key/secret)

### 2. Add GitHub Secrets

On GitHub: `Settings → Secrets and variables → Actions → New repository secret`

Add two secrets:

| Name                 | Value                                          |
|----------------------|------------------------------------------------|
| `MASTODON_INSTANCE`  | Your instance hostname, e.g. `mastodon.social` (no `https://`, no trailing slash) |
| `MASTODON_TOKEN`     | The access token copied in step 1              |

Optional variable (`Settings → Secrets and variables → Actions → Variables`):

| Name             | Value (default if absent)        |
|------------------|----------------------------------|
| `SITE_BASE_URL`  | `https://openvizier.org`          |

### 3. Bootstrap state (already done)

The file `.posted.json` already contains all 85 existing NL articles marked as
"already posted". This ensures the first workflow run will NOT spam your
Mastodon timeline with 85 historical toots.

If you ever need to regenerate this file (e.g. after restructuring the site):

```bash
cd /path/to/repo
python3 scripts/bootstrap_state.py
git add .posted.json
git commit -m "Bootstrap auto-post state"
git push
```

### 4. Enable the workflow

The workflow file is at `.github/workflows/auto-post.yml`. It activates as soon
as it's on the `main` branch. Verify it works with a dry run:

1. Go to **Actions → Auto-post new articles to Mastodon**
2. Click **Run workflow**
3. Set `dry_run` to `true`
4. Click **Run workflow**

The run will detect new articles (if any) and print what *would* be posted,
without actually posting.

## How it works

1. **Trigger**: push to `main` that touches `nl/wat-opkomt/**.html` or
   `nl/editie-*/**.html`
2. **Checkout**: with depth 2 so the script can see what changed
3. **Wait 120s**: gives Netlify time to deploy so the URLs resolve
4. **Run `scripts/auto_post.py`**:
   - Scans NL article directories for new HTML files
   - For each file not in `.posted.json`:
     - Parses `<title>`, `og:description`, `og:image`
     - Composes a toot: title + lead + URL (max 500 chars)
     - POSTs to `https://{MASTODON_INSTANCE}/api/v1/statuses`
     - Records the toot URL in `.posted.json`
5. **Commit back**: pushes the updated `.posted.json` to `main`
   (using `[skip ci]` to avoid recursion)

## Manual posting (skip the workflow)

You can also run the script locally:

```bash
export MASTODON_INSTANCE="mastodon.social"
export MASTODON_TOKEN="your-token"
export DRY_RUN="1"  # remove to actually post
python3 scripts/auto_post.py
```

## Adding LinkedIn later

LinkedIn requires either:
- A LinkedIn Developer app + OAuth flow (token refresh every 60 days), or
- A third-party scheduler (Buffer, Hootsuite, Zapier) with a webhook

When you're ready, the `auto_post.py` script has a clear shape: add a
`post_to_linkedin(status)` function alongside `post_to_mastodon(status)`,
and a `LINKEDIN_TOKEN` secret. Drop me a note when you want this.

## Adding more languages later

The script currently only scans `nl/` directories. To add DE/EN/RU:

1. Edit `scripts/auto_post.py`, expand the `NL_DIRS` list
2. Optionally compose toots per language (use the article's `<html lang="...">`
   to set the Mastodon `language` parameter)

Note: posting the same article in 4 languages = 4 toots. Fine on Mastodon,
considered spam on LinkedIn — so handle differently per platform.

## Troubleshooting

- **No new articles detected**: check that the new file is under a tracked
  directory and not in the `IGNORE_FILES` set
- **Mastodon HTTP 401**: token wrong or revoked; regenerate in
  `Preferences → Development`
- **Mastodon HTTP 422 "Validation failed"**: usually toot too long (the script
  truncates at 500 chars, but `<meta description>` could contain odd
  characters — check the failing toot in the workflow log)
- **Workflow runs but commits revert**: check the `concurrency` setting; never
  cancel an in-progress run or you'll lose state mid-update

## Security

- The Mastodon token has only `write:statuses` scope — it cannot read your
  DMs, change settings, or follow accounts
- Secrets are encrypted at rest in GitHub and only exposed to the workflow's
  environment, not to logs
- The token does NOT appear in `.posted.json` or any committed file
