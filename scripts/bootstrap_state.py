#!/usr/bin/env python3
"""
One-time bootstrap: mark all existing NL articles as 'already posted' so the
auto-post workflow only posts NEW articles published after the workflow is
enabled.

Run this once locally before enabling the GitHub Actions workflow:
  python scripts/bootstrap_state.py

Output: .posted.json with all current articles marked as posted at this moment.
"""

import json
import sys
import time
from pathlib import Path

# Import the discovery + URL helpers from auto_post
sys.path.insert(0, str(Path(__file__).parent))
from auto_post import find_articles, relative_url, extract_metadata, STATE_FILE


def main() -> int:
    articles = find_articles()
    print(f"Found {len(articles)} NL articles")

    state = {"posted": {}}
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    for a in articles:
        url = relative_url(a)
        meta = extract_metadata(a)
        title = meta["title"] if meta else a.stem
        state["posted"][url] = {
            "title": title,
            "posted_at": now,
            "toot_url": "(bootstrap — not actually posted)",
            "bootstrap": True,
        }

    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {STATE_FILE} with {len(state['posted'])} entries.")
    print("All current articles are now marked as posted.")
    print("The auto-post workflow will only post NEW articles from this point on.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
