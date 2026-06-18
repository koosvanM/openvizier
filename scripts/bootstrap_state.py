#!/usr/bin/env python3
"""
One-time bootstrap: mark all existing articles (NL/DE/EN/RU) as 'already posted'
on both Mastodon and LinkedIn, so the auto-post workflow only posts NEW
articles published after the workflow is enabled.

Run this once locally:
  python scripts/bootstrap_state.py

State structure: keys are "platform|lang|url" so each (platform, lang, url)
combo posts at most once.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auto_post import (
    find_articles, relative_url, extract_metadata,
    STATE_FILE, state_key, LINKEDIN_LANGS,
)


def main() -> int:
    articles = find_articles()
    print(f"Found {len(articles)} articles across all languages")

    state = {"posted": {}}
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    mastodon_count = 0
    linkedin_count = 0

    for path, lang in articles:
        url = relative_url(path)
        meta = extract_metadata(path)
        title = meta["title"] if meta else path.stem

        # Mastodon: all 4 languages
        mkey = state_key("mastodon", lang, url)
        state["posted"][mkey] = {
            "title": title,
            "platform": "mastodon",
            "lang": lang,
            "posted_at": now,
            "result_url": "(bootstrap)",
            "bootstrap": True,
        }
        mastodon_count += 1

        # LinkedIn: only NL + EN
        if lang in LINKEDIN_LANGS:
            lkey = state_key("linkedin", lang, url)
            state["posted"][lkey] = {
                "title": title,
                "platform": "linkedin",
                "lang": lang,
                "posted_at": now,
                "result_url": "(bootstrap)",
                "bootstrap": True,
            }
            linkedin_count += 1

    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {STATE_FILE}:")
    print(f"  - {mastodon_count} mastodon entries (all 4 languages)")
    print(f"  - {linkedin_count} linkedin entries (NL + EN only)")
    print(f"  - {mastodon_count + linkedin_count} total")
    print("All current articles are now marked as already posted.")
    print("The auto-post workflow will only post NEW articles from this point on.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
