#!/usr/bin/env python3
"""
Auto-post new articles from Het Open Vizier to Mastodon.

Detects new NL articles under nl/wat-opkomt/, nl/editie-N/, etc.
Extracts <title>, <meta description>, og:image.
Posts to Mastodon as a toot with title + lead + link.
Tracks posted URLs in .posted.json so each article posts only once.

Environment variables required:
- MASTODON_INSTANCE  (e.g. "mastodon.social" or "fosstodon.org" — no https://)
- MASTODON_TOKEN     (Mastodon application access token with 'write:statuses' scope)
- SITE_BASE_URL      (default: "https://openvizier.org")
- DRY_RUN            (optional: "1" to skip actual posting, log only)
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
MASTODON_INSTANCE = os.environ.get("MASTODON_INSTANCE", "").strip().rstrip("/")
MASTODON_TOKEN = os.environ.get("MASTODON_TOKEN", "").strip()
DRY_RUN = os.environ.get("DRY_RUN", "").strip() in ("1", "true", "yes")

# Only NL articles for now. Pattern: nl/wat-opkomt/*.html and nl/editie-N/*.html
NL_DIRS = ["nl/wat-opkomt", "nl/editie-0", "nl/editie-1", "nl/editie-2",
           "nl/editie-3", "nl/editie-4", "nl/editie-5", "nl/editie-6"]

# Files to ignore: index pages, share, about, etc.
IGNORE_FILES = {"index.html", "delen.html", "over.html"}

# Maximum length for Mastodon toot
MASTODON_LIMIT = 500


# -----------------------------------------------------------------------------
# Metadata extraction
# -----------------------------------------------------------------------------
class MetaExtractor(HTMLParser):
    """Parses an HTML head and pulls <title>, og:title, og:description, description."""

    def __init__(self):
        super().__init__()
        self.title = None
        self.og_title = None
        self.og_description = None
        self.description = None
        self.og_image = None
        self._in_title = False
        self._stop = False

    def handle_starttag(self, tag, attrs):
        if self._stop:
            return
        if tag == "body":
            self._stop = True
            return
        if tag == "title":
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
    """Return {title, description, og_image} or None if extraction failed."""
    try:
        html = html_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  WARN: cannot read {html_path}: {e}", file=sys.stderr)
        return None

    parser = MetaExtractor()
    try:
        parser.feed(html)
    except Exception:
        # Continue with whatever we parsed before the error
        pass

    title = parser.og_title or parser.title
    description = parser.og_description or parser.description

    # Clean up title (strip " · Het Open Vizier" suffix)
    if title:
        title = re.sub(r'\s*[·\|]\s*Het Open Vizier.*$', '', title).strip()

    if not title:
        return None

    return {
        "title": title,
        "description": description or "",
        "og_image": parser.og_image,
    }


# -----------------------------------------------------------------------------
# State tracking
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


# -----------------------------------------------------------------------------
# Discover articles
# -----------------------------------------------------------------------------
def find_articles() -> list[Path]:
    """Return list of NL article HTML files (excluding index/share/about)."""
    articles = []
    for d in NL_DIRS:
        dir_path = ROOT / d
        if not dir_path.is_dir():
            continue
        for f in sorted(dir_path.iterdir()):
            if f.is_file() and f.suffix == ".html" and f.name not in IGNORE_FILES:
                articles.append(f)
    return articles


def relative_url(html_path: Path) -> str:
    """Convert workspace path to public URL."""
    rel = html_path.relative_to(ROOT).as_posix()
    return f"{SITE_BASE}/{rel}"


# -----------------------------------------------------------------------------
# Toot composition
# -----------------------------------------------------------------------------
def compose_toot(meta: dict, url: str) -> str:
    """Compose toot text within Mastodon limit."""
    title = meta["title"].strip()
    desc = meta["description"].strip()
    
    # Account for newlines and URL in budget
    # URL counts as 23 chars in Mastodon regardless of actual length
    fixed_overhead = len(title) + 23 + 4  # title + url + 2 newlines + space
    desc_budget = MASTODON_LIMIT - fixed_overhead - 5  # safety margin

    if desc and desc_budget > 30:
        if len(desc) > desc_budget:
            desc = desc[:desc_budget - 1].rstrip() + "…"
        return f"{title}\n\n{desc}\n\n{url}"
    else:
        return f"{title}\n\n{url}"


# -----------------------------------------------------------------------------
# Mastodon API
# -----------------------------------------------------------------------------
def post_to_mastodon(status: str) -> str | None:
    """Post a status to Mastodon. Returns the toot URL on success, None on failure."""
    if DRY_RUN:
        print(f"  [DRY RUN] Would post:\n---\n{status}\n---")
        return "https://dry-run.example/dummy"

    if not MASTODON_INSTANCE or not MASTODON_TOKEN:
        print("  ERROR: MASTODON_INSTANCE or MASTODON_TOKEN missing", file=sys.stderr)
        return None

    url = f"https://{MASTODON_INSTANCE}/api/v1/statuses"
    data = json.dumps({
        "status": status,
        "visibility": "public",
        "language": "nl",
    }).encode("utf-8")

    req = request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {MASTODON_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "openvizier-autopost/1.0",
            "Idempotency-Key": f"openvizier-{int(time.time())}-{hash(status) & 0xffff:04x}",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            payload = json.loads(body)
            return payload.get("url") or payload.get("uri") or "(no url returned)"
    except error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR: HTTP {e.code} from Mastodon: {err_body}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        return None


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> int:
    state = load_state()
    posted = state.setdefault("posted", {})

    articles = find_articles()
    print(f"Found {len(articles)} NL articles total")

    new_articles = []
    for a in articles:
        url = relative_url(a)
        if url not in posted:
            new_articles.append((a, url))

    print(f"New articles to post: {len(new_articles)}")

    if not new_articles:
        print("Nothing to do.")
        return 0

    # Cap: max 3 posts per run to avoid flooding on initial bootstrap
    MAX_PER_RUN = 3
    if len(new_articles) > MAX_PER_RUN:
        print(f"  Capping at {MAX_PER_RUN} posts/run (bootstrap protection).")
        new_articles = new_articles[:MAX_PER_RUN]

    success_count = 0
    failed_count = 0

    for article_path, url in new_articles:
        print(f"\nProcessing: {url}")
        meta = extract_metadata(article_path)
        if not meta:
            print(f"  SKIP: could not extract metadata")
            continue

        toot = compose_toot(meta, url)
        print(f"  Composed toot ({len(toot)} chars):")
        for line in toot.split("\n"):
            print(f"    | {line}")

        toot_url = post_to_mastodon(toot)
        if toot_url:
            print(f"  ✓ Posted: {toot_url}")
            posted[url] = {
                "title": meta["title"],
                "posted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "toot_url": toot_url,
            }
            success_count += 1
            # Rate-limit pause between posts
            if len(new_articles) > 1:
                time.sleep(2)
        else:
            failed_count += 1

    save_state(state)

    print(f"\nDone. Success: {success_count}, Failed: {failed_count}")
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
