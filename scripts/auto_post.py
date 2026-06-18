#!/usr/bin/env python3
"""
Auto-post new articles from Het Open Vizier to Mastodon and LinkedIn.

Detects new articles in NL/DE/EN/RU directories.
Extracts <title>, <meta description>, og:image per article.
Posts to:
  - Mastodon: all 4 languages, each as its own toot (lang param set correctly)
  - LinkedIn: NL + EN only (avoid spam; LinkedIn favours fewer posts)
    - Native API if LINKEDIN_TOKEN + LINKEDIN_AUTHOR_URN are set
    - Buffer webhook fallback if BUFFER_WEBHOOK_URL is set
    - Skipped silently if neither is configured

State: .posted.json — keyed by (platform, language, url) so each combo posts once.

Environment variables (all optional, but at least one platform must be configured):
  Common:
    SITE_BASE_URL              default https://openvizier.org
    DRY_RUN                    "1" to log only
    MAX_POSTS_PER_RUN          default 6 (bootstrap protection)

  Mastodon:
    MASTODON_INSTANCE          e.g. "mastodon.social" (no https://)
    MASTODON_TOKEN             access token, scope write:statuses

  LinkedIn (native):
    LINKEDIN_TOKEN             OAuth2 access token (60-day validity)
    LINKEDIN_AUTHOR_URN        URN of the posting entity, e.g.
                               "urn:li:person:abc123" or "urn:li:organization:456"

  LinkedIn (Buffer fallback):
    BUFFER_WEBHOOK_URL         Zapier/Buffer webhook URL
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib import request, error
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / ".posted.json"
SITE_BASE = os.environ.get("SITE_BASE_URL", "https://openvizier.org").rstrip("/")
DRY_RUN = os.environ.get("DRY_RUN", "").strip() in ("1", "true", "yes")
MAX_POSTS_PER_RUN = int(os.environ.get("MAX_POSTS_PER_RUN", "6"))

# Mastodon
MASTODON_INSTANCE = os.environ.get("MASTODON_INSTANCE", "").strip().rstrip("/")
MASTODON_TOKEN = os.environ.get("MASTODON_TOKEN", "").strip()

# LinkedIn native
LINKEDIN_TOKEN = os.environ.get("LINKEDIN_TOKEN", "").strip()
LINKEDIN_AUTHOR_URN = os.environ.get("LINKEDIN_AUTHOR_URN", "").strip()

# LinkedIn via Buffer/Zapier webhook
BUFFER_WEBHOOK_URL = os.environ.get("BUFFER_WEBHOOK_URL", "").strip()

# Language → article directories
LANG_DIRS = {
    "nl": ["nl/wat-opkomt", "nl/editie-0", "nl/editie-1", "nl/editie-2",
           "nl/editie-3", "nl/editie-4", "nl/editie-5", "nl/editie-6"],
    "de": ["de/was-aufkommt", "de/ausgabe-0", "de/ausgabe-1", "de/ausgabe-2",
           "de/ausgabe-3", "de/ausgabe-4", "de/ausgabe-5", "de/ausgabe-6"],
    "en": ["en/what-surfaces", "en/edition-0", "en/edition-1", "en/edition-2",
           "en/edition-3", "en/edition-4", "en/edition-5", "en/edition-6"],
    "ru": ["ru/chto-vsplyvaet", "ru/vypusk-0", "ru/vypusk-1", "ru/vypusk-2",
           "ru/vypusk-3", "ru/vypusk-4", "ru/vypusk-5", "ru/vypusk-6"],
}

# LinkedIn only posts these languages (avoid spam)
LINKEDIN_LANGS = ("nl", "en")

# Files to ignore
IGNORE_FILES = {
    "index.html", "delen.html", "over.html",
    "teilen.html", "ueber.html",
    "share.html", "about.html",
    "podelitsya.html",
}

MASTODON_LIMIT = 500
LINKEDIN_LIMIT = 3000  # actual cap is ~3000 chars

# Per-language label for "Back to source" / hashtags
LANG_LABELS = {
    "nl": {"by": "Door", "read_more": "Lees verder"},
    "de": {"by": "Von", "read_more": "Weiterlesen"},
    "en": {"by": "By", "read_more": "Read more"},
    "ru": {"by": "Автор", "read_more": "Читать дальше"},
}


# -----------------------------------------------------------------------------
# HTML metadata extraction
# -----------------------------------------------------------------------------
class MetaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.og_title = None
        self.og_description = None
        self.description = None
        self.og_image = None
        self.html_lang = None
        self._in_title = False
        self._stop = False

    def handle_starttag(self, tag, attrs):
        if self._stop:
            return
        if tag == "body":
            self._stop = True
            return
        if tag == "html":
            attr = dict(attrs)
            self.html_lang = attr.get("lang", "").strip().lower()
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            attr = dict(attrs)
            name = (attr.get("name") or "").lower()
            prop = (attr.get("property") or "").lower()
            content = attr.get("content", "").strip()
            if not content:
                return
            if prop == "og:title":
                self.og_title = content
            elif prop == "og:description":
                self.og_description = content
            elif prop == "og:image":
                self.og_image = content
            elif name == "description":
                self.description = content

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and self.title is None:
            self.title = data.strip()


def extract_metadata(html_path: Path) -> dict | None:
    try:
        html = html_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  WARN: cannot read {html_path}: {e}", file=sys.stderr)
        return None

    parser = MetaExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass

    title = parser.og_title or parser.title
    description = parser.og_description or parser.description

    if title:
        # Strip " · Het Open Vizier" / " | Het Open Vizier" suffix
        title = re.sub(r'\s*[·\|]\s*Het Open Vizier.*$', '', title).strip()

    if not title:
        return None

    return {
        "title": title,
        "description": description or "",
        "og_image": parser.og_image,
        "html_lang": parser.html_lang or "",
    }


# -----------------------------------------------------------------------------
# State
# -----------------------------------------------------------------------------
def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            print(f"  WARN: cannot parse {STATE_FILE}, starting fresh", file=sys.stderr)
    return {"posted": {}}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def state_key(platform: str, lang: str, url: str) -> str:
    """Composite key: platform | lang | url."""
    return f"{platform}|{lang}|{url}"


# -----------------------------------------------------------------------------
# Discover articles
# -----------------------------------------------------------------------------
def find_articles() -> list[tuple[Path, str]]:
    """Return list of (path, language) for all article HTML files."""
    articles = []
    for lang, dirs in LANG_DIRS.items():
        for d in dirs:
            dir_path = ROOT / d
            if not dir_path.is_dir():
                continue
            for f in sorted(dir_path.iterdir()):
                if f.is_file() and f.suffix == ".html" and f.name not in IGNORE_FILES:
                    articles.append((f, lang))
    return articles


def relative_url(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT).as_posix()
    return f"{SITE_BASE}/{rel}"


# -----------------------------------------------------------------------------
# Toot composition
# -----------------------------------------------------------------------------
def compose_short(meta: dict, url: str, limit: int) -> str:
    """Composes title + lead + URL within character limit."""
    title = meta["title"].strip()
    desc = meta["description"].strip()
    # Mastodon counts URLs as 23 chars; LinkedIn counts actual length
    url_count = 23 if limit == MASTODON_LIMIT else len(url)
    fixed_overhead = len(title) + url_count + 4  # 2× \n\n
    desc_budget = limit - fixed_overhead - 5  # safety margin

    if desc and desc_budget > 30:
        if len(desc) > desc_budget:
            desc = desc[:desc_budget - 1].rstrip() + "…"
        return f"{title}\n\n{desc}\n\n{url}"
    return f"{title}\n\n{url}"


# -----------------------------------------------------------------------------
# Mastodon API
# -----------------------------------------------------------------------------
def post_to_mastodon(status: str, lang: str) -> str | None:
    if DRY_RUN:
        print(f"  [DRY RUN][mastodon/{lang}] Would post ({len(status)} chars):")
        for ln in status.split("\n"):
            print(f"    | {ln}")
        return "https://dry-run.example/mastodon"

    if not MASTODON_INSTANCE or not MASTODON_TOKEN:
        return None  # silently skip if not configured

    url = f"https://{MASTODON_INSTANCE}/api/v1/statuses"
    data = json.dumps({
        "status": status,
        "visibility": "public",
        "language": lang,
    }).encode("utf-8")

    req = request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {MASTODON_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "openvizier-autopost/1.1",
            "Idempotency-Key": f"openvizier-mastodon-{lang}-{hash(status) & 0xffffffff:08x}",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return payload.get("url") or payload.get("uri") or "(no url)"
    except error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR mastodon HTTP {e.code}: {err_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ERROR mastodon: {e}", file=sys.stderr)
        return None


# -----------------------------------------------------------------------------
# LinkedIn — native UGC Posts API
# -----------------------------------------------------------------------------
def post_to_linkedin_native(status: str, lang: str, article_url: str) -> str | None:
    if not LINKEDIN_TOKEN or not LINKEDIN_AUTHOR_URN:
        return None

    if DRY_RUN:
        print(f"  [DRY RUN][linkedin-native/{lang}] Would post ({len(status)} chars):")
        for ln in status.split("\n"):
            print(f"    | {ln}")
        return "https://dry-run.example/linkedin-native"

    api_url = "https://api.linkedin.com/v2/ugcPosts"
    payload = {
        "author": LINKEDIN_AUTHOR_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": status},
                "shareMediaCategory": "ARTICLE",
                "media": [{
                    "status": "READY",
                    "originalUrl": article_url,
                }],
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }
    req = request.Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {LINKEDIN_TOKEN}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
            "User-Agent": "openvizier-autopost/1.1",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            urn = resp.headers.get("x-restli-id") or resp.headers.get("X-RestLi-Id") or "(no urn)"
            return f"https://www.linkedin.com/feed/update/{urn}"
    except error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR linkedin-native HTTP {e.code}: {err_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ERROR linkedin-native: {e}", file=sys.stderr)
        return None


# -----------------------------------------------------------------------------
# LinkedIn — Buffer/Zapier webhook fallback
# -----------------------------------------------------------------------------
def post_to_linkedin_buffer(status: str, lang: str, article_url: str, meta: dict) -> str | None:
    if not BUFFER_WEBHOOK_URL:
        return None

    if DRY_RUN:
        print(f"  [DRY RUN][linkedin-buffer/{lang}] Would webhook ({len(status)} chars)")
        return "https://dry-run.example/buffer"

    payload = {
        "platform": "linkedin",
        "language": lang,
        "text": status,
        "url": article_url,
        "title": meta.get("title", ""),
        "description": meta.get("description", ""),
        "image": meta.get("og_image", ""),
    }
    req = request.Request(
        BUFFER_WEBHOOK_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "openvizier-autopost/1.1",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            return f"buffer-webhook-{resp.status}"
    except error.HTTPError as e:
        print(f"  ERROR linkedin-buffer HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}",
              file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ERROR linkedin-buffer: {e}", file=sys.stderr)
        return None


def post_to_linkedin(status: str, lang: str, article_url: str, meta: dict) -> str | None:
    """Try native first, fall back to Buffer if configured."""
    if LINKEDIN_TOKEN and LINKEDIN_AUTHOR_URN:
        return post_to_linkedin_native(status, lang, article_url)
    if BUFFER_WEBHOOK_URL:
        return post_to_linkedin_buffer(status, lang, article_url, meta)
    return None  # not configured


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> int:
    # Detect which platforms are configured
    have_mastodon = bool(MASTODON_INSTANCE and MASTODON_TOKEN)
    have_linkedin = bool((LINKEDIN_TOKEN and LINKEDIN_AUTHOR_URN) or BUFFER_WEBHOOK_URL)

    if not have_mastodon and not have_linkedin and not DRY_RUN:
        print("No platform configured yet (Mastodon/LinkedIn secrets are empty).")
        print("This is fine — the workflow will start posting as soon as you add the secrets.")
        print("See scripts/AUTO_POST_SETUP.md for instructions.")
        return 0  # graceful exit, not a failure

    print(f"Platforms: mastodon={have_mastodon} linkedin={have_linkedin} dry_run={DRY_RUN}")

    state = load_state()
    posted = state.setdefault("posted", {})

    articles = find_articles()
    print(f"Found {len(articles)} articles across {len(LANG_DIRS)} languages")

    # Build queue of (platform, lang, path, url) tuples that still need posting
    # Only queue platforms that are actually configured
    queue: list[tuple[str, str, Path, str]] = []
    for path, lang in articles:
        url = relative_url(path)

        if have_mastodon:
            key = state_key("mastodon", lang, url)
            if key not in posted:
                queue.append(("mastodon", lang, path, url))

        if have_linkedin and lang in LINKEDIN_LANGS:
            key = state_key("linkedin", lang, url)
            if key not in posted:
                queue.append(("linkedin", lang, path, url))

    print(f"New post-targets in queue: {len(queue)}")

    if not queue:
        print("Nothing to do.")
        return 0

    # Bootstrap-cap
    if len(queue) > MAX_POSTS_PER_RUN:
        print(f"  Capping at {MAX_POSTS_PER_RUN} (bootstrap protection).")
        queue = queue[:MAX_POSTS_PER_RUN]

    success = 0
    failed = 0

    for platform, lang, path, url in queue:
        print(f"\n[{platform}/{lang}] {url}")
        meta = extract_metadata(path)
        if not meta:
            print("  SKIP: no metadata")
            continue

        limit = MASTODON_LIMIT if platform == "mastodon" else LINKEDIN_LIMIT
        status = compose_short(meta, url, limit)

        if platform == "mastodon":
            result = post_to_mastodon(status, lang)
        else:
            result = post_to_linkedin(status, lang, url, meta)

        if result:
            print(f"  ✓ posted: {result}")
            key = state_key(platform, lang, url)
            posted[key] = {
                "title": meta["title"],
                "platform": platform,
                "lang": lang,
                "posted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "result_url": result,
            }
            success += 1
            time.sleep(2)  # gentle pacing
        else:
            failed += 1
            print(f"  ✗ failed")

    save_state(state)
    print(f"\nDone. Success: {success}, Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
